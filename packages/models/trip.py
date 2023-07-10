from dataclasses import dataclass
from typing import Optional

from packages.enums import Google_Modes, User_Modes


@dataclass
class Trip:
    id: str
    id_viaje: str
    origen_lat: float
    origen_lng: float
    origen_address: str
    destination_lat: float
    destination_lng: float
    destination_address: str
    mode: str
    departure_time: str
    timezone: Optional[str]
    avoid: str

    def has_origin_address(self):
        if self.origen_address == None:
            return False
        if self.origen_address == "":
            return False
        return True

    def has_destination_address(self):
        if self.destination_address == None:
            return False
        if self.destination_address == "":
            return False
        return True

    def get_origin_coordinates(self):
        return (self.origen_lat, self.origen_lng)

    def get_destination_coordinates(self):
        return (self.destination_lat, self.destination_lng)

    def get_user_mode(self):
        return User_Modes(self.mode).name

    def get_google_mode(self):
        if self.mode == User_Modes.car.value:
            google_mode = Google_Modes.car
        if self.mode == User_Modes.transit.value or self.mode == User_Modes.bus.value:
            google_mode = Google_Modes.transit
        if self.mode == User_Modes.walk.value:
            google_mode = Google_Modes.walk
        return google_mode.value

    def use_bus(self):
        return self.mode == User_Modes.bus

    def get_avoid_tolls(self):
        if not self.avoid:
            return False
        if "tolls" in self.avoid:
            return True
        return False
