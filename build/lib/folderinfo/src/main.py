from folderinfo.src.config_handler import ConfigHandler
from folderinfo.src.file_processor import FileProcessor
from folderinfo.src.project_summary import ProjectSummary
from folderinfo.src.logger_config import configure_logging
import click
import json


@click.group()
def cli():
    """Main CLI group for folderinfo."""
    pass


@cli.command()
@click.option("--config", default="config.ini", help="Path to the configuration file.")
@click.option(
    "--directory", required=True, help="Directory to generate file list from."
)
@click.option(
    "--output", default="file_list.json", help="Output file for generated file list."
)
@click.option("--lines-to-read", type=int, help="Number of lines to read from a file.")
@click.option(
    "--file-types", type=str, help="File types to include in the list. Comma-separated."
)
def generate(config, directory, output, lines_to_read, file_types):
    """Generate a file list based on the provided directory and config."""
    configure_logging()
    config_handler = ConfigHandler(config)

    if lines_to_read:
        config_handler.config.set("Main", "LinesToRead", str(lines_to_read))
    if file_types:
        config_handler.config.set("Main", "FileTypes", file_types)

    processor = FileProcessor(config_handler)
    processor.generate_file_list(directory, output)

    click.echo(f"File list generated and saved to {output}.")


@cli.command()
@click.option("--config", default="config.ini", help="Path to the configuration file.")
@click.option(
    "--file-list",
    required=True,
    type=click.Path(exists=True),
    help="File list generated in previous phase.",
)
def analyze(config, file_list):
    """Analyze files based on a given file list."""
    config_handler = ConfigHandler(config)
    processor = FileProcessor(config_handler)
    analysis = processor.analyze_from_list(file_list)

    for key, body in analysis.items():
        if isinstance(body, dict) and "lines" in body:
            click.echo(f"Processing file: {key}")
            for line in body.get("lines", []):
                click.echo(line.strip())
        else:
            click.echo(f"Unexpected item in analysis: {body}")


@cli.command()
@click.option("--section", help="Section in the configuration.")
@click.option("--key", help="Key within the section.")
@click.option("--value", help="Value for the given key.")
@click.option(
    "--raw-config", type=click.STRING, help="Raw configuration in JSON format."
)
def set_config(section, key, value, raw_config):
    """
    Set configuration values.
    If --raw-config is provided, it takes precedence.
    """
    config_handler = ConfigHandler(use_env_var=False)

    if raw_config:
        update_config_from_raw(config_handler, raw_config)
    elif all([section, key, value]):
        update_config_from_values(config_handler, section, key, value)
    else:
        click.echo(
            "Please provide either --raw-config or --section, --key, and --value."
        )
        return

    # Save the updated configuration
    # with open('path_to_save_config.ini', 'w') as configfile:
    #     config_handler.config.write(configfile)
    click.echo("Configuration updated successfully.")


def update_config_from_raw(config_handler, raw_config):
    """Update config from raw JSON input."""
    try:
        config_content = json.loads(raw_config)
        config_handler._read_config_from_content(config_content)
    except json.JSONDecodeError:
        click.echo("Invalid JSON provided in raw-config.")
        raise click.Abort()


def update_config_from_values(config_handler, section, key, value):
    """Update config based on section, key, and value inputs."""
    if not config_handler.has_section(section):
        config_handler.config.add_section(section)
    config_handler.config.set(section, key, value)


cli.add_command(set_config)

if __name__ == "__main__":
    cli()
