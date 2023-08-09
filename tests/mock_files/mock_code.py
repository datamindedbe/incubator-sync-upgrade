class MockCode:
    mock_from_import_code_attr = {"original_code": """from package.module import object""",
                                  "new_code": """from package.new_module import object"""}

    mock_argument_code = {"original_code": """Class(arg1='arg1')""",
                          "new_code": """Class(arg2='arg1')"""}

    mock_add_attribute_from_import_code = {"original_code": """from package.module import object""",
                                           "new_code": """from package.module.new_module import object"""}
    mock_parameter_code = {"original_code": """def function(parameter1):pass""",
                           "new_code": """def function(parameter2):pass"""}
    mock_class_attribute_code = {"original_code": """self.attribute1""",
                                 "new_code": """self.attribute2"""}
    mock_assign_class_attribute_code = {"original_code": """self.attribute = value1""",
                                        "new_code": """self.attribute = value2"""}
    mock_class_definition_code = {"original_code": """class ClassName:pass""",
                                  "new_code": """class NewClassName:pass"""}

    mock_class_call_code = {"original_code": """ClassName()""",
                            "new_code": """NewClassName()"""}
    mock_name_code = {"original_code": """variable = 5""",
                      "new_code": """new_variable = 5"""}

    mock_method_call_code = {"original_code": """class_name.method()""",
                             "new_code": """class_name.new_method()"""}

    mock_function_call_code = {"original_code": """function()""",
                               "new_code": """new_function()"""}
    mock_annotation_code = {"original_code": """variable: int = 5""",
                            "new_code": """variable: float = 5"""}
    mock_from_import_code_value = {"original_code": """from package.module import object""",
                                   "new_code": """from new_package.module import object"""}
    mock_from_import_code_alias = {"original_code": """from package.module import object""",
                                   "new_code": """from package.module import new_object"""}
