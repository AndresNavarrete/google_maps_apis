import json

import pandas

from packages.models.trip_request import TripRequest


class InputParser:
    def __init__(self, input_path):
        self.input_path = input_path
        self.requests = list()
        self.trips = list()
        self.load_input()

    def load_input(self):
        self.read_excel()
        self.generate_trip_requests()

    def read_excel(self):
        df = pandas.read_excel(self.input_path, sheet_name="Viajes")
        input_json = df.to_json(orient="records")
        self.requests = json.loads(input_json)

    def generate_trip_requests(self):
        for row in self.requests:
            new_trip = self.get_trip_requests(row)
            self.trips.append(new_trip)

    def get_trip_requests(self, row):
        return TripRequest(
            id=row["ID"],
            origen_lat=row["Origen_Lat"],
            origen_lng=row["Origen_Lng"],
            origen_address=row["Origen_str"],
            destination_lat=row["Destino_Lat"],
            destination_lng=row["Destino_Lng"],
            destination_address=row["Destino_str"],
            mode=row["Modo"],
            departure_time=row["Hora"],
            id_viaje=row["ID_Viaje"],
            avoid_tolls=row["Parameter_avoid"],
        )
