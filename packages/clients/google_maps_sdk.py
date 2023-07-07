from googlemaps import Client
from packages.clients.base_client import BaseClient


### Docs https://github.com/googlemaps/google-maps-services-python
class GoogleMapsSDK(BaseClient):
    def __init__(self, api_key):
        super().__init__(api_key)
        self.gmaps = Client(self.api_key)
