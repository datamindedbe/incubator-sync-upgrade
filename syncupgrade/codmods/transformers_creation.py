from difflib import unified_diff
from typing import List

from libcst import CSTTransformer
from libcst.codemod import transform_module

from syncupgrade.exceptions.custom_exceptions import MissingTransformationMethod
from syncupgrade.utils.parsing_utils import handle_transform_module_response


class TransformersManager:
    def __init__(self):
        self.transformers = []

    def add_transformers(self, node: List[CSTTransformer]):
        self.transformers.extend(node)

    def apply_transformers(self, original_source_code: str) -> str:
        if not self.transformers:
            raise MissingTransformationMethod()

        generated_source_code = original_source_code
        for transformer in self.transformers:
            generated_source_code = handle_transform_module_response(
                transform_module(transformer, generated_source_code))
        if "".join(unified_diff(
                original_source_code.splitlines(1),
                generated_source_code.splitlines(1))):
            return generated_source_code
