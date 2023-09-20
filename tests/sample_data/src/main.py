from .config_handler import ConfigHandler
from .file_processor import FileProcessor
from .project_summary import ProjectSummary
from .logger_config import configure_logging
import click


@click.group()
def cli():
    pass


@cli.command()
@click.option("--config", default="config.ini", help="Path to the configuration file.")
@click.option(
    "--directory", required=True, help="Directory to generate file list from."
)
@click.option(
    "--output", default="file_list.json", help="Output file for generated file list."
)
def generate(config, directory, output):
    configure_logging()
    config_handler = ConfigHandler(config)
    processor = FileProcessor(config_handler)
    processor.generate_file_list(directory, output)


@cli.command()
@click.option(
    "--file-list",
    required=True,
    type=click.Path(exists=True),
    help="File list generated in previous phase.",
)
def analyze(file_list):
    config_handler = ConfigHandler()
    processor = FileProcessor(config_handler)
    processor.analyze_from_list(file_list)


if __name__ == "__main__":
    cli()
