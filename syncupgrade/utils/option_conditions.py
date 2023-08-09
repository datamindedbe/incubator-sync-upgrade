from pathlib import Path

from syncupgrade.models.enum_models import ApplyMode


def package_conditions(package: str) -> bool:
    return package.isalpha() if package else True


def version_condition(version: str) -> bool:
    if not version:
        return True
    try:
        float(version)
        return True
    except ValueError:
        return False


def package_version_condition(package: str, version: str):
    return bool((package and not version) or (version and not package))


def validate_refactoring_file_path(file_path: Path):
    return file_path.exists()


def validate_git_behavior(activate_git: bool, apply_mode: ApplyMode):
    return not activate_git and apply_mode == ApplyMode.pull_request
