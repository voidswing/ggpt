# built-in
import os
from typing import Optional
from dataclasses import dataclass

# ggpt
from ggpt.console import Console
from ggpt.gpt import GPTClient
from ggpt.const import (
    DEFAULT_MAX_TOKEN,
    MAX_DIFF_LENGTH,
)
from ggpt.utils import get_diff
from ggpt.exception import (
    GGptException,
    APIKeyError,
    NoContentError,
    NotImplementedCommandError,
)


@dataclass
class GGPT:
    hash: Optional[str] = None
    staged_only: bool = False
    api_key: Optional[str] = None
    path: str = None
    command: str = None
    user_prompt: str = None
    console: Console = Console()
    max_token: int = DEFAULT_MAX_TOKEN

    def __post_init__(self):
        """
        Initializes a new instance of the GGPT class and sets up the GPTClient instance.
        """
        self.set_path()
        self.set_api_key()

        self.gpt_client = GPTClient(api_key=self.api_key)

    def set_path(self):
        """
        Sets the path for the GGPT instance, if it is not already set.
        """
        if self.path is None:
            self.path = os.getcwd()

    def set_api_key(self):
        """
        Sets the OpenAI API key for the GGPT instance.
        If an API key is already set, this method does nothing.

        Raises:
            APIKeyError: If the API key is not set, either through an environment
            variable or the --api-key CLI option. Provides instructions for setting
            the API key through either method.
        """
        if self.api_key is None:
            self.api_key = os.getenv("OPENAI_API_KEY")

        if self.api_key is None:
            raise APIKeyError(self.command)

    def run(self):
        """
        Runs the GGPT command specified by the `command` attribute and displays the response.
        """
        try:
            command = getattr(self, f"run_{self.command.upper()}", None)
            if command is None:
                raise NotImplementedCommandError(self.command)

            with self.console.show_status("[cyan]Waiting for GPT response..."):
                response = command()

            self.console.print_panel(response, title="[bold blue]Response[/bold blue]")

        except GGptException as e:
            self.console.print_error_panel(str(e))
        except:
            self.console.print_traceback_panel()

    def run_REVIEW(self) -> str:
        """
        Requests a review from OpenAI's GPT API for the Git diff between the current repository

        Returns:
            str: The generated review text from the GPT API.
        """
        diff = get_diff(self.path, self.hash, self.staged_only)
        return self.gpt_client.request_review(diff)

    def run_DOCSTRING(self):
        """
        Requests a docstring generation from OpenAI's GPT API for the Git diff between the current
        repository state and the specified commit hash or staged files.

        Returns:
            str: The generated docstring text from the GPT API.
        """
        diff = get_diff(self.path, self.hash, self.staged_only)
        return self.gpt_client.request_docstring(diff)

    def run_NAMING(self):
        """
        Generates variable name suggestions for a user-provided prompt using OpenAI's GPT API.

        Raises:
            NoContentError: If the user prompt is empty or contains only whitespace.

        Returns:
            str: The generated variable name suggestion from the GPT API.
        """
        user_prompt = self.user_prompt.strip()
        if not user_prompt:
            raise NoContentError()

        return self.gpt_client.request_naming(self.user_prompt)
