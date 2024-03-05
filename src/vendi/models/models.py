from vendi.core.http_client import HttpClient
from vendi.models.schema import Model, HuggingFaceModel, ModelProvider


class Models:
    def __init__(self, url: str, api_key: str):
        self.__client = HttpClient(
            url=url,
            api_key=api_key,
            api_prefix=f"/platform/v1/models"
        )

    # def create(self, name: str, model: Model):
    #     pass

    def import_model(
        self,
        model_name: str,
        model_provider: ModelProvider,
    ) -> Model:
        """
        Relevant only for Self-hosted customers.
        Import a model from any of the supported model providers.
        For huggingface, pass the model card name as the model_name.
        """
        res = self.__client.post(
            uri=f"/import",
            json_data={
                "model_name": model_name,
                "model_provider": model_provider,
            },
        )
        return Model(**res)

    def get(self, model_id: str):
        """
        Get mode metadata by ID
        """
        res = self.__client.get(uri=f"/{model_id}")
        return Model(**res)

    def list(self):
        """
        List all models available to the user
        """
        res = self.__client.get(uri=f"/")
        return [Model(**model) for model in res]

    def delete(self, model_id: str) -> bool:
        """
        Delete a model by ID
        """
        res = self.__client.delete(uri=f"/{model_id}")
        return res

    def set_public(self, model_id: str, status: bool) -> bool:
        """
        Set the public status of a model so that all vendi customers can use it.
        """
        res = self.__client.post(uri=f"/{model_id}/set-public/{status}")
        return res

    def get_huggingface_model(self, hf_model_name: str) -> HuggingFaceModel:
        """
        Get metadata information about a huggingface model card.
        :param hf_model_name: The model card name
        """
        res = self.__client.post(uri=f"/huggingface/get", json_data={"hf_model_name": hf_model_name})
        return HuggingFaceModel(**res)
