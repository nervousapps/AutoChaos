"""
Chaos module
"""
import openai

from auto_chaos.gpt_utils import generate_text


class BaseSystem:
    def __init__(self) -> None:
        pass

    def do_action(self, data):
        pass

class Chaos:
    def __init__(self, system: BaseSystem) -> None:
        # Initialize openai api_key
        with open("./openai_key.txt", "r") as file:
            openai.api_key = (file.read()).strip()
        self.system = system

    def chaos(self, messages, index = 0):
        print(f"Chaos {index}")
        if index > 11:
            return messages
        # if index == 11:
        #     messages.append({"role": "user", "content": f"REPORT"})
        response = generate_text(
            messages, model="gpt-3.5-turbo-16k", temperature=1
        )

        response = response.choices[0].message.content
        messages.append({"role": "assistant", "content": response})

        print(f"Doing {response}")
        messages.append({"role": "user", "content": f"{self.system.do_action(response)}"})
        messages = self.chaos(messages, index+1)

        return messages