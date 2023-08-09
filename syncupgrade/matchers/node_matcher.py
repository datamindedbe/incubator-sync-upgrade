import libcst as cst
from libcst.matchers import matches, Name, Arg, ImportFrom, Attribute, ImportAlias, Param, Assign, AssignTarget, \
    ClassDef, Call, FunctionDef, Annotation, findall


def find_argument(node: cst.Arg, argument_name: str):
    return matches(
        node,
        Arg(keyword=Name(argument_name))
    )


def find_from_import_alias(node: cst.ImportFrom, import_alias_name: str):
    return matches(
        node,
        ImportFrom(names=[ImportAlias(Name(import_alias_name))])
    )


def find_parameter(node: cst.Param, parameter_name: str):
    return matches(
        node,
        Param(name=Name(parameter_name))
    )


def find_attribute(node: cst.Attribute, attribute: str, value: str = "self"):
    return matches(
        node,
        Attribute(value=Name(value),
                  attr=Name(attribute))
    )


def find_assign(node: cst.Assign, value: str, target: str = None):
    if target is None:
        return matches(
            node,
            Assign(value=Name(value))
        )
    return matches(
        node,
        Assign(value=Name(value), targets=[AssignTarget(Name(target))])
    )


def find_class_definition(node: cst.ClassDef, class_name: str):
    return matches(
        node,
        ClassDef(name=Name(class_name))
    )


def find_method_call(node: cst.Call, method_name: str):
    return matches(
        node,
        Call(func=Attribute(attr=Name(method_name)))
    )


def find_function_call(node: cst.Call, function_name: str):
    return matches(
        node,
        Call(func=Name(function_name))
    )


def find_class_call(node: cst.Call, class_name: str):
    return matches(
        node,
        Call(func=Name(class_name))
    )


def find_name(node: cst.Name, reference_name: str, parent_node: cst.CSTNode = None):
    if not parent_node and isinstance(parent_node, (cst.FunctionDef, cst.ClassDef, cst.AssignTarget)):
        return False
    return matches(
        node,
        Name(value=reference_name)
    )


def find_function_def(node: cst.FunctionDef, function_name: str):
    return matches(
        node,
        FunctionDef(name=Name(function_name))
    )


def find_annotation(node: cst.Annotation, annotation_name: str):
    return matches(
        node,
        Annotation(annotation=Name(annotation_name))
    )


def find_import_alias(node: cst.ImportAlias, object_name: str):
    return matches(
        node,
        ImportAlias(name=Name(object_name))
    )


def find_import_from_attribute_attr(node: cst.ImportFrom, old_module_name: str):
    if node := findall(
            node,
            Attribute(attr=Name(old_module_name))
    ):
        return node[0]


def find_import_from_attribute_value(node: cst.ImportFrom, old_module_name: str):
    if node := findall(
            node,
            Attribute(value=Name(old_module_name))
    ):
        return node[0]


def find_assign_target_variable(node: cst.AssignTarget, variable_name: str):
    return matches(
        node,
        AssignTarget(target=Name(variable_name))
    )
