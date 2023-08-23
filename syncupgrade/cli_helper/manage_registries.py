from pathlib import Path
from shutil import rmtree, move
from typing import Union

from syncupgrade.exceptions.custom_exceptions import LoadingCodmodsFailed, UpdateMethodNotFound, \
    RefactoringFileNotFound, RefactoringFilesFolderMissing
from syncupgrade.models.cli_models import CommonOptions
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
    def __init__(self, cli_options: CommonOptions, root_path: str):
        self.cli_options = cli_options
        self.root_path = root_path

    def create_local_registries(self):
        self.cli_options.refactoring_file_path.parent.mkdir(parents=True, exist_ok=True)
        for folder in self.cli_options.refactoring_file_path.parents:
            if not (folder / '__init__.py').exists() or folder.name != "":
                (folder / '__init__.py').touch()
        with self.cli_options.refactoring_file_path.open("w", encoding="utf-8") as file:
            file.write(python_file)
        return f"template refactoring file created in {self.cli_options.refactoring_file_path}"

    def get_remote_registries(self, path_data: dict):
        try:
            self.move_refactoring_files_folder(path_data["root_path"])
        except FileNotFoundError as file_not_found:
            raise RefactoringFilesFolderMissing() from file_not_found
        rmtree(path_data["remote_local_path"])
        return "Got remote"

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

    @staticmethod
    def move_refactoring_files_folder(root_path: Union[str, Path]):
        refactoring_folder_path = next(Path(root_path).rglob("refactoring_files"), None)
        move(refactoring_folder_path, f"{root_path}/refactoring_files")

    def find_root_path(self):
        if self.root_path:
            return Path(self.root_path).parent
