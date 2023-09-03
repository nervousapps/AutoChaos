"""
AutoChaos
"""
import os
import json

from auto_chaos.k8s_system import K8sSystem
from auto_chaos.chaos import Chaos


PROMPTS_PATH = os.path.join(os.path.dirname(__file__), "prompts")


def main():
    # load_dotenv(sys.argv[1])


    kuberntes_context = os.getenv("K8S_CTX")
    keyfile = os.getenv("KEYFILE")
    namespace = os.getenv("NAMESPACE")
    availability_route = os.getenv("AVAILABILITY_ROUTE")
    # TODO : take a description file (a json describing the API)
    api_routes = os.getenv("API_ROUTES")
    resource_type = os.getenv("RESOURCE_TYPE")
    model = os.getenv("GPT_VERSION", "gpt-3.5-turbo-16k")

    # Load chaos engineer prompt
    with open(
        os.path.join(
            PROMPTS_PATH,
            "chaos_engineer.txt",
        ),
        "r",
    ) as file:
        system_prompt = file.read()

    # K8s actions
    k8s_system = K8sSystem()

    # Load system description
    system_resources = {
        "system_resources": k8s_system.describe(),
        "api_routes": ["http://localhost/ping", "http://localhost/pong"],
        "availability_route": "http://localhost/ping",
    }

    # Prepare first system and use messages
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": f"{system_resources}"},
    ]

    # It is time to do chaos !
    messages = Chaos(k8s_system).chaos(messages)

    # Write the result file
    with open(
        os.path.join(f"autochaos.json"), "w"
    ) as file:
        file.write(json.dumps(messages, indent=4))


if __name__ == "__main__":
    main()
