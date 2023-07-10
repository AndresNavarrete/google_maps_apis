from packages.clients.google_maps_sdk import GoogleMapsSDK
from packages.enums import Google_Modes


# https://developers.google.com/maps/documentation/directions
class Directions(GoogleMapsSDK):
    def get_response(
        self, origin, destination, mode, departure_time, parameter_avoid, only_bus
    ):
        directions_response = self.get_directions_response(
            origin, destination, mode, departure_time, parameter_avoid, only_bus
        )
        if not directions_response:
            return self.get_default_response()
        trip = directions_response[0]["legs"][0]
        steps = self.get_steps_information(trip, mode)
        wait_time, walk_time, travel_time = self.get_desagregated_time(
            trip, steps, mode
        )

        response = {
            "distance": trip["distance"]["value"],
            "duration": trip["duration_in_traffic"]["value"],
            "end_address": trip["end_address"],
            "end_location_lat": trip["end_location"]["lat"],
            "end_location_lng": trip["end_location"]["lng"],
            "start_address": trip["start_address"],
            "start_location_lat": trip["start_location"]["lat"],
            "start_location_lng": trip["start_location"]["lng"],
            "wait_time": wait_time,
            "walk_time": walk_time,
            "travel_time": travel_time,
            "transfers": self.get_transfer_number(steps),
            "steps": steps,
        }
        return response

    def get_directions_response(
        self, origin, destination, mode, departure_time, parameter_avoid, only_bus=False
    ):
        if only_bus:
            transit_mode = Google_Modes.bus
        else:
            transit_mode = None
        directions_response = self.gmaps.directions(
            origin,
            destination,
            mode=mode,
            transit_mode=transit_mode,
            departure_time=departure_time,
            avoid=parameter_avoid,
        )
        return directions_response

    def get_default_response(self):
        return {
            "distance": None,
            "duration": None,
            "end_address": None,
            "end_location_lat": None,
            "end_location_lng": None,
            "start_address": None,
            "start_location_lat": None,
            "start_location_lng": None,
            "wait_time": None,
            "walk_time": None,
            "travel_time": None,
            "transfers": None,
            "steps": [],
        }

    def get_steps_information(self, trip, mode):
        steps = list()
        if mode != "transit":
            return steps
        for step in trip["steps"]:
            step_info = self.get_new_step(step)
            steps.append(step_info)
        return steps

    def get_new_step(self, step):
        step_info = {
            "distance": step["distance"]["value"],
            "duration": step["duration_in_traffic"]["value"],
            "travel_mode": step["travel_mode"],
            "instruction": step["html_instructions"],
            "headway": 0,
        }
        if step["travel_mode"] == "TRANSIT":
            step_info["headway"] = step["transit_details"]["headway"]

        return step_info

    def get_desagregated_time(self, trip, steps, mode):
        wait_time = 0
        walk_time = 0
        travel_time = 0
        if mode in ("driving", "walking"):
            travel_time = trip["duration_in_traffic"]["value"]
        if mode == "transit":
            walk_time = sum(
                [step["duration"] for step in steps if step["travel_mode"] == "WALKING"]
            )
            travel_time = sum(
                [
                    step["duration"]
                    for step in steps
                    if step["travel_mode"] in ("TRANSIT", "DRIVING")
                ]
            )
            wait_time = max(trip["duration"]["value"] - walk_time - travel_time, 0)
        return wait_time, walk_time, travel_time

    def get_transfer_number(self, steps):
        transfers = 0
        for step in steps:
            if step["travel_mode"] == "TRANSIT":
                transfers += 1
        return max(0, transfers - 1)
