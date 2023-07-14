import logging
from abc import ABC


class BaseProvider(ABC):
    def __init__(self, input_parser, client) -> None:
        self.input = input_parser
        self.client = client
        self.responses = list()

    def execute(self):
        for trip in self.input.trips:
            self.hande_trip(trip)

    def hande_trip(self, trip):
        try:
            self.execute_service_level_request(trip)
        except Exception as error:
            self.handle_trip_error(trip, error)

    def execute_service_level_request(self, trip):
        response = self.get_service_level(trip)
        self.responses.append(response)
        msg = f"Processed request {trip.id}"
        logging.info(msg)

    def handle_trip_error(self, trip, error):
        response = self.client.get_default_response()
        self.responses.append(response)
        msg = f"Error on: {trip.id}. {error}"
        logging.warning(msg)

    def get_service_level(self, trip):
        return None

    def get_origin(self, trip):
        if trip.has_origin_address():
            return trip.origen_address
        return trip.get_origin_coordinates()

    def get_destination(self, trip):
        if trip.has_destination_address():
            return trip.destination_address
        return trip.get_destination_coordinates()
