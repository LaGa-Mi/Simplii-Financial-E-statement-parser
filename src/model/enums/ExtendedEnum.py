from enum import Enum

class ExtendedEnum(Enum):
    @classmethod
    def set(cls):
        return set(m.value for m in cls)