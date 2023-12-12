"""
\U0001F9E0
GPT utils
\U0001F9E0
"""
import os
import openai
from typing import List, Generator


def generate_text(
    messages: List[str], temperature: float, model: str = os.getenv("MODEL_NAME")
) -> Generator:
    """
    Generate text from a list of messages relying on OpenAI compatible API.

    Args:
        messages (List[str]): List of messages (system, user, assistant)
        model (str): LLM model to be used
        temperature (float): Temperature

    Returns:
        Generator: GPT response object
    """
    response = openai.chat.completions.create(
        model=model,
        messages=messages,
        temperature=temperature,
        max_tokens=6742,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
    )

    return response
