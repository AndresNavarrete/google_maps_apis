from dataclasses import dataclass


@dataclass
class RouteResponse:
    meters: float
    seconds: float
    toll_currency: str
    toll_amount: float
    description: str
    instructions: str
    meters_with_tolls: int
