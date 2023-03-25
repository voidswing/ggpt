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
    DEFAULT_MAX_TOKEN,
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


def get_git_diff_result(path: str, cached_only: bool = False) -> Optional[str]:
    """
    Get the Git diff for the given Git repository path.

    Args:
        path (str): The path to the Git repository.
        cached_only (bool): True to show the diff of the staged changes, False to show the diff of unstaged changes.

    Returns:
        Optional[str]: The Git diff for the repository, or None if an error occurred.
    """
    if not is_git_repository(path):
        raise NotGitRepositoryError(path)

    diff_command = ["git", "diff"]
    if cached_only:
        diff_command.append("--cached")

    try:
        result = subprocess.run(diff_command, cwd=path, capture_output=True, check=True, text=True)
        return result.stdout
    except subprocess.CalledProcessError:
        return None


def get_git_show_result(path: str, git_hash: Optional[str]) -> Optional[str]:
    """
    Get the result of `git show {git_hash}` for the given Git repository path.

    Args:
        path (str): The path to the Git repository.
        git_hash (Optional[str]): The hash of the commit to show. If None, show the result of `git show HEAD`.

    Returns:
        Optional[str]: The result of `git show {git_hash}` for the repository, or None if an error occurred.
    """
    if not is_git_repository(path):
        raise NotGitRepositoryError(path)

    git_command = ["git", "show"]
    if git_hash:
        git_command.append(git_hash)
    else:
        git_command.append("HEAD")

    try:
        result = subprocess.run(git_command, cwd=path, capture_output=True, check=True, text=True)
        return result.stdout
    except subprocess.CalledProcessError:
        import traceback

        traceback.print_exc()
        return None


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
