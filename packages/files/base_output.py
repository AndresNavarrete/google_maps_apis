from abc import ABC
from dataclasses import dataclass


@dataclass
class BaseOutput(ABC):
    output_path: str
