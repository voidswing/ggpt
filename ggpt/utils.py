# bulit-in
import os
import subprocess
from typing import Optional

# ggpt
from ggpt.exception import (
    NotGitRepositoryError,
    GitDiffTooLongError,
    NoContentError,
)
from ggpt.const import (
    MAX_DIFF_LENGTH,
)


def is_git_repository(path: str) -> bool:
    """
    Check if the given path is a valid Git repository.

    Args:
        path (str): The path to check.

    Returns:
        bool: True if the path is a valid Git repository, False otherwise.
    """
    git_dir = os.path.join(path, ".git")

    if not (os.path.exists(git_dir) and os.path.isdir(git_dir)):
        return False

    return True


def get_diff(path: str, hash: Optional[str] = None, staged_only: bool = False) -> str:
    """
    Get the diff for the given Git repository based on the options set.

    Args:
        path (str): The path to the Git repository.
        hash (Optional[str]): The Git hash to diff against. If None, diff against HEAD.
        staged_only (bool): If True, only show the diff of staged changes.

    Returns:
        str: The Git diff for the repository.

    Raises:
        NoContentError: If the Git hash does not exist or there are no changes in the diff.
        GitDiffTooLongError: If the length of the Git diff is greater than MAX_DIFF_LENGTH.
    """
    if not is_git_repository(path):
        raise NotGitRepositoryError(path)

    if hash:
        diff_command = ["git", "show", hash]
    else:
        diff_command = ["git", "diff"]

        if staged_only:
            diff_command.append("--cached")

    try:
        result = subprocess.run(diff_command, cwd=path, capture_output=True, check=True, text=True)
        diff = result.stdout
    except subprocess.CalledProcessError:
        raise NoContentError()

    diff = diff.strip()

    if not diff:
        raise NoContentError()

    if len(diff) > MAX_DIFF_LENGTH:
        raise GitDiffTooLongError(len(diff))

    return diff
