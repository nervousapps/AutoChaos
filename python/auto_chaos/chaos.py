"""
Chaos module
"""
import os
import openai
import asyncio

from auto_chaos.gpt_utils import generate_text

PROMPTS_PATH = os.path.join(os.path.dirname(__file__), "prompts")


class BaseSystem:
    def __init__(self) -> None:
        self.results = []
        self.errors = []

    def do_action(self, data: str):
        """
        Do the action defined in data.

        Args:
            data (str): KILL pod kop-123 namespace_1
        """
        self.results = []
        self.errors = []
        all_tasks = []
        # Parse the string and get the action
        if "," in data:
            datas = data.split(",")
        else:
            datas = [data]
        for data in datas:
            if data[0] == " ":
                data = data[1:]
            try:
                all_tasks.append(
                    asyncio.to_thread(
                        getattr(self, data.split(" ")[0].lower()), data.split(" ")[1:]
                    )
                )
            except AttributeError:
                pass
            except Exception as error:
                self.errors.append(error)
        asyncio.get_event_loop().run_until_complete(asyncio.gather(*all_tasks))
        return self.results, self.errors

    def default_action(self, args: list[str] = None):
        """
        Actions must be defined like that default action

        Args:
            args (list[str], optional): List of arguments to use. Defaults to None.

        Returns:
            _type_: _description_
        """
        pass
        # print("Not implemented")


class Chaos:
    def __init__(self, systems: list[BaseSystem], initial_state: dict) -> None:
        # Initialize openai api_key
        with open("./openai_key.txt", "r") as file:
            openai.api_key = (file.read()).strip()

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

        self.systems = systems

    def chaos(self, objective=5) -> None:
        """
        Do chaos

        Args:
            objective (int, optional): Number of chaos iteration. Defaults to 5.

        Returns:
            list[dict]: _description_
        """
        print(f"Chaos {objective}")
        if objective < 0:
            return

        response = None
        while not response:
            response = generate_text(
                self.messages, model="gpt-3.5-turbo-16k", temperature=1
            )
            response = response.choices[0].message
        self.messages.append(response)

        print(f"Doing {response.content}")
        system_result = []
        system_error = []
        for system in self.systems:
            result, error = system.do_action(response.content)
            system_result += result
            system_error += error
        if system_result or system_error:
            self.messages.append(
                {
                    "role": "user",
                    "content": f"Result : {system_result}, Error: {system_error}",
                }
            )
        self.chaos(objective - 1)

    def report(self):
        """
        Do a report of the chaos
        """
        report = []
        for system in self.systems:
            system_description = f"{system.do_action('DESCRIBE')}"

        # Load chaos report prompt
        with open(
            os.path.join(
                PROMPTS_PATH,
                "chaos_report.txt",
            ),
            "r",
        ) as file:
            system_prompt = file.read()

        report_prompt = "Here are the results of chaos actions:"
        for message in self.messages:
            report_prompt += f" {message['content']}"
        report.append({"role": "system", "content": system_prompt})
        report.append({"role": "user", "content": report_prompt})
        response = generate_text(report, model="gpt-3.5-turbo-16k", temperature=1.4)

        response = response.choices[0].message.content
        self.messages.append({"role": "assistant", "content": response})
