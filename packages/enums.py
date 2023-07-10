from enum import Enum


class ExtendedEnum(Enum):
    @classmethod
    def list(cls):
        return list(map(lambda c: c.value, cls))

    @classmethod
    def string_list(cls):
        return ",".join(cls.list())


class Google_Modes(ExtendedEnum):
    car = "driving"
    transit = "transit"
    bus = "bus"
    walk = "walking"


class User_Modes(ExtendedEnum):
    car = "auto"
    transit = "tp"
    bus = "bus"
    walk = "caminata"


class Field_Masks(ExtendedEnum):
    route_duration = "routes.duration"
    route_meters = "routes.distanceMeters"
    route_tolls = "routes.travelAdvisory.tollInfo"
