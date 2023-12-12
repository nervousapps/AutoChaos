<h1 align="center">
AutoChaos
</h1>
<h1 align="center">
<img width="200" style="border-radius: 50%" src="https://raw.githubusercontent.com/nervousapps/AutoChaos/main/logo.png" alt="AutoChaos">
</h1>

:warning: This README reflect the final objective of this project, not the actual state.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![python](https://img.shields.io/badge/Python-3.9-3776AB.svg?style=flat&logo=python&logoColor=white)](https://www.python.org)
[![openai](https://img.shields.io/badge/openai%20-GPT-yellowgreen)](https://www.openai.com)

[![Pylint](https://github.com/nervousapps/AutoChaos/actions/workflows/pylint.yaml/badge.svg)](https://github.com/nervousapps/AutoChaos/actions/workflows/pylint.yaml)
[![Pytest](https://github.com/nervousapps/AutoChaos/actions/workflows/tests.yaml/badge.svg)](https://github.com/nervousapps/AutoChaos/actions/workflows/tests.yaml)
[![Docs](https://github.com/nervousapps/AutoChaos/actions/workflows/pdoc.yaml/badge.svg)](https://nervousapps.github.io/AutoChaos/auto_chaos)


<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->

- [:artificial_satellite: Introduction](#artificial_satellite-introduction)
  - [Purpose](#purpose)
  - [:books: How It Works](#books-how-it-works)
- [:pinched_fingers: Requirements](#pinched_fingers-requirements)
- [:surfing_woman: Installation](#surfing_woman-installation)
- [:unicorn: OpenAI key configuration](#unicorn-openai-key-configuration)
- [:point_right: Quickstart](#point_right-quickstart)
- [:label: Environement variables (config file)](#label-environement-variables-config-file)
- [Implementation details](#implementation-details)
  - [How to add actions](#how-to-add-actions)
- [Results](#results)
- [Conclusion](#conclusion)
- [:roller_coaster: Going further](#roller_coaster-going-further)
- [:carousel_horse: Disclaimers](#carousel_horse-disclaimers)
- [:recycle: Formatter](#recycle-formatter)
- [:ledger: License](#ledger-license)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->


## :artificial_satellite: Introduction
AutoChaos is a powerful tool designed to inject chaos in various systems (kubernetes clusters for now).

### Purpose
The purpose of AutoChaos is to analyze and simulate chaos in systems, helping organizations identify potential vulnerabilities, bottlenecks, and failure points. By subjecting systems to controlled chaos scenarios, businesses can gain valuable insights into their resilience and make informed decisions for improvement.

### :books: How It Works
AutoChaos utilizes LLM to inject controlled chaos into systems. It can simulate various chaotic events, such as sudden spikes in usage, hardware failures, network interruptions, and more. The tool measures the system's response to these chaotic events and provides detailed analysis and visualizations of the system's behavior under stress.

## :pinched_fingers: Requirements

- Python 3.9 or newer (needs of [asyncio.to_thread()](https://docs.python.org/3/library/asyncio-task.html#asyncio.to_thread))
```bash
sudo apt update
sudo apt install python3.xx python3.xx-dev python3.xx-venv
```

- [Open API key](https://platform.openai.com/account/api-keys), or a [LoacalAI](https://localai.io/) instance, or any other GenAI instance compatible with the openAi python package.

## :surfing_woman: Installation
1 - Clone this repository
```bash
git clone https://github.com/nervousapps/AutoChaos.git
```

2 - Go in the repo directory
```bash
cd AutoChaos
```

3 - A python venv is recommended, to create one, in your terminal:
```bash
python3.xx -m venv autochaos
```
And enable it
```bash
source ./autochaos/bin/activate
```

4 - Install AutoChaos package and dependencies by executing:
```bash
pip install -r ./python/requirements.txt
pip install ./python --no-deps
```

## :unicorn: OpenAI key configuration
- Fill openai_key.txt.template with your opanai key and rename it to openai_key.txt. Or create a new one using:
```bash
nano ./openai_key.txt
```

## :point_right: Quickstart
```python
if loacal_ai_url:
    # Change api url to LoacalAi one
    openai.base_url = loacal_ai_url
    openai.api_key = "sx-xxx"
else:
    # Initialize openai api_key
    with open("./openai_key.txt", "r") as file:
        openai.api_key = (file.read()).strip()

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
with open(
    os.path.join(f"autochaos.json"), "w"
) as file:
    file.write(json.dumps(chaos.messages, indent=4))

```


## :label: Environement variables (config file)
| env name                       | description     | default value      |
| -------------------------------| ----------------| -------------------|
| K8S_CTX                        | K8s context                                                       | default   | 
| KEYFILE                        | Path to openai keyfile.txt                                        | ./openai_key.txt|
| NAMESPACE                      | Namespace on which chaos will be applied                    | all  |
| AVAILABILITY_ROUTE                  | Route to check system availability          | None               |
| API_ROUTES    | Routes on which locust system will do load test, must be of form "/foo/hostname /bar/hostname" | ""              |
| LOCAL_AI_URL                    | Url of a local instance of an api compatible with openAi python package                                        | "" |
| MODEL_NAME                    | Model name to use                                        | gpt-3.5-turbo-16k |
| NB_ITERATION                  | Number of chaos iteration                                       | 5 |

## Implementation details
At first, actions are defined in system prompt (chaos_engineer.txt) like the following example :
```text
- DESCRIBE : this action must be used to see the system state during chaos, no arguments required, use it after chaos has begun
- KILL : this action must be used to kill a process, a task, a pod, a node of anything in the system, you have to indicate in this order: the type, the name and the namespace of resource to kill (for example KILL pod kop-123 namespace_1), no talking, no comments
```
LLM (acting as a chaos engineer) will choose one of the defined actions and ask to do it with corresponding arguments, a response can be for example :
```text
KILL pod kop-123 namespace_1
```

Handlers for defined actions must be implemented in systems class that inherit from auto_chaos.chaos.BaseSystem.
This BaseSytem class defines a do_action method that will analyze the chaos engineer response and call the corresponding handler if any, else it will call a defaut handler.

### How to add actions 
- Define a new action in chaos_engineer.txt prompt.
- Add a new handler with the same name (lower case) in a system class inheriting from BaseSystem.


## Results
The AutoChaos tool provides accurate and detailed results on the system's behavior during chaos events. The analysis includes metrics such as response time, error rates, resource utilization, and system stability. Visualizations, such as charts and graphs, are also generated to help visualize the data and identify patterns or anomalies. By analyzing the results, businesses can identify potential weaknesses and take proactive measures to improve the system's resilience and performance.

## Conclusion
AutoChaos is a powerful tool for analyzing chaos in systems, providing businesses with valuable insights into their resilience and vulnerabilities. By simulating chaos events and analyzing the system's response, organizations can make informed decisions and take proactive steps to improve their systems' robustness. Install AutoChaos today and gain a deeper understanding of your systems' behavior under stress.

## :roller_coaster: Going further
- do a report of the initial state of the system
- take an objective (like : I want my system to be able to handle 10000 users)
- take a description file (a json describing the API to automatically guess routes)
- use a client instead of the base openai package one


## :carousel_horse: Disclaimers
This is not an official OpenAI product. This is a personal project and it is not affiliated with OpenAI in any way.

## :recycle: Formatter

[BLACK](https://pypi.org/project/black/)

## :ledger: License
[License MIT](./LICENSE)