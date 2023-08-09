from syncupgrade.matchers.node_matcher import find_from_import_alias, find_argument, find_parameter, \
    find_attribute, find_assign, find_class_definition, find_class_call, find_name, find_method_call, \
    find_function_call, find_annotation, find_import_from_attribute_attr, find_import_from_attribute_value, \
    find_function_def, find_import_alias, find_assign_target_variable
from tests.mock_files.mock_nodes import MockNodes


def test_find_from_import_alias():
    assert find_from_import_alias(MockNodes.from_import_alias_node, "object")


def test_failed_from_find_import_alias():
    assert not find_from_import_alias(MockNodes.from_import_alias_node, "wrong_object")


def test_find_from_import_attribute_attr():
    assert find_import_from_attribute_attr(MockNodes.from_import_attr_node, "module")


def test_failed_find_from_import_attribute_attr():
    assert not find_import_from_attribute_attr(MockNodes.from_import_attr_node, "wrong_module")


def test_find_import_from_attribute_value():
    assert find_import_from_attribute_value(MockNodes.from_import_attr_node, "package")


def test_failed_find_import_from_attribute_value():
    assert not find_import_from_attribute_value(MockNodes.from_import_attr_node, "wrong_package")


def test_find_argument():
    assert find_argument(MockNodes.argument_node, "arg1")


def test_failed_find_argument():
    assert not find_argument(MockNodes.argument_node, "arg3")


def test_find_parameters():
    assert find_parameter(MockNodes.param_node, "param")


def test_failed_find_parameters():
    assert not find_parameter(MockNodes.param_node, "wrong_param")


def test_find_attribute():
    assert find_attribute(MockNodes.attribute_node, "method", "object")


def test_failed_find_attribute():
    assert not find_attribute(MockNodes.attribute_node, "wrong_method", "object")


def test_find_assign():
    assert find_assign(MockNodes.assign_node, "random_value", "param")


def test_failed_find_assign():
    assert not find_assign(MockNodes.assign_node, "wrong_value", "wrong_param")


def test_find_class_definition():
    assert find_class_definition(MockNodes.class_definition_node, "ClassName")


def test_failed_find_class_definition():
    assert not find_class_definition(MockNodes.class_definition_node, "WrongClassName")


def test_find_class_call():
    assert find_class_call(MockNodes.class_call_node, "ClassName")


def test_failed_find_class_call():
    assert not find_class_call(MockNodes.class_call_node, "WrongClassName")


def test_find_name_from_function_body():
    assert find_name(MockNodes.name_node, "param", MockNodes.return_node)


def test_failed_find_name():
    assert not find_name(MockNodes.name_node, "wrong_param", MockNodes.return_node)


def test_find_method_call():
    assert find_method_call(MockNodes.method_call_node, "method")


def test_failed_find_method_cal():
    assert not find_method_call(MockNodes.method_call_node, "wrong_method")


def test_find_function_call():
    assert find_function_call(MockNodes.function_call_node, "function")


def test_failed_find_function_call():
    assert not find_function_call(MockNodes.function_call_node, "wrong_function")


def test_find_annotation():
    assert find_annotation(MockNodes.annotation_node, "ObjectType")


def test_failed_find_annotation():
    assert not find_annotation(MockNodes.annotation_node, "WrongType")


def test_find_function_definition():
    assert find_function_def(MockNodes.function_def_node, "function_name")


def test_failed_find_function_definition():
    assert not find_function_def(MockNodes.function_def_node, "wrong_function_name")


def test_find_import_alias():
    assert find_import_alias(MockNodes.import_alias_node, "object")


def test_failed_find_import_alias():
    assert not find_import_alias(MockNodes.import_alias_node, "wrong_object")


def test_find_assign_target_variable():
    assert find_assign_target_variable(MockNodes.assign_target_node, "variable")


def test_failed_find_assign_target_variable():
    assert not find_assign_target_variable(MockNodes.assign_target_node, "wrong_variable")
