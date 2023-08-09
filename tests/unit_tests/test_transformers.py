from tests.conftest import generate_new_code
from tests.mock_files.mock_code import MockCode


def test_rename_import_attr_transformer(mock_rename_import_attr):
    assert generate_new_code(MockCode.mock_from_import_code_attr["original_code"], mock_rename_import_attr) == \
           MockCode.mock_from_import_code_attr["new_code"]


def test_rename_arguments_transformer(mock_rename_arguments):
    assert generate_new_code(MockCode.mock_argument_code["original_code"], mock_rename_arguments) == \
           MockCode.mock_argument_code["new_code"]


def test_add_from_import_attribute_transformer(mock_add_import_attribute):
    assert generate_new_code(MockCode.mock_add_attribute_from_import_code["original_code"],
                             mock_add_import_attribute) == MockCode.mock_add_attribute_from_import_code["new_code"]


def test_rename_parameters_transformer(mock_rename_parameter):
    assert generate_new_code(MockCode.mock_parameter_code["original_code"], mock_rename_parameter) == \
           MockCode.mock_parameter_code["new_code"]


def test_rename_class_attribute_transformer(mock_rename_class_attribute):
    assert generate_new_code(MockCode.mock_class_attribute_code["original_code"],
                             mock_rename_class_attribute) == MockCode.mock_class_attribute_code["new_code"]


def test_rename_class_assign(mock_rename_class_assign):
    assert generate_new_code(MockCode.mock_assign_class_attribute_code["original_code"], mock_rename_class_assign) == \
           MockCode.mock_assign_class_attribute_code["new_code"]


def test_rename_class_definition(mock_rename_class_definition):
    assert generate_new_code(MockCode.mock_class_definition_code["original_code"], mock_rename_class_definition) == \
           MockCode.mock_class_definition_code["new_code"]


def test_rename_class_call(mock_rename_class_definition):
    assert generate_new_code(MockCode.mock_class_call_code["original_code"],
                             mock_rename_class_definition) == MockCode.mock_class_call_code["new_code"]


def test_rename_name(mock_rename_variables):
    assert generate_new_code(MockCode.mock_name_code["original_code"], mock_rename_variables) == \
           MockCode.mock_name_code[
               "new_code"]


def test_rename_method_call(mock_rename_method):
    assert generate_new_code(MockCode.mock_method_call_code["original_code"], mock_rename_method) == \
           MockCode.mock_method_call_code["new_code"]


def test_rename_function_call(mock_rename_function):
    assert generate_new_code(MockCode.mock_function_call_code["original_code"], mock_rename_function) == \
           MockCode.mock_function_call_code["new_code"]


def test_rename_annotation(mock_rename_annotation):
    assert generate_new_code(MockCode.mock_annotation_code["original_code"], mock_rename_annotation) == \
           MockCode.mock_annotation_code["new_code"]


def test_rename_import_value_transformer(mock_rename_import_value):
    assert generate_new_code(MockCode.mock_from_import_code_value["original_code"], mock_rename_import_value) == \
           MockCode.mock_from_import_code_value["new_code"]


def test_rename_import_alias_transformer(mock_rename_import_alias):
    assert generate_new_code(MockCode.mock_from_import_code_alias["original_code"], mock_rename_import_alias) == \
           MockCode.mock_from_import_code_alias["new_code"]
