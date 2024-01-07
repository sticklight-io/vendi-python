from typing import List

from vendi.core.http_client import HttpClient
from vendi.models.schema import ModelProvider
from vendi.providers.schema import Provider


class Providers:
    def __init__(self, url: str, api_key: str):
        self.__client = HttpClient(
            url=url,
            api_key=api_key,
            api_prefix=f"/api/v1/providers"
        )

    def list(self) -> List[Provider]:
        """
        List all providers available to the user
        """
        res = self.__client.get(uri=f"/instances")
        return [Provider(**provider) for provider in res]

    def get(self, provider_name: ModelProvider) -> Provider:
        """
        Get provider metadata by name. Providers metadata containsthe provider configuration
        """
        res = self.__client.get(uri=f"/{provider_name}/instance")
        return Provider(**res)

    def create(self, provider_name: ModelProvider, config: dict) -> Provider:
        """
        Create a new provider instance

        For openai, the config looks like:
        {
            "api_key": "sk-1234567890"
        }

        If you are not sure use the get_provider_schema() method to get the schema.

        :param provider_name: any of the supported providers
        :param config: the provider configuration
        :return: the provider instance
        """

        res = self.__client.patch(uri=f"/{provider_name}/instance", json_data={"config": config})
        return Provider(**res)

    def get_provider_schema(self, provider_name: ModelProvider) -> dict:
        """
        Get the provider configuration schema that should be used to create a new provider instance.
        """
        res = self.__client.get(uri=f"/{provider_name}/schema")
        return res

    def delete(self, provider_name: ModelProvider) -> bool:
        """
        Delete a provider instance by name
        """
        return self.__client.delete(uri=f"/{provider_name}/instance")
