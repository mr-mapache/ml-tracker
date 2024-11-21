from typing import Any
from dataclasses import dataclass

@dataclass
class Module:
    type: str
    hash: str
    name: str
    arguments: dict[str, Any]

    def __eq__(self, value: object) -> bool:
        if not isinstance(value, Module):
            return False
        return self.hash == value.hash
    
    def __hash__(self) -> int:
        return hash(self.hash)