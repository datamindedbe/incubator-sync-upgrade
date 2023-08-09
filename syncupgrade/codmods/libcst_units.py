from libcst import Attribute, Name, ImportFrom, Assign, ClassDef, Call, FunctionDef, \
    Annotation, ImportAlias, Param, Arg, AssignTarget
from libcst import matchers as m
from libcst.codemod import CodemodContext, VisitorBasedCodemodCommand
from libcst.metadata import ParentNodeProvider, ScopeProvider

from syncupgrade.matchers.node_matcher import find_from_import_alias, find_attribute, find_assign, find_class_definition, \
    find_class_call, find_function_def, \
    find_function_call, find_method_call, find_annotation, find_import_alias, find_import_from_attribute_attr, \
    find_import_from_attribute_value, find_argument, find_parameter, find_name, find_assign_target_variable


class BaseTransformer(VisitorBasedCodemodCommand):
    METADATA_DEPENDENCIES = (ScopeProvider, ParentNodeProvider)
    transformer_context = CodemodContext()

    def __init__(self, old_name: str, new_name: str, context: CodemodContext = transformer_context) -> None:
        super().__init__(context)
        self.old_name = old_name
        self.new_name = new_name


class RenameParameters(BaseTransformer):

    def __init__(self, old_name: str, new_name: str):
        super().__init__(old_name, new_name)

    def leave_Arg(self, original_node: Arg, updated_node: Arg) -> Arg:
        if find_argument(updated_node, self.old_name):
            return updated_node.with_changes(
                keyword=Name(self.new_name)
            )
        return updated_node

    def leave_Param(self, original_node: Param, updated_node: Param) -> Param:
        if find_parameter(updated_node, self.old_name):
            return updated_node.with_changes(
                name=Name(self.new_name)
            )
        return updated_node

    @m.call_if_inside(m.OneOf(m.FunctionDef() | m.ClassDef()))
    def leave_Name(self, original_node: Name, updated_node: Name) -> Name:
        if find_name(updated_node, self.old_name, self.get_metadata(ParentNodeProvider, original_node)):
            return updated_node.with_changes(value=self.new_name)
        return updated_node


class RenameClassAttribute(BaseTransformer):
    def __init__(self, old_name, new_name):
        super().__init__(old_name, new_name)

    def leave_Attribute(self, original_node: Attribute, updated_node: Attribute) -> Attribute:
        if find_attribute(updated_node, attribute=self.old_name):
            return updated_node.with_changes(
                attr=Name(self.new_name)
            )
        return updated_node

    def leave_Assign(self, original_node: Assign, updated_node: Assign) -> Assign:
        if find_assign(updated_node, self.old_name):
            return updated_node.with_changes(
                value=Name(self.new_name)
            )
        return updated_node


class RenameClass(BaseTransformer):
    def __init__(self, old_name: str, new_name: str):
        super().__init__(old_name, new_name)

    def leave_ClassDef(self, original_node: ClassDef, updated_node: ClassDef) -> ClassDef:
        if find_class_definition(updated_node, self.old_name):
            return updated_node.with_changes(
                name=Name(self.new_name)
            )
        return updated_node

    def leave_Call(self, original_node: Call, updated_node: Call) -> Call:
        if find_class_call(updated_node, self.old_name):
            return updated_node.with_changes(
                func=Name(self.new_name)
            )
        return updated_node


class RenameFunctions(BaseTransformer):
    def __init__(self, old_name: str, new_name: str):
        super().__init__(old_name, new_name)

    def leave_FunctionDef(self, original_node: FunctionDef, updated_node: FunctionDef) -> FunctionDef:
        if find_function_def(updated_node, self.old_name):
            return updated_node.with_changes(
                name=Name(self.new_name)
            )
        return updated_node

    def leave_Call(self, original_node: Call, updated_node: Call) -> Call:
        if find_function_call(updated_node, self.old_name):
            return updated_node.with_changes(
                func=Name(self.new_name)
            )
        if find_method_call(original_node, self.old_name):
            return updated_node.with_changes(
                func=Attribute(attr=Name(self.new_name), value=updated_node.func.value))
        return updated_node


class RenameAnnotation(BaseTransformer):
    def __init__(self, old_name: str, new_name: str):
        super().__init__(old_name, new_name)

    def leave_Annotation(self, original_node: Annotation, updated_node: Annotation) -> Annotation:
        if find_annotation(updated_node, self.old_name):
            return updated_node.with_changes(annotation=Name(self.new_name))
        return updated_node


class AddImportAttribute(BaseTransformer):
    def __init__(self, old_name: str, new_name: str):
        super().__init__(old_name, new_name)

    def leave_ImportFrom(self, original_node: ImportFrom, updated_node: ImportFrom) -> ImportFrom:
        if find_from_import_alias(updated_node, self.old_name):
            return updated_node.with_changes(
                module=Attribute(
                    value=updated_node.module,
                    attr=Name(self.new_name)
                )

            )
        return updated_node


class RenameImport(BaseTransformer):
    def __init__(self, old_name: str, new_name: str):
        super().__init__(old_name, new_name)

    def leave_ImportAlias(self, original_node: ImportAlias, updated_node: ImportAlias) -> ImportAlias:
        if find_import_alias(updated_node, self.old_name):
            return updated_node.with_changes(
                name=Name(self.new_name)
            )
        return updated_node

    def leave_ImportFrom(self, original_node: ImportFrom, updated_node: ImportFrom) -> ImportFrom:
        if old_node := find_import_from_attribute_attr(updated_node, self.old_name):
            return updated_node.deep_replace(old_node, old_node.with_changes(
                attr=Name(self.new_name), value=old_node.value
            ))
        if old_node := find_import_from_attribute_value(updated_node, self.old_name):
            return updated_node.deep_replace(old_node, old_node.with_changes(
                attr=old_node.attr, value=Name(self.new_name)
            ))
        return updated_node


class RenameVariables(BaseTransformer):
    def __init__(self, old_name: str, new_name: str):
        super().__init__(old_name, new_name)

    def leave_AssignTarget(self, original_node: AssignTarget, updated_node: AssignTarget) -> AssignTarget:
        if find_assign_target_variable(original_node, self.old_name):
            return updated_node.with_changes(
                target=Name(self.new_name)
            )
        return updated_node
