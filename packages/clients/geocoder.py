from packages.clients.google_maps_sdk import GoogleMapsSDK


# https://developers.google.com/maps/documentation/geocoding
class Geocoder(GoogleMapsSDK):
    def get_coordinates(self, location):
        response = self.get_geocode_response(location)
        formatted_address = response[0]["formatted_address"]
        lat = response[0]["geometry"]["location"]["lat"]
        lng = response[0]["geometry"]["location"]["lng"]
        coord_response = {
            "location_input": location,
            "lat": lat,
            "lng": lng,
            "formatted_address": formatted_address,
        }
        return coord_response

    def get_geocode_response(self, location):
        geocode_result = self.gmaps.geocode(location)
        return geocode_result
