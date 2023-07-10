import datetime

import dateparser

from packages.providers.base_provider import BaseProvider


class DirectionsProvider(BaseProvider):
    def get_service_level(self, trip):
        origin = self.get_origin(trip)
        destination = self.get_destination(trip)
        mode = trip.get_google_mode()
        hour = trip.departure_time
        parameter_avoid = trip.avoid
        date = dateparser.parse(hour)
        only_bus = trip.use_bus()

        response = self.directions.get_response(
            origin, destination, mode, date, parameter_avoid, only_bus
        )
        self.responses.append(response)
