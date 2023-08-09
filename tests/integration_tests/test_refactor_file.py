from pytest import raises

from syncupgrade.refactor.refactoring_methods import SyncUpgrade, RenameRefactoring
from tests.conftest import mock_folder_path
from tests.conftest import renamer


def test_multiple_transformation(mock_refactored_code_base, mock_original_code_base):
    (
        SyncUpgrade(mock_folder_path)
        .apply_renames(renamer)
        .apply_code_changes("tests/conftest.py")
    )
    for original_code, refactored_code in zip(mock_original_code_base, mock_refactored_code_base):
        assert open(original_code).read() == mock_refactored_code_base[refactored_code]
        with open(original_code, "w") as file:
            file.write(mock_original_code_base[original_code])


def test_wrong_refactoring_input():
    with raises(ValueError, match="Refactoring input cannot contain special characters"):
        RenameRefactoring().rename_class("Calculat e", "Calculator")


def test_custom_transformation():
    class WrongClass:
        def __init__(self):
            pass

    with raises(ValueError, match="Custom codmods must either be a CSTTransformer or a subclass of it."):
        SyncUpgrade("").apply_custom_transformation(WrongClass())
