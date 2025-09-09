from enum import StrEnum, auto



class Step(StrEnum):
    send_code = auto()
    validate_code = auto()
    validate_password = auto()
    final = auto()
