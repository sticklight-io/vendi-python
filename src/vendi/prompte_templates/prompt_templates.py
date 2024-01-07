from typing import Optional, List

from vendi.core.http_client import HttpClient
from vendi.prompte_templates.schema import PromptTemplate


class PromptTemplates:
    def __init__(self, url: str, api_key: str):
        self.__client = HttpClient(
            url=url,
            api_key=api_key,
            api_prefix=f"/api/v1/prompt-templates"
        )

    def create(self, name: str, prompt_template: str, description: Optional[str] = None) -> PromptTemplate:
        """
        Create a new prompt template.
        :param name: The name of the prompt template.
        :param prompt_template: The prompt template string
        :param description: A description of the prompt template.


        Example:
        ```
        >>> from vendi import Vendi
        >>> client = Vendi(api_key="my_api_key")
        >>> template = client.prompt_templates.create(
        ...     name="My Prompt Template",
        ...     prompt_template="Given the following conversation between a customer and a support agent, write a response from the support agent. {chat_history}",
        ...     description="This prompt template is used to generate prompts for the support agent response task."
        ... )
        """
        res = self.__client.post(
            uri=f"/create",
            json_data={
                "name": name,
                "description": description,
                "prompt_template": prompt_template,
            },
        )
        return PromptTemplate(**res)

    def get(self, template_id: str) -> PromptTemplate:
        """
        Get a prompt template by ID.
        """
        res = self.__client.get(uri=f"/{template_id}")
        return PromptTemplate(**res)

    def list(self) -> List[PromptTemplate]:
        """
        List all prompt templates available to the user.
        """
        res = self.__client.get(uri=f"/")
        return [PromptTemplate(**prompt_template) for prompt_template in res]

    def delete(self, template_id: str) -> bool:
        """
        Delete a prompt template by ID.
        """
        res = self.__client.delete(uri=f"/{template_id}")
        return res

    def update(self, template_id: str, name: Optional[str] = None, prompt_template: Optional[str] = None) -> PromptTemplate:
        """
        Update a prompt template content by ID.
        :param template_id: The ID of the prompt template to update.
        :param name: The name of the prompt template.
        :param prompt_template: The prompt template string
        """
        res = self.__client.patch(
            uri=f"/{template_id}",
            json_data={
                "name": name,
                "prompt_template": prompt_template,
            },
        )
        return PromptTemplate(**res)