"""
🦹🏼‍♂️
Chaos module
🦹🏼‍♂️
"""
import os
import pprint

from openai.types.chat import ChatCompletionMessage

from auto_chaos.gpt_utils import generate_text
from auto_chaos.base_system import BaseSystem
from auto_chaos.utility_system import UtilitySystem

PROMPTS_PATH = os.path.join(os.path.dirname(__file__), "prompts")


class Chaos:
    """
    Here the chaos happen !
    """

    def __init__(self, systems: list[BaseSystem], initial_state: dict) -> None:
        # Load chaos engineer prompt
        with open(
            os.path.join(
                PROMPTS_PATH,
                "chaos_engineer.txt",
            ),
            "r",
        ) as file:
            self.system_prompt = file.read()

        # Prepare first system and use messages
        self.messages = [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": f"{initial_state}"},
        ]

        # Prepare systems
        self.systems = systems
        self.systems.append(UtilitySystem())

    def chaos(self, objective=5) -> None:
        """
        Do chaos

        Args:
            objective (int, optional): Number of chaos iteration. Defaults to 5.
        """
        # This is the end of the chaos
        if objective < 0:
            return

        # Let the chaos engineer do his things and give actions to be done
        response = None
        while not response:
            response = generate_text(
                self.messages,
                model=os.getenv("MODEL_NAME", "gpt-3.5-turbo-16k"),
                temperature=1,
            )
            response = response.choices[0].message
        self.messages.append(response.dict())

        # Do actions in all systems
        print(f"🦹🏼‍♂️ Doing {response.content}")
        system_result = []
        system_error = []
        for system in self.systems:
            result, error = system.do_action(response.content)
            system_result += result
            system_error += error

        # Add the result to messages for the chaos engineer
        if system_result or system_error:
            self.messages.append(
                {
                    "role": "user",
                    "content": f"Result : {system_result}"
                    + (f", Error: {system_error}" if system_error else ""),
                }
            )

        # Do chaos again
        self.chaos(objective - 1)

    def report(self):
        """
        Do a report of the chaos
        """
        print(f"🦹🏼‍♂️ Doing report, please wait ...")
        report = []

        # Do a description of all systems
        # for system in self.systems:
        #    system_description = f"{system.do_action('DESCRIBE')}"

        # Load chaos report prompt
        with open(
            os.path.join(
                PROMPTS_PATH,
                "chaos_report.txt",
            ),
            "r",
        ) as file:
            system_prompt = file.read()
        report.append({"role": "system", "content": system_prompt})

        # Give chaos engineer all previous actions result
        report_prompt = "Here are the results of chaos actions:"
        for message in self.messages:
            if isinstance(message, ChatCompletionMessage):
                report_prompt += f" {message.content}"
                continue
            report_prompt += f" {message['content']}"
        report.append({"role": "user", "content": report_prompt})

        # Ask chaos engineer to do a report of the chaos
        response = generate_text(
            report, model=os.getenv("MODEL_NAME", "gpt-3.5-turbo-16k"), temperature=1.4
        )

        # Add chaos report to messages
        self.messages.append(
            {"role": "assistant", "content": response.choices[0].message.content}
        )

        pp = pprint.PrettyPrinter(indent=4)
        pp.pprint(response.choices[0].message.content)
