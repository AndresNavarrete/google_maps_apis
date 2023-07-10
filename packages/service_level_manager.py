import datetime

import dateparser

from packages.clients.directions import Directions
from packages.files.output_directions import OutputDirections
from packages.input_parser import InputParser
from packages.validator import Validator


class ServiceLevelManager:
    def __init__(self, input_path, api_key):
        self.input_path = input_path
        self.input = InputParser(input_path)
        self.validator = Validator(self.input)
        time = datetime.datetime.now().strftime("%d_%m")
        output_path = "resources/" + time + ".xlsx"
        self.output = OutputDirections(output_path)
        self.directions = Directions(api_key)
        self.responses = []

    def execute(self):
        self.validate_input()
        self.get_all_service_levels()
        self.fill_output()
        self.write_output()

    def validate_input(self):
        self.validator.validate_input()

    def get_all_service_levels(self):
        for trip in self.input.trips:
            self.get_service_level(trip)
            print(f"Processed request {trip.id}")

    def get_service_level(self, trip):
        origin = self.get_origin(trip)
        destination = self.get_destination(trip)
        mode = trip.get_google_mode()
        hour = trip.departure_time
        parameter_avoid = trip.avoid
        date = dateparser.parse(hour)
        only_bus = trip.use_bus()

        response = self.directions.get_directions(
            origin, destination, mode, date, parameter_avoid, only_bus
        )
        self.responses.append(response)

    def get_origin(self, trip):
        if trip.has_origin_address():
            return trip.origen_address
        return trip.get_origin_coordinates()

    def get_destination(self, trip):
        if trip.has_destination_address():
            return trip.destination_address
        return trip.get_destination_coordinates()

    def fill_output(self):
        for request, response in zip(self.input.requests, self.responses):
            self.output.add_trip(request, response)

    def write_output(self):
        self.output.write_excel()
