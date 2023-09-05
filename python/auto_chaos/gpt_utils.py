"""
\U0001F9E0
GPT utils
\U0001F9E0
"""
import openai
from typing import List, Generator


def generate_text(messages: List[str], model: str, temperature: float) -> Generator:
    """


    Args:
        messages (List[str]): List of messages (system, user, assistant)
        model (str): OpenAI model to be used
        temperature (float): Temperature

    Returns:
        Generator: GPT response object
    """
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=temperature,
        max_tokens=6742,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
    )

    return response
