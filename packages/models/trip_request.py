from dataclasses import dataclass

from packages.enums import Google_Modes, User_Modes

@dataclass
class TripRequest:
    id: str
    origen_lat: float
    origen_lng: float
    origen_address: str
    destination_lat: float
    destination_lng: float
    destination_adress: str
    modo: str
    hora: str
    id_viaje: str
    avoid_tolls: bool

    def has_origin_address(self):
        if self.origen_address == None:
            return False
        if self.origen_address == "":
            return False
        return True

    def has_destination_address(self):
        if self.destination_adress == None:
            return False
        if self.destination_adress == "":
            return False
        return True
    
    def get_origin_coordinates(self):
        return (self.origen_lat, self.origen_lng)
    
    def get_destination_coordinates(self):
        return (self.destination_lat, self.destination_lng)

    def get_user_mode(self):
        for mode in User_Modes.list():
            if self.modo == mode.value:
                return mode.value

    def get_google_mode(self):
        for mode in Google_Modes.list():
            if self.modo == mode.value:
                return mode.value
