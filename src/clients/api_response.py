"""
This file holds all standardized api responses to work with in the analysis module.
"""


class HeatPump:

    def __init__(self, device_id: str, serial_number: str):
        self.device_id = device_id
        self.serial_number = serial_number


class Token:

    def __init__(self, access_token: str, refresh_token: str, valid_until,
                 expires_in: int):
        self.access_token = access_token
        self.refresh_token = refresh_token
        self.valid_until = valid_until
        self.expires_in = expires_in


class HeatPumpData:

    def __init__(self, temp_inside: float, temp_target: float,
                 temp_range: float, temp_outdoor: float, heating_on: bool,
                 power_level: float):
        self.temp_inside: float = temp_inside
        self.temp_target: float = temp_target
        self.temp_range: float = temp_range
        self.temp_outdoor: float = temp_outdoor
        self.heating_on: bool = heating_on
        self.power_level: float = power_level
