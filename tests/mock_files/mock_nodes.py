from libcst import Arg, Name, Attribute, Param, Assign, AssignTarget, ClassDef, Pass, \
    SimpleStatementSuite, Call, Annotation, ImportAlias, ImportFrom, FunctionDef, Parameters, Return


class MockNodes:
    argument_node = Arg(keyword=Name("arg1"), value=Name("arg1"))
    param_node = Param(name=Name("param"))
    attribute_node = Attribute(value=Name("object"), attr=Name("method"))  # This is equivalent to object.method
    assign_node = Assign(value=Name("random_value"),
                         targets=[AssignTarget(Name("param"))])  # This is equivalent to param = random_value
    class_definition_node = ClassDef(name=Name("ClassName"), body=SimpleStatementSuite(
        body=[Pass()]))  # This equivalent to class ClassName: pass
    class_call_node = Call(func=Name("ClassName"))
    name_node = Name(value='param')
    return_node = Return(name_node)
    method_call_node = Call(
        func=Attribute(value=Name("class"), attr=Name("method")))  # This is equivalent to class.method()
    function_call_node = Call(func=Name("function"))
    annotation_node = Annotation(annotation=Name("ObjectType"))
    from_import_attr_node = Attribute(attr=Name("module"), value=Name("package"))
    from_import_alias_node = ImportFrom(names=[ImportAlias(name=Name("object"))], module=Name("module"))
    function_def_node = FunctionDef(name=Name("function_name"), params=Parameters(), body=SimpleStatementSuite(
        body=[Pass()]))
    import_alias_node = ImportAlias(name=Name("object"))
    assign_parent_target_node = AssignTarget(target=Name(value="param"))
    variable_name_node = Name("param")
    function_name = Name("function")
    assign_target_node = AssignTarget(target=Name("variable"))
