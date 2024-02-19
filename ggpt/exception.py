# built-in
from abc import ABC

# ggpt
from ggpt.const import MAX_DIFF_LENGTH, OPENAI_API_KEY_URL


class GGptException(Exception, ABC):
    pass


class NotGitRepositoryError(GGptException):
    def __init__(self, path: str):
        message = (
            f"The path '{path}' is not a valid Git repository.\n\n"
            "Please ensure that you are in a directory that is a Git repository.\n\n\n"
            "Alternatively, you can use the --path option with the correct path to the Git repository.\n\n"
            "\tggpt <COMMAND> --path=<YOUR_GIT_PROJECT_PATH>"
        )
        super().__init__(message)


class NoContentError(GGptException):
    def __init__(self):
        message = "There is no content to request."
        super().__init__(message)


class GitDiffTooLongError(GGptException):
    def __init__(self, diff_length: int):
        message = (
            f"The length of the diff ({diff_length}) is greater than {MAX_DIFF_LENGTH} characters.\n\n"
            f"The request to GPT may fail due to the limit on the amount of text that can be processed.\n\n"
            f"To reduce the size of the diff, you may consider the following options:\n"
            f"- Remove unnecessary or redundant code.\n"
            f"- Refactor the code to reduce the size of the diff.\n"
            f"- Split the changes into smaller and more manageable diff block."
        )
        super().__init__(message)


class APIKeyError(GGptException):
    def __init__(self, command: str):
        message = (
            f"The OpenAI API key is not set. Please set the OPENAI_API_KEY environment variable or use the --api-key option.\n\n\n"
            f"To set the API key using the CLI option, please run the command as follows:\n\n"
            f"\tggpt {command} --api-key <YOUR_API_KEY_HERE>\n\n\n"
            f"To set the API key using an environment variable, please add the following line to your shell profile:\n\n"
            f"\texport OPENAI_API_KEY=<YOUR_API_KEY_HERE>\n\n\n"
            f"To generate a new API key, please visit {OPENAI_API_KEY_URL}"
        )
        super().__init__(message)


class NotImplementedCommandError(GGptException):
    def __init__(self, command: str):
        message = f"Command '{command}' is not implemented."
        super().__init__(message)


class InvalidAPIKeyError(GGptException):
    def __init__(self):
        message = (
            f"The OpenAI API key is invalid. Please check that you have entered a valid API key.\n\n"
            f"To generate a new API key, please visit https://beta.openai.com/account/api-keys"
        )
        super().__init__(message)
