import pandas as pd 


class OutputDirections:
    def __init__(self, output_path):
        self.output_path = output_path
        self.steps = []
        self.trips = []

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
        trips = pd.DataFrame(self.trips)
        steps = pd.DataFrame(self.steps)
        with pd.ExcelWriter(self.output_path) as writer:
            trips.to_excel(writer, sheet_name="Viajes")
            steps.to_excel(writer, sheet_name="Etapas")
