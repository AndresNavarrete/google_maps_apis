import json

import pandas as pd

from packages.files.base_output import BaseOutput


class OutputDirections(BaseOutput):
    def export(self, trips, results, excel):
        self.trips = list()
        self.steps = list()
        for request, response in zip(trips, results):
            self.add_trip(request, response)
        if excel:
            self.write_excel()
        else:
            self.export_json()

    def add_trip(self, request, response):
        new_trip = {
            "id": request["ID"],
            "modo": request["Modo"],
            "hora": request["Hora"],
            "origen_direccion": response["start_address"],
            "origen_lat": response["start_location_lat"],
            "origen_lng": response["start_location_lng"],
            "destino_direccion": response["end_address"],
            "destino_lat": response["end_location_lat"],
            "destino_lng": response["end_location_lng"],
            "transbordos": response["transfers"],
            "distancia_m": response["distance"],
            "tiempo_total_seg": response["duration"],
            "tiempo_espera_seg": response["wait_time"],
            "tiempo_caminata_seg": response["walk_time"],
            "tiempo_viaje_seg": response["travel_time"],
        }
        self.trips.append(new_trip)
        for step in response["steps"]:
            self.add_step(step, request["ID"])

    def add_step(self, step, trip_id):
        new_step = {
            "viaje_id": trip_id,
            "modo": step["travel_mode"],
            "distancia_m": step["distance"],
            "tiempo_total_seg": step["duration"],
            "tiempo_espera_seg": step["headway"],
            "indicacion": step["instruction"],
        }
        self.steps.append(new_step)

    def write_excel(self):
        path = f"{self.output_path}.xlsx"
        trips = pd.DataFrame(self.trips)
        steps = pd.DataFrame(self.steps)
        with pd.ExcelWriter(path) as writer:
            trips.to_excel(writer, sheet_name="Viajes")
            steps.to_excel(writer, sheet_name="Etapas")

    def export_json(self):
        trips_path = f"{self.output_path}_trips.json"
        steps_path = f"{self.output_path}_steps.json"

        with open(trips_path, "w") as f:
            json.dump(self.trips, f)
        with open(steps_path, "w") as f:
            json.dump(self.steps, f)
