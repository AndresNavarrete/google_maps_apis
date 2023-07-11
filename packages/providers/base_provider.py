import logging
from abc import ABC


class BaseProvider(ABC):
    def __init__(self, input_parser, client) -> None:
        self.input = input_parser
        self.client = client
        self.responses = list()

    def execute(self):
        for trip in self.input.trips:
            self.get_service_level(trip)
            msg = f"Processed request {trip.id}"
            logging.info(msg)

    def get_service_level(self, trip):
        pass

    def get_origin(self, trip):
        if trip.has_origin_address():
            return trip.origen_address
        return trip.get_origin_coordinates()

    def get_destination(self, trip):
        if trip.has_destination_address():
            return trip.destination_address
        return trip.get_destination_coordinates()
