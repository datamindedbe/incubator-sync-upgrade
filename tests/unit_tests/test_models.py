from pathlib import Path

from pydantic import ValidationError
from pytest import raises

from syncupgrade.models.cli_models import InitOptions, CommonOptions, ApplyCommandOptions
from syncupgrade.models.enum_models import ApplyMode
from syncupgrade.utils.option_conditions import package_conditions, version_condition, package_version_condition, \
    validate_git_behavior


def test_init_options_model():
    init_options = InitOptions(package="package", version="2", registry="directory")
    assert init_options.refactoring_file_path == Path("directory/refactoring_files/upgrade_package_2.py")
    assert init_options.new_branch_name == "sync-upgrade/upgrade-package-2"


def test_validate_package_common_model():
    with raises(ValidationError, match="package bad123 must be a correct string"):
        CommonOptions(package="bad123", version="2", registry="directory")


def test_validate_version_common_model():
    with raises(ValidationError, match="version bad_version must be a correct string"):
        CommonOptions(package="package", version="bad_version", registry="directory")


def test_validate_version_package_common_model():
    with raises(ValidationError, match="Package and version must either be specified together or not."):
        CommonOptions(package="package", registry="directory", version="")
        CommonOptions(package="", registry="directory", version="version")


def test_validate_file_exists_init_model():
    with raises(ValidationError, match="Registry cannot be a file in the init command"):
        InitOptions(registry="tests/conftest.py", package="", version="")


def test_validate_missing_directory_apply_model():
    with raises(ValidationError, match="directory registry not found"):
        ApplyCommandOptions(package="package", version="2", registry="directory")


def test_validate_apply_no_git_model():
    with raises(ValidationError, match="Apply mode cannot be Pull Request if git option is deactivated."):
        ApplyCommandOptions(package="package", version="2", registry="tests/conftest.py",
                            apply_mode=ApplyMode.pull_request, activate_git=False)


def test_validate_missing_refactoring_file_model():
    with raises(ValidationError, match="wrong_registry registry not found"):
        ApplyCommandOptions(package="package", version="2", registry="wrong_registry")


def test_package_conditions():
    assert package_conditions("package")


def test_failed_package_conditions():
    assert not package_conditions("wrong!")


def test_empty_package_conditions():
    assert package_conditions("")


def test_empty_version_condition():
    assert version_condition("")


def test_version_condition():
    assert version_condition("123")


def test_failed_version_condition():
    assert not version_condition("wrong_version")


def test_package_version_condition():
    assert not package_version_condition("", "")
    assert not package_version_condition("package", "1")


def test_failed_package_version_condition():
    assert package_version_condition("package", "")
    assert package_version_condition("", "1")


def test_wrong_validate_git_behavior():
    assert validate_git_behavior(False, ApplyMode.pull_request)


def test_validate_git_behavior():
    assert not validate_git_behavior(True, ApplyMode.pull_request)
