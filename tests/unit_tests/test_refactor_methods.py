from libcst import CSTTransformer
from pytest import raises

from syncupgrade.codmods.libcst_units import RenameImport, RenameClass, RenameAnnotation, RenameFunctions, RenameParameters, \
    RenameClassAttribute, RenameVariables, AddImportAttribute
from syncupgrade.refactor.refactoring_methods import RenameRefactoring, AddRefactoring, SyncUpgrade


def test_rename_class_method(rename_refactoring):
    result = rename_refactoring.rename_class("old_name", "new_name")
    for codmod in rename_refactoring.codmods:
        assert isinstance(codmod, (RenameClass, RenameAnnotation))
    assert isinstance(result, RenameRefactoring)


def test_rename_functions(rename_refactoring):
    result = rename_refactoring.rename_functions("old_name", "new_name")
    for codmod in rename_refactoring.codmods:
        assert isinstance(codmod, RenameFunctions)
    assert isinstance(result, RenameRefactoring)


def test_rename_imports(rename_refactoring):
    result = rename_refactoring.rename_imports("old_name", "new_name")
    for codmod in rename_refactoring.codmods:
        assert isinstance(codmod, (RenameImport, RenameClass))
    assert isinstance(result, RenameRefactoring)


def test_rename_param(rename_refactoring):
    result = rename_refactoring.rename_param("old_name", "new_name")
    for codmod in rename_refactoring.codmods:
        assert isinstance(codmod, (RenameParameters, RenameClassAttribute))
    assert isinstance(result, RenameRefactoring)


def test_rename_variables(rename_refactoring):
    result = rename_refactoring.rename_variables("old_name", "new_name")
    for codmod in rename_refactoring.codmods:
        assert isinstance(codmod, (RenameVariables, RenameParameters))
    assert isinstance(result, RenameRefactoring)


def test_add_import_attribute(add_refactoring):
    result = add_refactoring.add_import_attribute("alias", "new_name")
    for codmod in add_refactoring.codmods:
        assert isinstance(codmod, AddImportAttribute)
    assert isinstance(result, AddRefactoring)


def test_refactor_method_fail(rename_refactoring):
    with raises(ValueError):
        rename_refactoring.rename_variables("old_n.ame", "new_name")


def test_apply_renames_fail(add_refactoring, sync_upgrade):
    with raises(ValueError, match="get_renames method takes only a Rename Class"):
        sync_upgrade.apply_renames(add_refactoring)


def test_apply_add_fail(rename_refactoring, sync_upgrade):
    with raises(ValueError, match="get_add method takes only a Rename Class"):
        sync_upgrade.apply_add(rename_refactoring)


def test_apply_renames(rename_refactoring, sync_upgrade):
    rename_refactoring.rename_variables("old_name", "new_name")
    result = sync_upgrade.apply_renames(rename_refactoring)
    assert isinstance(result, SyncUpgrade)
    assert isinstance(result.transformer_manager.transformers[0], RenameVariables)


def test_apply_add(add_refactoring, sync_upgrade):
    add_refactoring.add_import_attribute("alias", "new_name")
    result = sync_upgrade.apply_add(add_refactoring)
    assert isinstance(result, SyncUpgrade)
    assert isinstance(result.transformer_manager.transformers[0], AddImportAttribute)


def test_apply_custom_transformation_failed(sync_upgrade):
    class WrongClass:
        pass

    with raises(ValueError, match="Custom codmods must either be a CSTTransformer or a subclass of it."):
        sync_upgrade.apply_custom_transformation(WrongClass)


def test_apply_custom_transformation(sync_upgrade):
    class CorrectClass(CSTTransformer):
        pass

    result = sync_upgrade.apply_custom_transformation(CorrectClass())
    assert isinstance(result, SyncUpgrade)
    assert isinstance(result.transformer_manager.transformers[0], CorrectClass)
