"""
🛠️
Utility system
🛠️
"""
import os
import requests

from auto_chaos.base_system import BaseSystem


class UtilitySystem(BaseSystem):
    """
    Utility system
    """

    def __init__(self):
        """
        Init
        """
        self.availability_route = os.getenv("AVAILABILITY_ROUTE")
        super().__init__()

    def availability_request(self, args: list[str] = None):
        """
        Test availability route

        Args:
            args (list[str], optional): List of arguments to use. Defaults to None.
        """
        response = requests.get(self.availability_route).status_code
        self.results.append(response)
