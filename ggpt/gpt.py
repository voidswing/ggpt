# built-in
import re
from typing import Optional

# opneai
import openai

# ggpt
from ggpt.exception import InvalidAPIKeyError


class GPTClient:
    def __init__(self, api_key: str):
        """
        Constructor for the GPTClient class.

        Args:
            api_key (str): The API key to use for the OpenAI API.
        """
        self.api_key = api_key
        openai.api_key = self.api_key

    def request(self, prompt: str):
        """
        Sends a request to the OpenAI API.

        Args:
            prompt (str): The prompt to send to the API.

        Returns:
            The response from the API.

        Raises:
            InvalidAPIKeyError: If the OpenAI API key is invalid or not set.
        """
        messages = [
            {
                "role": "user",
                "content": prompt,
            }
        ]

        try:
            response = openai.chat.completions.create(
                model="gpt-4-1106-preview",
                messages=messages,
                temperature=0.3,
                frequency_penalty=0.0,
                presence_penalty=0.0,
            )

            return response
        except openai.AuthenticationError:
            raise InvalidAPIKeyError()

    def request_review(self, diff: str) -> str:
        """
        Sends a request to the OpenAI API to generate a code review based on a Git diff.

        Args:
            diff (str): The Git diff to generate a code review for.

        Returns:
            The generated code review.
        """
        prompt = (
            "As an experienced software developer, please provide a detailed and actionable code review for the following code changes.\n"
            "Consider the following aspects in your review:\n"
            "- Code correctness and potential bugs\n"
            "- Code readability and maintainability\n"
            "- Code efficiency and performance\n"
            "- Code modularity and organization\n"
            "- Compliance with best practices and coding standards\n"
            "Anything that starts with + is added, and anything that starts with - is removed.\n"
            "The code changes you need to review are as follows:\n"
            "==========BEGIN==========\n"
            f"{diff}"
            "==========END==========\n"
            "If there's nothing to feedback, just tell me 'Looks good to me'. "
            "If there is something you want to point out, start and only use ordinal expressions, like "
            "1. ~~~~\n2. ~~~~\n3. ~~~~\n... and so on.\n"
        )

        response = self.request(prompt=prompt)

        finish_text = response.choices[0].message.content
        finish_text = re.sub(r"(?<!\n)\n(?!\n)", "\n\n", finish_text)

        return finish_text

    def request_docstring(self, diff: str) -> str:
        """
        Generates a docstring for code changes specified by the `diff` argument
        using OpenAI's GPT API.

        Args:
            diff (str): The Git diff to generate a docstring for.

        Returns:
            str: The generated docstring text from the GPT-3 API.
        """
        prompt = (
            "Please generate comprehensive, detailed, and accurate docstrings for every function or class that needs one. "
            "Your docstring should include the following information when applicable:\n"
            "- Function or class purpose\n"
            "- Description of input parameters (name, type, purpose)\n"
            "- Description of return values (type, purpose)\n"
            "- Description of exceptions raised\n"
            "- Any other relevant information\n\n"
            "Detect the programming language used in the code diff and format the docstrings accordingly.\n"
            "The code diff looks like:\n"
            "==========BEGIN==========\n"
            f"{diff}"
            "==========END==========\n"
        )

        response = self.request(prompt=prompt)

        finish_text = response.choices[0].message.content

        return finish_text

    def request_naming(self, user_prompt: str) -> str:
        """
        Generates a variable name suggestion for the user-provided prompt
        using OpenAI's GPT API.

        Args:
            user_prompt (str): The prompt to generate a variable name for.

        Returns:
            str: The generated variable name suggestion from the GPT-3 API.
        """
        prompt = (
            f"Based on the description '{user_prompt}', please suggest a meaningful and descriptive variable name that adheres to commonly used naming conventions in programming. "
            "Provide the variable name in the following formats:\n"
            "- camelCase\n"
            "- PascalCase\n"
            "- snake_case\n"
            "- BIG_SNAKE_CASE\n"
        )
        response = self.request(prompt=prompt)

        finish_text = response.choices[0].message.content
        finish_text = re.sub(r"(?<!\n)\n(?!\n)", "\n\n", finish_text)

        return finish_text
