from pathlib import Path
from typing import Union
from urllib.parse import urlparse

from typer import prompt

from syncupgrade.exceptions.custom_exceptions import UpdateMethodNotFound, RefactoringFileNotFound, LoadingCodmodsFailed
from syncupgrade.git_integration.git_wrapper import GithubClient
from syncupgrade.models.cli_models import InitOptions, ApplyCommandOptions, CommonOptions
from syncupgrade.models.enum_models import ApplyMode
from syncupgrade.utils.parsing_utils import parse_refactoring_file

python_file = """from pathlib import Path

from syncupgrade import SyncUpgrade, RenameRefactoring, AddRefactoring

def update():
    renamer = (
        RenameRefactoring()
        .rename_param("old_param_name", 'new_param_name')
        .rename_imports("old_import_attribute", "new_import_attribute")
        .rename_class("old_class_name", "new_class_name")
        .rename_variables("old_variable_name", "new_variable_name")
        .rename_functions("old_function_name", "new_function_name")
  )
    add = (
        AddRefactoring()
        .add_import_attribute("ImportAlias", "new_import_attribute")    
    )

    return (
        SyncUpgrade(Path(__file__).parent.parent)
        .apply_renames(renamer)
        .apply_add(add)
        .apply_custom_transformation()
    )
"""


class RegistryManager:
    def __init__(self, cli_options: CommonOptions):
        self.cli_options = cli_options

    def create_local_registries(self):
        self.cli_options.registry.mkdir(parents=True, exist_ok=True)
        if not (self.cli_options.registry / "__init__.py").exists():
            open(self.cli_options.registry / "__init__.py", "w")
        with self.cli_options.refactoring_file_path.open("w", encoding="utf-8") as file:
            file.write(python_file)
        return f"template refactoring file created in {self.cli_options.refactoring_file_path}"

    def get_remote_registries(self):
        raise ValueError("Remote registries are not supported yet.")

    def get_codmods(self):
        if not self.cli_options.refactoring_file_path:
            return self._find_all_transformation_modules()
        if codmods := self._find_transformation_module(self.cli_options.refactoring_file_path):
            return {str(self.cli_options.refactoring_file_path): codmods}
        raise LoadingCodmodsFailed()

    def _find_all_transformation_modules(self):
        if transformation_modules := {
            str(module): self._find_transformation_module(module) for module in self.cli_options.registry.glob('*.py')
            if module.name != "__init__.py"
        }:
            return transformation_modules
        raise LoadingCodmodsFailed()

    @staticmethod
    def _find_transformation_module(refactoring_file: Path):
        try:
            return parse_refactoring_file(refactoring_file)
        except AttributeError as attribute_error:
            raise UpdateMethodNotFound from attribute_error
        except FileNotFoundError as file_not_found_error:
            raise RefactoringFileNotFound(refactoring_file, file_not_found_error) from file_not_found_error


class CliHelper:
    def __init__(self, cli_options: Union[InitOptions, ApplyCommandOptions]):
        self.cli_options = cli_options
        self.git_client = GithubClient() if self.cli_options.activate_git else None
        self.registry_manager = RegistryManager(self.cli_options)

    def dry_run(self):
        for refactoring_file_path, refactoring_object in self.registry_manager.get_codmods().items():
            refactoring_object.describe_changes(refactoring_file_path)

    def __apply_code_changes(self):
        for refactoring_file_path, refactoring_object in self.registry_manager.get_codmods().items():
            refactoring_object.apply_code_changes(refactoring_file_path)

    def apply_code(self):
        if not self.cli_options.activate_git:
            self.__apply_code_changes()
            return "Changes applied locally"

        if not self.git_client.check_current_branch(self.cli_options.new_branch_name):
            self.git_client.create_checkout_new_branch(self.cli_options.new_branch_name)
        self.__apply_code_changes()
        if self.cli_options.apply_mode == ApplyMode.pull_request:
            git_token = prompt("Enter your git token", hide_input=True)
            return self.git_client.push_to_remote(self.cli_options, git_token)
        return f"Changes applied locally in branch {self.cli_options.new_branch_name}"

    def process_registries(self):
        if self.cli_options.activate_git:
            self.git_client.create_checkout_new_branch(self.cli_options.new_branch_name)
        if urlparse(str(self.cli_options.registry)).scheme:
            self.registry_manager.get_remote_registries()
        return self.registry_manager.create_local_registries()
