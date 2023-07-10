import dateparser

from packages.providers.base_provider import BaseProvider


class RoutesProvider(BaseProvider):
    def get_service_level(self, trip):
        origin = self.get_origin(trip)
        destination = self.get_destination(trip)
        departureTime = trip.departure_time
        timezone = trip.timezone
        avoidTolls = trip.geget_avoid_tolls()

        response = self.directions.get_response(
            origin, destination, departureTime, timezone, avoidTolls
        )
        self.responses.append(response)
