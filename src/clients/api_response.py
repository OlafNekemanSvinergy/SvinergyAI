"""
This file holds all standardized api responses to work with in the analysis module.
"""


class Token:

    def __init__(self, access_token: str, refresh_token: str, valid_until, expires_in: int):
        self.access_token = access_token
        self.refresh_token = refresh_token
        self.valid_until = valid_until
        self.expires_in = expires_in
