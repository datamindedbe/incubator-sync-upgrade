import shutil

from pydantic import ValidationError

from syncupgrade.cli import cli
from syncupgrade.exceptions.custom_exceptions import UpdateMethodNotFound
from tests.mock_files.cli_options import CliOptions


def test_apply_dry_run_no_git(cli_runner):
    result = cli_runner.invoke(cli, CliOptions.dry_run_no_git_options)
    assert result.exit_code == 0


def test_apply_pull_request_no_git_fail(cli_runner):
    result = cli_runner.invoke(cli, CliOptions.apply_pull_request_no_git_fail_options)
    assert result.exit_code == 1
    assert isinstance(result.exception, ValidationError)
    assert "Apply mode cannot be Pull Request if git option is deactivated." in result.exception.errors()[0]["msg"]


def test_apply_no_git(cli_runner, mock_original_code_base, mock_refactored_code_base):
    result = cli_runner.invoke(cli, CliOptions.apply_no_git_options)
    assert result.exit_code == 0
    for original_code, refactored_code in zip(mock_original_code_base, mock_refactored_code_base):
        assert open(original_code).read() == mock_refactored_code_base[refactored_code]
        assert f"Applying changes for {original_code}" in result.stdout
        with open(original_code, "w") as file:
            file.write(mock_original_code_base[original_code])


def test_apply_missing_version_no_git_fail(cli_runner):
    result = cli_runner.invoke(cli, CliOptions.apply_missing_version_no_git_options)
    assert result.exit_code == 1
    assert isinstance(result.exception, ValidationError)
    assert "Package and version must either be specified together or not." in result.exception.errors()[0]["msg"]


def test_apply_wrong_package_no_git_fail(cli_runner):
    result = cli_runner.invoke(cli, CliOptions.apply_wrong_package_no_git_options)
    assert result.exit_code == 1
    assert isinstance(result.exception, ValidationError)
    assert "package package_name1 must be a correct string" in result.exception.errors()[0]["msg"]


def dry_run_wrong_registry_no_git_fail(cli_runner):
    result = cli_runner.invoke(cli, CliOptions.dry_run_wrong_registry_no_git_options)
    assert result.exit_code == 1
    assert isinstance(result.exception, ValidationError)
    assert "registry not found" in result.exception.errors()[0]["msg"]


def test_missing_update_method_no_git_fail(cli_runner):
    result = cli_runner.invoke(cli, CliOptions.dry_run_no_update_no_git_options)
    assert result.exit_code == 1
    assert isinstance(result.exception, UpdateMethodNotFound)


def test_init_no_git(cli_runner):
    result = cli_runner.invoke(cli, CliOptions.init_no_git_options)
    assert result.exit_code == 0
    assert "template refactoring file created in tests/mock_registry/refactoring_files/upgrade_project.py" in result.stdout
    shutil.rmtree("tests/mock_registry/")


def test_init_package_version_no_git(cli_runner):
    result = cli_runner.invoke(cli, CliOptions.init_package_version_no_git_options)
    assert result.exit_code == 0
    assert "template refactoring file created in tests/mock_registry/refactoring_files/upgrade_package_2.py" in result.stdout
    shutil.rmtree("tests/mock_registry/")


def test_init_exists_no_git(cli_runner):
    cli_runner.invoke(cli, CliOptions.init_no_git_exists_options)
    result = cli_runner.invoke(cli, CliOptions.init_no_git_exists_options)
    assert result.exit_code == 1
    assert isinstance(result.exception, ValidationError)
    assert "tests/mock_registry/refactoring_files/upgrade_project.py already exists" in result.exception.errors()[0]["msg"]
    shutil.rmtree("tests/mock_registry/")
