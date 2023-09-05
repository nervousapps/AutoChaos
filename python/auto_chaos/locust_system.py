"""
Locust system
"""
import os
import subprocess
import requests
import csv
from locust import HttpUser, task
from auto_chaos.chaos import BaseSystem


class LocustSystem(BaseSystem):
    def __init__(self):
        self.availability_route = os.getenv("AVAILABILITY_ROUTE")
        self.csv_report_names = [
            "_stats.csv"
        ]  # , "_failures.csv", "_exceptions.csv", "_stats_history.csv"]
        super().__init__()

    def stress_api(self, args: list[str] = None) -> str:
        """
        Stress api by running locust

        Args:
            args (list[str], optional): List of arguments to use. Defaults to None.

        Returns:
            _type_: _description_
        """
        if not "http" in args[0]:
            args[0] = "http://localhost:8080" + args[0]
        result = subprocess.run(
            [
                "locust",
                "-f",
                os.path.join(os.path.dirname(__file__), "locust_system.py"),
                "--headless",
                "-u",
                args[1],
                "-r",
                "5",
                "--run-time",
                "5",
                "--host",
                args[0],
                "--csv=stress",
            ],
            stdout=subprocess.PIPE,
        )

        stress_report = []
        for name in self.csv_report_names:
            csv_file = "stress" + name
            with open(csv_file, "r") as my_input_file:
                stress_report += [
                    (" ".join(row) + "\n") for row in csv.reader(my_input_file)
                ]
        self.results.append(str(stress_report))

    def availability_request(self, args: list[str] = None):
        """
        Actions must be defined like that default action

        Args:
            args (list[str], optional): List of arguments to use. Defaults to None.

        Returns:
            _type_: _description_
        """
        response = requests.get(self.availability_route).status_code
        self.results.append(response)


class LocustUser(HttpUser):
    @task
    def stress_api(self):
        self.client.get("")
