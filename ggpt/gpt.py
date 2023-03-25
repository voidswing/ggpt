# built-in
import re
from typing import Optional

# opneai
import openai

# ggpt
from ggpt.const import (
    CHARACTERS_PER_TOKEN,
    OPENAI_API_MAX_TOKENS,
)


class GPTClient:
    def __init__(self, api_key: str):
        """
        Constructor for the GPTClient class.

        Args:
            api_key (str): The API key to use for the OpenAI API.
        """
        self.api_key = api_key

    def get_max_tokens(self, prompt: str, max_token_limit: int = OPENAI_API_MAX_TOKENS) -> int:
        """
        Calculate the maximum number of tokens to send in an OpenAI API request.

        Args:
            prompt (str): The prompt string to calculate the maximum number of tokens for.
            max_token_limit (int): The maximum number of tokens allowed per API request. Default is 4076.

        Returns:
            int: The maximum number of tokens to send in an OpenAI API request.
        """

        prompt_tokens = int(len(prompt) // CHARACTERS_PER_TOKEN)
        max_tokens = max_token_limit - prompt_tokens

        return max_tokens

    def request(self, prompt: str, max_tokens: int):
        """
        Sends a request to the OpenAI API.

        Args:
            prompt (str): The prompt to send to the API.
            max_tokens (int): The maximum number of tokens to generate in the response.

        Returns:
            The response from the API.
        """
        return openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=max_tokens,
            temperature=0.7,
            frequency_penalty=0.0,
            presence_penalty=0.0,
        )

    def request_review(self, diff: str) -> str:
        """
        Sends a request to the OpenAI API to generate a code review based on a Git diff.

        Args:
            diff (str): The Git diff to generate a code review for.

        Returns:
            The generated code review.
        """
        openai.api_key = self.api_key

        prompt = (
            "You're going to act as a code reviewer from now on. "
            "As a code reviewer, please check the following:\n"
            "- Are there any bugs?\n"
            "- Are there any typos?\n"
            "- Is there code that is not readable or that severely violates code conventions?\n"
            "- Is there a way to structurally or fundamentally improve the code?\n"
            "Anything that starts with + is added, and anything that starts with - is removed.\n"
            "The code changes you need to review are as follows.\n"
            "==========BEGIN==========\n"
            f"{diff}"
            "==========END==========\n"
            "If there's nothing to feedback, just tell me 'Looks good to me'"
            "If there is something you want to point out, start and only use ordinal expressions, like\n"
            "1. ~~~~\n2. ~~~~\n3. ~~~~\n... and so on  \n"
        )

        max_tokens = self.get_max_tokens(prompt)

        response = self.request(prompt=prompt, max_tokens=max_tokens)

        finish_text = response.choices[0].text.strip()
        finish_reason = response.choices[0]["finish_reason"]

        finish_text = re.sub(r"(?<!\n)\n(?!\n)", "\n\n", finish_text)

        return finish_text
