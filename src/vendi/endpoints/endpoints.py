from typing import List

from vendi.core.http_client import HttpClient
from vendi.endpoints.schema import Endpoint


class Endpoints:
    def __init__(self, url: str, api_key: str):
        self.__client = HttpClient(
            url=url,
            api_key=api_key,
            api_prefix=f"/api/v1/endpoints"
        )

    def list(self) -> List[Endpoint]:
        """
        Get a list of the endpoints available to the user
        """
        res = self.__client.get(uri=f"/")
        return [Endpoint(**endpoint) for endpoint in res]

    def get(self, endpoint_id: str) -> Endpoint:
        """
        Get a single endpoint by ID
        """
        res = self.__client.get(uri=f"/{endpoint_id}")
        return Endpoint(**res)

    def set_public(self, endpoint_id: str, is_public: bool) -> bool:
        """
        Set the public status of an endpoint
        A public endpoint is accessible to any authenticated user in the world through the Vendi API.
        """
        res = self.__client.post(uri=f"/{endpoint_id}/set-public/{is_public}")
        return res

    def delete(self, endpoint_id: str) -> bool:
        """
        Delete an endpoint by ID
        """
        return self.__client.delete(uri=f"/{endpoint_id}")
