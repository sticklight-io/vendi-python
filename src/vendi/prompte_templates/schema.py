import re

from pydantic import model_validator

from vendi.core.schema import SchemaMixin


class PromptTemplate(SchemaMixin):
    name: str
    """The name of the prompt template."""
    description: str | None = None
    """A description of the prompt template."""
    prompt_template: str
    """The prompt template string"""
    prompt_schema: dict = None
    """The schema of the prompt template string"""

    @model_validator(mode="after")
    @classmethod
    def make_prompt_schema(cls, data: "PromptTemplate") -> "PromptTemplate":
        """
        Create a schema from the prompt template string by extracting all the {variables} in the string.
        """
        matches = re.findall(r"(?<!\{)\{([^{}]+)\}(?!\})", data.prompt_template)
        schema = {}
        for match in set(matches):
            schema[match] = {"type": "string"}
        data.prompt_schema = schema
        return data

    def compile(self, **kwargs) -> str:
        """
        Compile the prompt template string with the given kwargs.
        :param kwargs: The values to use for the variables in the prompt template string.
        :return: The prompt template string filled with kwargs.
        """
        return self.prompt_template.format(**kwargs)
