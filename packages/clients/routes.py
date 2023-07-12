import logging

import dateparser
import pytz
import requests

from packages.clients.base_client import BaseClient
from packages.enums import Field_Masks
from packages.models.route_response import RouteResponse


# https://developers.google.com/maps/documentation/routes
class Routes(BaseClient):
    def get_response(
        self, origin, destination, departureTime=None, timezone=None, avoidTolls=False
    ):
        response = self.get_raw_response(
            origin, destination, departureTime, timezone, avoidTolls
        )
        self.handle_error(response)
        return self.get_response_model(response)

    def get_raw_response(
        self, origin, destination, departureTime, timezone, avoidTolls
    ):
        url = "https://routes.googleapis.com/directions/v2:computeRoutes"
        headers = self.build_headers()
        payload = self.build_payload(
            origin, destination, departureTime, timezone, avoidTolls
        )
        logging.debug({"headers": headers, "payload": payload})

        response = requests.post(
            url,
            headers=headers,
            json=payload,
        )
        logging.debug(response.json())
        return response.json()

    def build_headers(self):
        FIELD_MASK = Field_Masks.string_list()
        return {
            "Content-Type": "application/json",
            "X-Goog-Api-Key": self.api_key,
            "X-Goog-FieldMask": FIELD_MASK,
        }

    def build_payload(self, origin, destination, departureTime, timezone, avoidTolls):
        payload = dict()
        payload["origin"] = self.build_location(origin)
        payload["destination"] = self.build_location(destination)
        payload["departureTime"] = self.build_time(departureTime, timezone)
        payload["travelMode"] = self.build_travel_mode()
        payload["routingPreference"] = self.build_routing_preferences()
        payload["extraComputations"] = self.build_extra_computations()
        payload["routeModifiers"] = self.build_route_modifiers(avoidTolls)
        return payload

    def build_location(self, location):
        if isinstance(location, str):
            return self.build_address(location)
        lat, lng = location
        return self.build_coordinates(lat, lng)

    def build_address(self, address):
        return {"address": address}

    def build_coordinates(self, lat, lng):
        return {"location": {"latLng": {"latitude": lat, "longitude": lng}}}

    def build_time(self, time_string, timezone):
        if not time_string:
            return None
        datetime = dateparser.parse(time_string)
        datetime = self.update_datetime_time_aware(datetime, timezone)
        return datetime.isoformat()

    def update_datetime_time_aware(self, datetime, timezone):
        # Avialable timezones: https://gist.github.com/heyalexej/8bf688fd67d7199be4a1682b3eec7568
        DEFAULT_TIMEZONE = "America/Mexico_City"
        if not timezone:
            timezone = DEFAULT_TIMEZONE
        tz = pytz.timezone(timezone)
        return datetime.replace(tzinfo=pytz.utc).astimezone(tz)

    def build_travel_mode(self):
        DEFAULT_MODE = "DRIVE"
        return DEFAULT_MODE

    def build_routing_preferences(self):
        DEFAUTLT_TRAFFIC = "TRAFFIC_AWARE_OPTIMAL"
        return DEFAUTLT_TRAFFIC

    def build_extra_computations(self):
        DEFAULT = "TOLLS"
        extra_computations = [DEFAULT]
        return extra_computations

    def build_route_modifiers(self, avoidTolls):
        route_modifiers = dict()
        route_modifiers["avoidTolls"] = avoidTolls
        return route_modifiers

    def handle_error(self, response):
        if not 'error' in response.keys():
            return
        msg = response["error"]["message"]
        raise ValueError(msg)

    def get_response_model(self, response):
        meters = response["routes"][0]["distanceMeters"]
        duration = response["routes"][0]["duration"]
        seconds = self.get_duration_seconds(duration)
        toll_info = self.get_toll_data(response)
        return RouteResponse(
            meters=int(meters),
            seconds=seconds,
            toll_amount=toll_info.get("amount"),
            toll_currency=toll_info.get("currency"),
        )

    def get_toll_data(self, response):
        DEFAULT_DATA = {"amount": None, "currency": None}
        if "travelAdvisory" not in response["routes"][0].keys():
            return DEFAULT_DATA
        tollInfo = response["routes"][0]["travelAdvisory"]["tollInfo"]
        toll_amount = tollInfo["estimatedPrice"][0]["units"]
        toll_currency = tollInfo["estimatedPrice"][0]["currencyCode"]
        return {"amount": int(toll_amount), "currency": toll_currency}

    def get_duration_seconds(self, duration):
        value = int(duration[:-1])
        if "s" in duration:
            return value
        if "m" in duration:
            return 60 * value
        if "h" in duration:
            return 3600 * value
