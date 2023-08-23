from pathlib import Path
from typing import Optional, Union
from urllib.parse import urlparse

from pydantic import BaseModel, field_validator, model_validator

from syncupgrade.models.enum_models import ApplyMode
from syncupgrade.utils.option_conditions import package_conditions, version_condition, validate_refactoring_file_path, \
    validate_git_behavior, package_version_condition
from syncupgrade.utils.parsing_utils import format_branch_name, format_file_name, parse_local_registry


class CommonOptions(BaseModel):
    package: Optional[str]
    version: Optional[str]
    registry: Union[str, Path]
    new_branch_name: Optional[str] = ""
    refactoring_file_path: Optional[Path] = None
    activate_git: Optional[bool] = True
    remote: Optional[bool] = False

    @field_validator("package")
    def validate_package(cls, package: str):
        if not package_conditions(package):
            raise ValueError(f"package {package} must be a correct string")
        return package.lower()

    @field_validator("version")
    def validate_version(cls, version: str) -> str:
        if not version_condition(version):
            raise ValueError(f"version {version} must be a correct string")
        return version

    @model_validator(mode="before")
    def validate_before_format_model(cls, cli_options: dict):
        if package_version_condition(cli_options["package"], cli_options["version"]):
            raise ValueError("Package and version must either be specified together or not.")
        return cli_options

    def _format_fields(self):
        if not self.new_branch_name:
            self.new_branch_name = format_branch_name(self.package, self.version)


class InitOptions(CommonOptions):
    @model_validator(mode="after")
    def validate_format_model(self):
        self._format_fields()
        if not self.remote and validate_refactoring_file_path(Path(self.refactoring_file_path)):
            raise ValueError(f"{self.refactoring_file_path} already exists")
        if self.remote and not str(self.registry).endswith(".git"):
            raise ValueError("Valid remote registry must end with .git to clone")
        return self

    @field_validator("registry")
    def validate_registry(cls, registry: str):
        if Path(registry).is_file() or Path(registry).suffix not in [".git", ""]:
            raise ValueError("Registry cannot be a file in the init command")
        return registry

    def _format_fields(self):
        super()._format_fields()
        if urlparse(self.registry).scheme:
            self.remote = True
        else:
            self.registry = Path(self.registry)
            self.refactoring_file_path = parse_local_registry(self.registry) / format_file_name(self.package,
                                                                                                self.version)


class ApplyCommandOptions(CommonOptions):
    apply_mode: Optional[ApplyMode] = ApplyMode.dry_run
    base_branch: Optional[str] = ""

    @field_validator("registry")
    def validate_registry(cls, registry: str):
        if Path(registry).exists():
            return registry
        raise ValueError(f"{registry} registry not found")

    @model_validator(mode="after")
    def validate_apply_model(self):
        self._format_fields()
        if validate_git_behavior(self.activate_git, self.apply_mode):
            raise ValueError("Apply mode cannot be Pull Request if git option is deactivated.")
        return self

    def _format_fields(self):
        super()._format_fields()
        self.registry = Path(self.registry)
        if self.registry.is_file():
            self.refactoring_file_path = self.registry
        elif self.package:
            self.refactoring_file_path = self.registry / format_file_name(self.package, self.version)
