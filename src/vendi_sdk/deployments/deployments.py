from typing import List

from vendi_sdk.core.http_client import HttpClient

from .schema import Deployment, DeploymentStatus


class Deployments:
    def __init__(self, url: str, api_key: str):
        self.__api_key = api_key

        self.__client = HttpClient(
            url=url,
            api_key=api_key,
            api_prefix=f"/v1/"
        )

    def list(self) -> list[Deployment]:
        """
        Get a list of the deployments available to the user
        """
        res = self.__client.get(uri=f"deployments/")
        return [Deployment(**deployment) for deployment in res]

    def list_private(self) -> List[Deployment]:
        """
        Get a list of the private deployments available to the user
        """
        res = self.__client.get(uri=f"deployments/")
        return [Deployment(**deployment) for deployment in res]

    def get(self, deployment_id: str) -> Deployment:
        """
        Get deployment metadata by ID
        :param deployment_id: The ID of the deployment to get
        :return: The deployment metadata
        """
        res = self.__client.get(uri=f"deployments/{deployment_id}")
        return Deployment(**res)

    def delete(self, deployment_id: str) -> bool:
        """
        Delete a deployment by ID
        :param deployment_id: The ID of the deployment to delete
        :return: True if the deployment was deleted successfully
        """
        res = self.__client.delete(uri=f"deployments/{deployment_id}")
        return res

    def create(
        self,
        name: str,
        model_name: str,
        model_id: str,
        backend: str,
        dtype: str,
        gpu_memory_utilization: float,
        max_model_len: int,
        scale_to_zero: bool = True,
        scale_to_zero_timeout_seconds: int = 900,
        quantization: str = None,
    ) -> Deployment:
        """
        Create a deployment on vendi with the given parameters
        :param name: The name of the deployment
        :param model_name: The name of the model to deploy. This model must be registered with vendi models and available to the user when running
        vendi.models.list().
        :param model_id: The ID of the model to deploy. This model must be registered with vendi models and available to the user when running
        :param backend: The backend to use for the deployment. Please see the vendi documentation for a list of supported backends.
        :param dtype: The data type to use for the deployment. Please see the vendi documentation for a list of supported data types.
        :param gpu_memory_utilization: The percentage of GPU memory to use for the deployment. This value must be between 0 and 1.
        :param max_model_len: The maximum length of the model to use for the deployment. This value must be between 0 and inf.
        :param scale_to_zero: Whether or not to scale the deployment to zero when it is not in use. This value must be a boolean.
        A deployment not in use is defined by the deployment not receiving any requests for the scale_to_zero_timeout_seconds.
        :param scale_to_zero_timeout_seconds: The number of seconds to wait before scaling the deployment to zero when it is not in use.
        This value must be between 0 and inf.
        :param quantization: The quantization to use for the deployment. Please see the vendi documentation for a list of supported quantizations.
        :return: The created deployment metadata
        """
        res = self.__client.post(
            uri=f"deployments/create/",
            json_data={
                "name": name,
                "model_configuration": {
                    "model_name": model_name,
                    "backend": backend,
                    "dtype": dtype,
                    "gpu_memory_utilization": str(gpu_memory_utilization),
                    "max_model_len": str(max_model_len),
                    "quantization": quantization,
                },
                "model_id": model_id,
                "scale_to_zero": scale_to_zero,
                "scale_to_zero_timeout_seconds": scale_to_zero_timeout_seconds,
            },
        )
        return Deployment(**res)

    def update(
        self,
        deployment_id: str,
        scale_to_zero: bool | None = None,
        scale_to_zero_timeout_seconds: int | None = None,
    ) -> Deployment:
        """
        Update a deployment on vendi with the given parameters
        :param deployment_id: The ID of the deployment to update
        :param scale_to_zero: Whether or not to scale the deployment to zero when it is not in use. This value must be a boolean.
        A deployment not in use is defined by the deployment not receiving any requests for the scale_to_zero_timeout_seconds.
        :param scale_to_zero_timeout_seconds: The number of seconds to wait before scaling the deployment to zero when it is not in use.
        This value must be between 0 and inf.
        :return: The updated deployment metadata
        """
        res = self.__client.patch(
            uri=f"deployments/{deployment_id}",
            json_data={
                "scale_to_zero": scale_to_zero,
                "scale_to_zero_timeout_seconds": scale_to_zero_timeout_seconds,
            },
        )
        return Deployment(**res)

    def start(
        self,
        deployment_id: str,
    ) -> Deployment:
        """
        Start a deployment by ID from a stopped state
        :param deployment_id: The ID of the deployment to start
        :return: The updated deployment metadata
        """
        res = self.__client.post(
            uri=f"deployments/{deployment_id}/start",
        )
        return Deployment(**res)

    def stop(
        self,
        deployment_id: str,
    ) -> Deployment:
        """
        Stop a deployment by ID from a started state
        :param deployment_id: The ID of the deployment to stop
        :return: The updated deployment metadata
        """
        res = self.__client.post(
            uri=f"deployments/{deployment_id}/stop",
        )
        return Deployment(**res)

    def status(self, deployment_id: str) -> DeploymentStatus:
        """
        Get the status of a deployment
        :param deployment_id: The ID of the deployment to get the status of
        :return: The status of the deployment
        """
        res = self.__client.get(uri=f"deployments/{deployment_id}")
        return res["status"]
