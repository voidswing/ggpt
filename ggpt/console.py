# built-in
import traceback

# rich
from rich.console import Console as RichConsole
from rich.panel import Panel
from rich.spinner import Spinner
from rich.status import Status


class Console:
    def __init__(self):
        """
        Initialize a new instance of the Console class,
        which provides a wrapper around RichConsole for enhanced console output.
        """
        self.console = RichConsole()

    def show_status(self, message: str, spinner: str = "dots") -> Status:
        """
        Displays a status message with an optional spinner animation.

        Args:
            message (str): The message to display.
            spinner (str): The spinner animation to use. Default is "dots".

        Returns:
            An instance of Status, which can be used to update the status message later.
        """
        return self.console.status(message, spinner=spinner)

    def print_panel(self, content: str, title: str = None):
        """
        Displays a panel with optional title.

        Args:
            content (str): The content of the panel.
            title (str): The title of the panel. Default is None.
        """
        self.console.print(Panel(content, title=title))

    def print_error_panel(self, message: str):
        """
        Displays a panel with an error message.

        Args:
            message (str): The error message to display.
        """
        self.console.print(Panel(message, title="Error", border_style="bold red"))

    def print_traceback_panel(self):
        """
        Displays a panel with a traceback for an internal error.
        """
        self.console.print(Panel(traceback.format_exc(), title="Internal Error", border_style="bold red"))
