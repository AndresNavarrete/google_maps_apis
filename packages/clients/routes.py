import requests

from packages.clients.base_client import BaseClient
from packages.enums import Field_Masks
class Routes(BaseClient):

    def get_route(self,  origin, destination, avoidTolls=False):
        url = "https://routes.googleapis.com/directions/v2:computeRoutes"
        headers = self.build_headers()
        payload = self.build_payload(origin, destination, avoidTolls)
        response = requests.post(
            url,
            headers=headers,
            json=payload,
        )
        return response 

    def build_headers(self):
        FIELD_MASK = Field_Masks.string_list()
        return {
            "Content-Type": "application/json",
            "X-Goog-Api-Key": self.api_key,
            "X-Goog-FieldMask": FIELD_MASK,
        }
    
    def build_payload(self, origin, destination, avoidTolls):
        payload = dict()
        payload["origin"] = self.build_address(origin)
        payload["destination"] = self.build_address(destination)
        payload["travelMode"] = "DRIVE"
        payload["routingPreference"] = "TRAFFIC_AWARE"
        payload["extraComputations"] = ["TOLLS"]
        payload["routeModifiers"] = self.build_route_modifiers(avoidTolls)
        return payload
    
    def build_address(self, address):
        return {"address": address}
    
    def build_route_modifiers(self, avoidTolls):
        route_modifiers = dict()
        route_modifiers["avoidTolls"] = avoidTolls
        return route_modifiers

