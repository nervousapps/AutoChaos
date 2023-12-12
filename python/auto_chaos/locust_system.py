"""
🦞
Locust system
🦞
"""
import os
import subprocess
import requests
import csv
from locust import HttpUser, task
from auto_chaos.base_system import BaseSystem


class LocustSystem(BaseSystem):
    """
    Locust system
    """

    SPAWN_RATE = "5"
    RUN_TIME = "5"

    def __init__(self):
        """
        Init
        """
        self.availability_route = os.getenv("AVAILABILITY_ROUTE")
        self.csv_report_names = [
            "_stats.csv"
        ]  # , "_failures.csv", "_exceptions.csv", "_stats_history.csv"]
        super().__init__()

    def stress_api(self, args: list[str] = None):
        """
        Stress api by running locust

        Args:
            args (list[str], optional): List of arguments to use. Defaults to None.
        """
        if not "http" in args[0]:
            args[0] = "http://localhost:8080" + args[0]

        # Run locust
        result = subprocess.run(
            [
                "locust",
                "-f",
                os.path.join(os.path.dirname(__file__), "locust_system.py"),
                "--headless",
                "-u",
                args[1],
                "--spawn-rate",
                self.SPAWN_RATE,
                "--run-time",
                self.RUN_TIME,
                "--host",
                args[0],
                "--csv=stress",
            ],
            # stdout=subprocess.PIPE,
        )

        # Get CSV reports
        stress_report = []
        for name in self.csv_report_names:
            csv_file = "stress" + name
            with open(csv_file, "r") as my_input_file:
                stress_report += [
                    (" ".join(row) + "\n") for row in csv.reader(my_input_file)
                ]
        # Add the result to results
        self.results.append(str(stress_report))


class LocustUser(HttpUser):
    """
    A simple locust user
    """

    @task
    def stress_api(self):
        """
        Request on the url given at locust starting
        """
        self.client.get("")
