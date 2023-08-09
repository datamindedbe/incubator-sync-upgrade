from pathlib import Path
from typing import Any, TypeVar, Union

from libcst import CSTTransformer
from rich.progress import Progress

from syncupgrade.codmods.libcst_units import RenameImport, RenameParameters, RenameClassAttribute, \
    RenameClass, RenameFunctions, RenameAnnotation, AddImportAttribute, RenameVariables
from syncupgrade.codmods.transformers_creation import TransformersManager
from syncupgrade.utils.parsing_utils import parse_code_files, parse_code_difference, parse_refactoring_methods_input, \
    cli_console

Add = TypeVar('Add', bound='AddRefactoring')
Rename = TypeVar('Rename', bound='RenameRefactoring')


class SyncUpgrade:
    def __init__(self, code_base_path: Union[str, Path]):
        self.transformer_manager = TransformersManager()
        self.code_base_path = code_base_path
        self.generated_code_base = {}

    def describe_changes(self, refactoring_file_path: str):
        self._apply_codmods(refactoring_file_path)
        for file_path in self.generated_code_base:
            parse_code_difference(file_path, self.generated_code_base[file_path])

    def apply_code_changes(self, refactoring_file_path: str):
        self._apply_codmods(refactoring_file_path)
        for file_path in self.generated_code_base:
            cli_console.print(f"Applying changes for {file_path}")
            with open(file_path, "w") as file:
                file.write(self.generated_code_base[file_path])

    def _apply_codmods(self, refactoring_file_path: str):
        original_code_base = parse_code_files(self.code_base_path)
        with Progress() as progress:
            codmod = progress.add_task(f"applying codmods from {refactoring_file_path}",
                                       total=len(original_code_base))
            for file_path in original_code_base:
                if new_code := self.transformer_manager.apply_transformers(original_code_base[file_path]):
                    self.generated_code_base[file_path] = new_code
                progress.advance(codmod)

    def apply_renames(self, renaming_transformations: Rename):
        if not isinstance(renaming_transformations, RenameRefactoring):
            raise ValueError("get_renames method takes only a Rename Class")
        self.transformer_manager.add_transformers(renaming_transformations.codmods)
        return self

    def apply_add(self, add_transformations: Add):
        if not isinstance(add_transformations, AddRefactoring):
            raise ValueError("get_add method takes only a Rename Class")
        self.transformer_manager.add_transformers(add_transformations.codmods)
        return self

    def apply_custom_transformation(self, custom_codmods: Any):
        if not isinstance(custom_codmods, CSTTransformer):
            raise ValueError("Custom codmods must either be a CSTTransformer or a subclass of it.")
        self.transformer_manager.add_transformers([custom_codmods])
        return self


class RenameRefactoring:
    def __init__(self):
        self.codmods = []

    def rename_class(self, *changes: Any):
        for old_name, new_name in parse_refactoring_methods_input(changes):
            self.codmods.extend([RenameClass(old_name, new_name), RenameAnnotation(old_name, new_name)])
        return self

    def rename_functions(self, *changes: Any):
        for old_name, new_name in parse_refactoring_methods_input(changes):
            self.codmods.extend([RenameFunctions(old_name, new_name)])
        return self

    def rename_imports(self, *changes: Any):
        for old_name, new_name in parse_refactoring_methods_input(changes):
            self.codmods.extend([RenameImport(old_name, new_name), RenameClass(old_name, new_name)])
        return self

    def rename_param(self, *changes: Any):
        for old_name, new_name in parse_refactoring_methods_input(changes):
            self.codmods.extend([RenameParameters(old_name, new_name), RenameClassAttribute(old_name, new_name)])
        return self

    def rename_variables(self, *changes: Any):
        for old_name, new_name in parse_refactoring_methods_input(changes):
            self.codmods.extend([RenameVariables(old_name, new_name), RenameParameters(old_name, new_name)])
        return self


class AddRefactoring:
    def __init__(self):
        self.codmods = []

    def add_import_attribute(self, *changes: Any):
        for imported_module_name, added_attribute in parse_refactoring_methods_input(changes):
            self.codmods.extend([AddImportAttribute(imported_module_name, added_attribute)])
        return self
