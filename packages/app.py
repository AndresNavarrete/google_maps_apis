from datetime import datetime

from packages.clients.directions import Directions
from packages.clients.routes import Routes
from packages.files.input_parser import InputParser
from packages.files.output_directions import OutputDirections
from packages.files.output_routes import OutputRoutes
from packages.providers.directions_provider import DirectionsProvider
from packages.providers.routes_providers import RoutesProvider
from packages.validation.validator import Validator
import logging

class App:
    logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    def __init__(self, api_key, input_file, service_name) -> None:
        self.api_key = api_key
        self.input_file = input_file
        self.service_name = service_name

    def execute(self):
        self.set_inputs()
        self.execute_service()

    def set_inputs(self):
        path = f"resources/{self.input_file}"
        self.input_parser = InputParser(path)
        Validator(self.input_parser).validate_input()

    def execute_service(self):
        if self.service_name == "directions":
            return self.execute_directions()
        if self.service_name == "routes":
            return self.execute_routes()
        msg = f"Invalid service name: {self.service_name}. Try directions or routes"
        raise ValueError(msg)

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
        output = OutputDirections(output_path)
        output.export(trips, results)

    def get_time_string(self):
        return datetime.now().strftime("%Y-%m-%d_at_%H:%M")

    def execute_routes(self):
        trips = self.input_parser.trips
        results = self.get_routes_results()
        self.process_routes_output(trips, results)

    def get_routes_results(self):
        routes = Routes(self.api_key)
        manager = RoutesProvider(self.input_parser, routes)
        manager.execute()
        return manager.responses

    def process_routes_output(self, trips, results):
        time = self.get_time_string()
        output_path = f"resources/routes_{time}.xlsx"
        output = OutputRoutes(output_path)
        output.export(trips, results)

