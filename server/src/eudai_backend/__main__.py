"""Command-line interface."""
import click


@click.command()
@click.version_option()
def main() -> None:
    """eudai-backend."""


if __name__ == "__main__":
    main(prog_name="eudai-backend")  # pragma: no cover
