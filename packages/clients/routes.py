import dateparser
import pytz
import requests

from packages.clients.base_client import BaseClient
from packages.enums import Field_Masks


# https://developers.google.com/maps/documentation/routes
class Routes(BaseClient):
    def get_route(
        self, origin, destination, departureTime=None, timezone=None, avoidTolls=False
    ):
        url = "https://routes.googleapis.com/directions/v2:computeRoutes"
        headers = self.build_headers()
        payload = self.build_payload(
            origin, destination, departureTime, timezone, avoidTolls
        )
        response = requests.post(
            url,
            headers=headers,
            json=payload,
        )
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
        payload["origin"] = self.build_address(origin)
        payload["destination"] = self.build_address(destination)
        payload["departureTime"] = self.build_time(departureTime, timezone)
        payload["travelMode"] = "DRIVE"
        payload["routingPreference"] = "TRAFFIC_AWARE_OPTIMAL"
        payload["extraComputations"] = ["TOLLS"]
        payload["routeModifiers"] = self.build_route_modifiers(avoidTolls)
        return payload

    def build_address(self, address):
        return {"address": address}

    def build_time(self, time_string, timezone):
        if not time_string:
            return None
        datetime = dateparser.parse(time_string)
        datetime = self.update_datetime_time_aware(datetime, timezone)
        return datetime.isoformat()

    def update_datetime_time_aware(self, datetime, timezone):
        # Avialable timezones: https://gist.github.com/heyalexej/8bf688fd67d7199be4a1682b3eec7568
        DEFAULT_TIMEZONE = "America/Santiago"
        if not timezone:
            timezone = DEFAULT_TIMEZONE
        tz = pytz.timezone(timezone)
        return datetime.replace(tzinfo=pytz.utc).astimezone(tz)

    def build_route_modifiers(self, avoidTolls):
        route_modifiers = dict()
        route_modifiers["avoidTolls"] = avoidTolls
        return route_modifiers
