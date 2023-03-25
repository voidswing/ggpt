# click
import click

# ggpt
from ggpt.ggpt import GGPT


@click.group()
def cli():
    pass


@cli.command()
@click.option("--api-key", type=str, help="OpenAI API Key.")
@click.option("--path", type=str, help="Path to the Git repository to be used for the command.")
@click.option("--hash", type=str, help="Include specific hash value of the commit.")
@click.option("--staged", is_flag=True, help="Include only staged changes.")
def review(api_key=None, path=None, hash=None, staged=False):
    if hash and staged:
        raise click.UsageError("Only one of --hash, --staged can be set.")

    ggpt = GGPT(
        command="review",
        api_key=api_key,
        path=path,
        hash=hash,
        staged_only=staged,
    )

    ggpt.run()


@cli.command()
@click.option("--api-key", type=str, help="OpenAI API Key")
@click.option("--path", type=str, help="Path to the Git repository to be used for the command.")
@click.option("--hash", type=str, help="Include specific hash value of the commit.")
@click.option("--staged", is_flag=True, help="Include only staged changes.")
def docstring(api_key=None, path=None, hash=None, staged=False):
    if hash and staged:
        raise click.UsageError("Only one of --hash, --staged can be set.")

    ggpt = GGPT(
        command="docstring",
        hash=hash,
        api_key=api_key,
        staged_only=staged,
    )

    ggpt.run()


@cli.command()
@click.argument("prompt", type=str)
@click.option("--api-key", type=str, help="OpenAI API Key")
def naming(prompt: str, api_key=None):
    ggpt = GGPT(
        command="naming",
        api_key=api_key,
        user_prompt=prompt,
    )

    ggpt.run()


if __name__ == "__main__":
    cli()
