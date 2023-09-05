"""
AutoChaos
"""
import os
import sys
import json
from dotenv import load_dotenv
from gevent import monkey

monkey.patch_all()

from auto_chaos.k8s_system import K8sSystem
from auto_chaos.locust_system import LocustSystem
from auto_chaos.chaos import Chaos


def main():
    load_dotenv(sys.argv[1])

    kuberntes_context = os.getenv("K8S_CTX")
    namespace = os.getenv("NAMESPACE")
    availability_route = os.getenv("AVAILABILITY_ROUTE")
    # TODO : take a description file (a json describing the API)
    api_routes = os.getenv("API_ROUTES", "").split(" ")
    resource_type = os.getenv("RESOURCE_TYPE")
    model = os.getenv("GPT_VERSION", "gpt-3.5-turbo-16k")

    # Systems
    k8s_system = K8sSystem(namespace)
    locust_system = LocustSystem()

    # Load system description
    initial_state = {
        "system_resources": k8s_system.describe(),
        "api_routes": api_routes,
        "availability_route": availability_route,
    }

    # It is time to do chaos !
    chaos = Chaos([k8s_system, locust_system], initial_state)
    chaos.chaos(objective=10)
    chaos.report()

    # Write the result file
    with open(os.path.join(f"autochaos.json"), "w") as file:
        file.write(json.dumps(chaos.messages, indent=4))


if __name__ == "__main__":
    main()
