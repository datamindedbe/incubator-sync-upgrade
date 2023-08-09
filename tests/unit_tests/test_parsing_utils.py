from pathlib import Path

from pytest import raises

from syncupgrade.exceptions.custom_exceptions import RefactoringFileNotFound
from syncupgrade.refactor.refactoring_methods import SyncUpgrade
from syncupgrade.utils.parsing_utils import parse_code_files, parse_refactoring_methods_input, parse_refactoring_file


def test_parse_code_files_failed():
    with raises(ValueError, match="Couldn't find code base with wrong_path"):
        parse_code_files("wrong_path")


def test_parse_code_wrong_file_failed():
    with raises(ValueError, match="Only python files are supported"):
        parse_code_files("poetry.lock")


def test_parse_code_folder():
    assert set(parse_code_files("tests/mock_files/end_to_end_test").keys()) == {
        Path('tests/mock_files/end_to_end_test/mock_code_file.py'),
        Path('tests/mock_files/end_to_end_test/mock_refactored_file.py'),
        Path('tests/mock_files/end_to_end_test/operator.py'),
        Path('tests/mock_files/end_to_end_test/refactored_operator.py')}


def test_parse_code_file():
    assert parse_code_files("tests/mock_files/end_to_end_test/operator.py") == {
        "tests/mock_files/end_to_end_test/operator.py": """class Operator:
    def make_addition(self, x, y):
        return x + y

    def make_multiplication(self, x, y):
        return x * y
"""
    }


def test_empty_parse_refactoring_methods_input():
    with raises(ValueError, match="Refactoring input cannot be empty"):
        list(parse_refactoring_methods_input(()))


def test_bad_parse_refactoring_methods_input():
    with raises(ValueError, match="Refactoring input cannot contain special characters"):
        list(parse_refactoring_methods_input(("bad name", "bad name")))


def test_parse_refactoring_methods_input(mocker):
    mocked = mocker.patch("syncupgrade.utils.parsing_utils.validation_refactoring_input", return_value=("old_name", "new_name"))
    list(parse_refactoring_methods_input(("old_name", "new_name")))
    assert mocked.called


def test_parse_refactoring_file_failed():
    with raises(RefactoringFileNotFound, match="Couldn't load refactoring file wrong_file."):
        parse_refactoring_file(Path("wrong_file"))


def test_parse_refactoring_file():
    result = parse_refactoring_file(Path("tests/conftest.py"))
    assert isinstance(result, SyncUpgrade)
    assert len(result.transformer_manager.transformers) == 19


def test_parse_refactoring_file_no_update():
    with raises(AttributeError, match="module 'tests/mock_files' has no attribute 'update'"):
        parse_refactoring_file(Path("tests/mock_files/mock_code.py"))
