from datetime import datetime

from packages.clients.directions import Directions
from packages.clients.routes import Routes
from packages.files.input_parser import InputParser
from packages.files.output_directions import OutputDirections
from packages.files.output_routes import OutputRoutes
from packages.providers.directions_provider import DirectionsProvider
from packages.vaiidation.validator import Validator


class App:
    def __init__(self, api_key, input_file, service_name) -> None:
        self.api_key = api_key
        self.input_file = input_file
        self.service_name = service_name

    def execute(self):
        self.set_inputs()
        self.execute_directions()

    def set_inputs(self):
        path = f"resources/{self.input_file}"
        self.input_parser = InputParser(path)
        Validator(self.input_parser).validate_input()

    def execute_directions(self):
        trips = self.input_parser.requests
        results = self.get_directions_results()
        self.process_direction_output(trips, results)

    def get_directions_results(self):
        self.directions = Directions(self.api_key)
        manager = DirectionsProvider(self.input_parser, self.directions)
        manager.execute()
        return manager.responses

    def process_direction_output(self, trips, results):
        time = self.get_time_string()
        output_path = f"resources/directions_{time}.xlsx"
        self.output_directions = OutputDirections(output_path)
        self.output_directions.export(trips, results)

    def get_time_string(self):
        return datetime.now().strftime("%Y-%m-%d_at_%H:%M")

    def set_routes(self):
        time = self.get_time_string()
        output_path = f"resources/routes_{time}.xlsx"
        self.output_directions = OutputRoutes(output_path)
        self.directions = Routes(self.api_key)