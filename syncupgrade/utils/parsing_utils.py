from difflib import unified_diff
from importlib.util import spec_from_file_location, module_from_spec
from pathlib import Path
from re import search, match
from sys import modules

from libcst import Module
from libcst.codemod import TransformResult, TransformSuccess, TransformFailure
from rich.console import Console

from syncupgrade.exceptions.custom_exceptions import RefactoringFileNotFound

cli_console = Console(log_time=True)


def parse_code_files(user_input: str):
    code_base_path = Path(user_input)
    if code_base_path.is_file():
        if code_base_path.suffix != ".py":
            raise ValueError("Only python files are supported")
        return {user_input: open(user_input, "r").read()}
    if code_base := {file: open(file, "r").read() for file in get_code_files(code_base_path)}:
        return code_base
    raise ValueError(f"Couldn't find code base with {user_input}")


def get_code_files(code_base_path: Path):
    for file in code_base_path.rglob("*.py"):
        if all(
                keyword not in str(file) for keyword in ["bin", "Scripts", "lib"]
        ):
            yield file


def parse_code_difference(file_path: str, code_changes: Module):
    if diff := "".join(unified_diff(
            open(file_path, "r").read().splitlines(1),
            code_changes.splitlines(1))):
        cli_console.log(f"Changes for file {file_path}")
        for line in diff.splitlines():
            if line.startswith('+') and search('[a-zA-Z]', line):
                cli_console.print(line, style="green")
            elif line.startswith('-') and search('[a-zA-Z]', line):
                cli_console.print(line, style="red")


def format_branch_name(package: str, version: str):
    if package and version:
        return f"sync-upgrade/upgrade-{package}-{version}"
    return "sync-upgrade/upgrade-project"


def format_file_name(package: str, version: str):
    if package and version:
        return f"upgrade_{package}_{version}.py"
    return "upgrade_project.py"


def parse_refactoring_methods_input(changes: tuple):
    if not changes or not changes[0]:
        raise ValueError("Refactoring input cannot be empty")
    if isinstance(changes[0], tuple):
        for change in changes:
            yield validation_refactoring_input(change)
        return
    yield validation_refactoring_input(changes)


def handle_transform_module_response(response: TransformResult) -> str:
    if isinstance(response, TransformSuccess):
        return response.code
    if isinstance(response, TransformFailure):
        raise response.error


def validation_refactoring_input(changes: tuple):
    if bool(match(r'^[a-zA-Z0-9_]+$', changes[0]) and match(r'^[a-zA-Z0-9_]+$', changes[1])):
        return changes[0], changes[1]
    raise ValueError("Refactoring input cannot contain special characters")


def format_pr_link(url: str):
    return f"PR link {url.replace('api.github.com/repos', 'github.com').replace('pulls', 'pull')}"


def parse_refactoring_file(refactoring_file: Path):
    if spec := spec_from_file_location(str(refactoring_file.parent), str(refactoring_file)):
        module = module_from_spec(spec)
        modules[str(refactoring_file.parent)] = module
        spec.loader.exec_module(module)
        return module.update()
    raise RefactoringFileNotFound(refactoring_file)
