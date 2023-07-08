import datetime

import dateparser

from packages.clients.directions import Directions
from packages.enums import Google_Modes, User_Modes
from packages.input_parser import InputParser
from packages.output_parser import OutputParser
from packages.validator import Validator


class ServiceLevelManager:
    def __init__(self, input_path, api_key):
        self.input_path = input_path
        self.input = InputParser(input_path)
        self.validator = Validator(self.input)
        time = datetime.datetime.now().strftime("%d_%m")
        output_path = "resources/" + time + ".xlsx"
        self.output = OutputParser(output_path)
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
        for request in self.input.requests:
            self.get_service_level(request)
            print("Processed request {}".format(request["ID"]))

    def get_service_level(self, request):
        origin = self.get_origin(request)
        destination = self.get_destination(request)
        mode = self.get_mode(request)
        hour = request["Hora"]
        parameter_avoid = request["Parameter_avoid"]
        date = dateparser.parse(hour)
        only_bus = request["Modo"] == User_Modes.bus

        response = self.directions.get_directions(
            origin, destination, mode, date, parameter_avoid, only_bus
        )
        self.responses.append(response)

    def get_origin(self, request):
        if request["Origen_str"] is None:
            return (request["Origen_Lat"], request["Origen_Lng"])
        return request["Origen_str"]

    def get_destination(self, request):
        if request["Destino_str"] is None:
            return (request["Destino_Lat"], request["Destino_Lng"])
        return request["Destino_str"]

    def get_mode(self, request):
        if request["Modo"] == User_Modes.car:
            mode = Google_Modes.car
        if request["Modo"] == User_Modes.transit or request["Modo"] == User_Modes.bus:
            mode = Google_Modes.transit
        if request["Modo"] == User_Modes.walk:
            mode = Google_Modes.walk

        return mode

    def fill_output(self):
        for request, response in zip(self.input.requests, self.responses):
            self.output.add_trip(request, response)

    def write_output(self):
        self.output.write_excel()
