<h1 align="center">
AutoChaos
</h1>
<h1 align="center">
<img width="200" src="https://raw.githubusercontent.com/nervousapps/AutoChaos/master/logo.png" alt="AutoChaos">
</h1>

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![python](https://img.shields.io/badge/Python-3.9-3776AB.svg?style=flat&logo=python&logoColor=white)](https://www.python.org)
[![openai](https://img.shields.io/badge/openai%20-GPT-yellowgreen)](https://www.openai.com)


<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->
**Table of Contents**  *generated with [DocToc](https://github.com/thlorenz/doctoc)*

- [Introduction](#introduction)
- [Purpose](#purpose)
- [How It Works](#how-it-works)
- [:pinched_fingers: Requirements](#pinched_fingers-requirements)
- [:surfing_woman: Installation](#surfing_woman-installation)
- [:unicorn: OpenAI key configuration](#unicorn-openai-key-configuration)
- [Usage](#usage)
- [Results](#results)
- [Conclusion](#conclusion)
- [:carousel_horse: Disclaimers](#carousel_horse-disclaimers)
- [:ledger: License](#ledger-license)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->


## Introduction
AutoChaos is a powerful tool designed to inject chaos in various systems (kubernetes clusters for now), helping businesses identify and mitigate potential vulnerabilities and weaknesses. 
This README.md file will provide an overview of the AutoChaos tool, its purpose, functionality, installation instructions, and usage guidelines.

## Purpose
The purpose of AutoChaos is to analyze and simulate chaos in systems, helping organizations identify potential vulnerabilities, bottlenecks, and failure points. By subjecting systems to controlled chaos scenarios, businesses can gain valuable insights into their resilience and make informed decisions for improvement.

## How It Works
AutoChaos utilizes advanced algorithms and simulation techniques to inject controlled chaos into systems. It can simulate various chaotic events, such as sudden spikes in usage, hardware failures, network interruptions, and more. The tool measures the system's response to these chaotic events and provides detailed analysis and visualizations of the system's behavior under stress.

## :pinched_fingers: Requirements

- Python 3.9 or newer (needs of [asyncio.to_thread()](https://docs.python.org/3/library/asyncio-task.html#asyncio.to_thread))

- [Open API key](https://platform.openai.com/account/api-keys)

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
python3 -m venv autochaos
```
And enable it
```bash
source ./autochaos/bin/activate
```

4 - Install GPTenterprise package and dependencies by executing:
```bash
pip install ./python
```

## :unicorn: OpenAI key configuration
- Fill openai_key.txt.template with your opanai key and rename it to openai_key.txt. Or create a new one using:
```bash
nano ./openai_key.txt
```

## Usage
Once AutoChaos is installed, you can use it by following these steps:
1. Launch the AutoChaos application.
2. Select the system or process you want to analyze from the dropdown menu.
3. Choose the type of chaos event you want to simulate.
4. Set the parameters for the chaos event, such as duration, intensity, and frequency.
5. Click the \"Start\" button to initiate the chaos simulation.
6. Monitor the system's behavior and collect data during the chaos event.
7. View the analysis and visualizations provided by AutoChaos to gain insights into the system's resilience and performance under stress.
8. Take appropriate actions based on the analysis to improve the system's robustness.
## Results
The AutoChaos tool provides accurate and detailed results on the system's behavior during chaos events. The analysis includes metrics such as response time, error rates, resource utilization, and system stability. Visualizations, such as charts and graphs, are also generated to help visualize the data and identify patterns or anomalies. By analyzing the results, businesses can identify potential weaknesses and take proactive measures to improve the system's resilience and performance.
## Conclusion
AutoChaos is a powerful tool for analyzing chaos in systems, providing businesses with valuable insights into their resilience and vulnerabilities. By simulating chaos events and analyzing the system's response, organizations can make informed decisions and take proactive steps to improve their systems' robustness. Install AutoChaos today and gain a deeper understanding of your systems' behavior under stress.


## :carousel_horse: Disclaimers
This is not an official OpenAI product. This is a personal project and it is not affiliated with OpenAI in any way.

## :ledger: License
[License MIT](./LICENSE)