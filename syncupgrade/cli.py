from pathlib import Path
from typing import Annotated

from typer import Typer, Option

from syncupgrade.cli_helper.cli_utils import CliHelper
from syncupgrade.models.cli_models import InitOptions, ApplyCommandOptions
from syncupgrade.models.enum_models import ApplyMode
from syncupgrade.utils.parsing_utils import cli_console

cli = Typer()


@cli.command(name="init")
def add_transformation(package: Annotated[str, Option(help='Package to upgrade')] = "",
                       version: Annotated[str, Option(help='New package version')] = "",
                       registry: Annotated[
                           str, Option(help='Directory where refactoring files are saved')] = './refactoring_files/',
                       git: Annotated[bool, Option(help='Activate git')] = True):
    init_command_options = InitOptions(package=package, version=version, registry=registry,
                                       activate_git=git)
    cli_helper = CliHelper(init_command_options)
    cli_console.print(cli_helper.process_registries())


@cli.command(name="apply")
def apply_transformation(package: Annotated[str, Option(help='Package to upgrade')] = "",
                         version: Annotated[str, Option(help='New package version')] = "",
                         base_branch: Annotated[str, Option(help='Git branch to merge with')] = "",
                         apply_mode: Annotated[ApplyMode, Option(
                             help='Check or apply changes or create a pull request')] = ApplyMode.dry_run.value,
                         registry: Annotated[
                             str, Option(help='Directory where refactoring files are saved')] = './refactoring_files/',
                         git: Annotated[bool, Option(help='Activate git')] = True):
    apply_command_options = ApplyCommandOptions(package=package, version=version, registry=Path(registry),
                                                apply_mode=apply_mode, base_branch=base_branch,
                                                activate_git=git)
    cli_helper = CliHelper(apply_command_options)
    if apply_mode.value == apply_mode.dry_run.value:
        cli_helper.dry_run()
    else:
        cli_console.print(cli_helper.apply_code())
