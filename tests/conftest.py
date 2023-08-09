from libcst.codemod import transform_module, ContextAwareTransformer
from pytest import fixture
from typer.testing import CliRunner

from syncupgrade.cli_helper.cli_utils import RegistryManager
from syncupgrade.codmods.libcst_units import RenameImport, RenameParameters, AddImportAttribute, RenameClassAttribute, \
    RenameClass, RenameFunctions, RenameAnnotation, RenameVariables
from syncupgrade.models.cli_models import ApplyCommandOptions
from syncupgrade.refactor.refactoring_methods import RenameRefactoring, SyncUpgrade, AddRefactoring

mock_folder_path = "tests/mock_files/end_to_end_test/"


@fixture
def mock_original_code_base():
    original_mock_code = "tests/mock_files/end_to_end_test/mock_code_file.py"
    original_mock_operator = "tests/mock_files/end_to_end_test/operator.py"
    return {original_mock_code: open(original_mock_code, "r").read(),
            original_mock_operator: open(original_mock_operator, "r").read()}


@fixture
def mock_refactored_code_base():
    refactored_mock_code = "tests/mock_files/end_to_end_test/mock_refactored_file.py"
    refactored_mock_operator = "tests/mock_files/end_to_end_test/refactored_operator.py"

    return {refactored_mock_code: open(refactored_mock_code, "r").read(),
            refactored_mock_operator: open(refactored_mock_operator, "r").read()}


def generate_new_code(code_statement: str, transformer: ContextAwareTransformer) -> str:
    return transform_module(transformer, code_statement).code


@fixture
def mock_rename_import_attr():
    return RenameImport("module", "new_module")


@fixture
def mock_rename_arguments():
    return RenameParameters("arg1", "arg2")


@fixture
def mock_add_import_attribute():
    return AddImportAttribute("object", "new_module")


@fixture
def mock_rename_parameter():
    return RenameParameters("parameter1", "parameter2")


@fixture
def mock_rename_class_attribute():
    return RenameClassAttribute("attribute1", "attribute2")


@fixture
def mock_rename_class_assign():
    return RenameClassAttribute("value1", "value2")


@fixture
def mock_rename_class_definition():
    return RenameClass("ClassName", "NewClassName")


@fixture
def mock_rename_variables():
    return RenameVariables("variable", "new_variable")


@fixture
def mock_rename_method():
    return RenameFunctions("method", "new_method")


@fixture
def mock_rename_function():
    return RenameFunctions("function", "new_function")


@fixture
def mock_rename_annotation():
    return RenameAnnotation("int", "float")


@fixture
def mock_rename_import_value():
    return RenameImport("package", "new_package")


@fixture
def mock_rename_import_alias():
    return RenameImport("object", "new_object")


@fixture
def cli_runner():
    return CliRunner()


@fixture
def registry_manager():
    return RegistryManager(ApplyCommandOptions(package="", version="", registry=""))


renamer = (
    RenameRefactoring()
    .rename_class("Calculate", "Calculator")
    .rename_param(("param1", "x"), ("param2", "y"), ("function", "operation"), ("operator", "calculator_helper"))
    .rename_functions(("calculate_add", "add_operation"), ("calculate_multiply", "multiply_operation"),
                      ("calculator", "make_calculations"), ("make_addition", "add"),
                      ("make_multiplication", "multiply"))
    .rename_imports(("operator", "refactored_operator"), ("Operator", "CalculatorHelper"))
)


def update():
    return (
        SyncUpgrade(mock_folder_path)
        .apply_renames(renamer)
    )


@fixture
def rename_refactoring():
    return RenameRefactoring()


@fixture
def add_refactoring():
    return AddRefactoring()

@fixture
def sync_upgrade():
    return SyncUpgrade("tests")