from pathlib import Path

from pytest import raises

from syncupgrade.cli_helper.cli_utils import RegistryManager
from syncupgrade.exceptions.custom_exceptions import RefactoringFileNotFound, UpdateMethodNotFound, LoadingCodmodsFailed
from syncupgrade.refactor.refactoring_methods import SyncUpgrade


def test_find_transformation_module_file_not_found(registry_manager):
    with raises(RefactoringFileNotFound,
                match="Couldn't load refactoring file wrong_file. Couldn't load refactoring file wrong_file"):
        registry_manager._find_transformation_module(Path("wrong_file"))


def test_find_transformation_module_file_no_update_method(registry_manager):
    with raises(UpdateMethodNotFound,
                match="Refactoring file must implement the update()"):
        registry_manager._find_transformation_module(Path("tests/mock_files/mock_code.py"))


def test_find_transformation_module_file(registry_manager):
    result = registry_manager._find_transformation_module(Path("tests/conftest.py"))
    assert isinstance(result, SyncUpgrade)
    assert len(result.transformer_manager.transformers) == 19


def test_find_all_transformation_modules_failed(registry_manager):
    registry_manager.cli_options.registry = Path("wrong_directory")
    with raises(LoadingCodmodsFailed, match="Failed to load codmods"):
        registry_manager._find_all_transformation_modules()


def test_find_all_transformation_modules(registry_manager):
    registry_manager.cli_options.registry = Path("tests")
    result = registry_manager._find_all_transformation_modules()
    assert list(result.keys()) == ["tests/conftest.py"]
    assert len(result["tests/conftest.py"].transformer_manager.transformers) == 19


def test_get_codmods_from_file(registry_manager, mocker):
    registry_manager.cli_options.refactoring_file_path = Path("refactoring_file")
    sync = SyncUpgrade("")
    mock_find_transformation_module = mocker.patch.object(RegistryManager, "_find_transformation_module",
                                                          return_value=sync)
    result = registry_manager.get_codmods()
    assert mock_find_transformation_module.called
    assert result == {"refactoring_file": sync}


def test_get_all_codmods(registry_manager, mocker):
    sync = SyncUpgrade("tests")
    registry_manager.cli_options.registry = Path("tests")
    mock_find_all_transformation_module = mocker.patch.object(RegistryManager, "_find_all_transformation_modules",
                                                              return_value={'tests/conftest.py': sync})
    registry_manager.get_codmods()
    assert mock_find_all_transformation_module.called


def test_get_all_codmods_failed(registry_manager, mocker):
    mocker.patch.object(RegistryManager, "_find_transformation_module", None)
    with raises(LoadingCodmodsFailed):
        registry_manager.get_codmods()
