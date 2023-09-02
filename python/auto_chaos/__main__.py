"""
AutoChaos
"""
import os
import sys
import asyncio
import json

from enum import Enum, auto
from functools import partial
from dotenv import load_dotenv

import openai
from kubernetes import client, config

from auto_chaos.gpt_utils import generate_text

PROMPTS_PATH = os.path.join(os.path.dirname(__file__), "prompts")

# Initialize openai api_key
with open("./openai_key.txt", "r") as file:
    openai.api_key = (file.read()).strip()


# Configs can be set in Configuration class directly or using helper utility
config.load_kube_config()
v1 = client.CoreV1Api()


def describe(message=None):
    result = {"pods": {}, "services": {}, "node": {}}

    print("Listing nodes:")
    ret = v1.list_node()
    for node in ret.items:
        result["node"][node.metadata.name] = {
            "ip": node.status.addresses[0].address
        }
        print("%s" % (node.metadata.name))

    print("Listing pods:")
    ret = v1.list_pod_for_all_namespaces(watch=False)
    for i in ret.items:
        result["pods"][i.metadata.name] = {
            "ip": i.status.pod_ip,
            "namespace": i.metadata.namespace,
            "name": i.metadata.name,
        }
        print("%s\t%s\t%s" % (i.status.pod_ip, i.metadata.namespace, i.metadata.name))
    
    print("Listing services:")
    for namespace in v1.list_namespace().items:
        ret = v1.list_namespaced_service(namespace=namespace.metadata.name, watch=False)
        for i in ret.items:
            result["services"][i.metadata.name] = {
                "name": i.metadata.name,
            }
            print("%s" % (i.metadata.name))
    return result


def availability_request(message):
    return 200


def kill(message):
    resource_type = message.split()[1]
    resource_name = message.split()[2]
    namespace = message.split()[3]

    if resource_type == "pod":
        v1.delete_namespaced_pod(
            name=resource_name,
            namespace=namespace,
        )
    if resource_type == "service":
        v1.delete_namespaced_service(
            name=resource_name,
            namespace=namespace,
        )
    if resource_type == "node":
        v1.delete_node(
            name=resource_name,
        )
    return 200


def stress_api(message):
    return [200, 400, 404, 500, 200, 400]


class Actions(Enum):
    DESCRIBE = partial(describe)
    AVAILABILITY_REQUEST = partial(availability_request)
    KILL = partial(kill)
    STRESS_API = partial(stress_api)


def chaos(messages, index = 0):
    if index > 11:
        return messages
    # if index == 11:
    #     messages.append({"role": "user", "content": f"REPORT"})
    response = generate_text(
        messages, model="gpt-3.5-turbo-16k", temperature=1
    )

    print(json.dumps(response.choices[0].message.content, indent=4))

    # if response.choices[0].message.content == messages[-1]["content"]:
    #     messages.append({"role": "user", "content": "Try something else, the system is still available !"})
    #     return messages
    messages.append({"role": "assistant", "content": response.choices[0].message.content})

    # no_action = False
    for action in Actions:
        if action.name in response.choices[0].message.content:
            print(f"Doing {action.name}")
            messages.append({"role": "user", "content": f"{action.value(response.choices[0].message.content)}"})
            messages = chaos(messages, index+1)
            break
        # else:
        #     no_action = True
        #     continue
    # if no_action:
    #     messages.append({"role": "user", "content": "Try something else, the system is still available ! What actions do you want to do ?"})
    #     messages = chaos(messages, index+1)
    return messages

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

    # Load system description
    system_description = {
        "resources": Actions.DESCRIBE.value(),
        "api_routes": ["http://localhost/ping", "http://localhost/pong"],
        "availability_route": "http://localhost/ping",
    }

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": f"{system_description}"},
    ]

    messages = chaos(messages)

    # Write the result file
    with open(
        os.path.join(f"autochaos.json"), "w"
    ) as file:
        file.write(json.dumps(messages, indent=4))


if __name__ == "__main__":
    main()
