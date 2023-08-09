from pathlib import Path
from typing import Optional

from pydantic import BaseModel, field_validator, model_validator

from syncupgrade.models.enum_models import ApplyMode
from syncupgrade.utils.option_conditions import package_conditions, version_condition, validate_refactoring_file_path, \
    validate_git_behavior, package_version_condition
from syncupgrade.utils.parsing_utils import format_branch_name, format_file_name


class CommonOptions(BaseModel):
    package: Optional[str]
    version: Optional[str]
    registry: Path
    new_branch_name: Optional[str] = ""
    refactoring_file_path: Optional[Path] = ""
    activate_git: Optional[bool] = True

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
        if validate_refactoring_file_path(Path(self.refactoring_file_path)):
            raise ValueError(f"{self.refactoring_file_path} already exists")
        return self

    def _format_fields(self):
        super()._format_fields()
        if self.registry.is_file() or self.registry.suffix:
            self.refactoring_file_path = self.registry
            self.registry = self.registry.parent
        else:
            self.refactoring_file_path = self.registry / format_file_name(self.package, self.version)


class ApplyCommandOptions(CommonOptions):
    apply_mode: Optional[ApplyMode] = ApplyMode.dry_run
    base_branch: Optional[str] = ""

    @field_validator("registry")
    def validate_registry(cls, registry: Path):
        if registry.exists():
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
        if self.registry.is_file():
            self.refactoring_file_path = self.registry
        elif self.package:
            self.refactoring_file_path = self.registry / format_file_name(self.package, self.version)
