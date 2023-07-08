from abc import ABC
from dataclasses import dataclass


@dataclass
class BaseClient(ABC):
    api_key: str
