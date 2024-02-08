import time
import uuid
from typing import List, Dict, Optional

from vendi.completions.schema import ChatCompletion, ModelParameters, BatchInference, BatchInferenceStatus, LlmMessage, \
    CompletionRequest
from vendi.core.http_client import HttpClient
from vendi.endpoints.schema import EndpointInfo
from vendi.models.schema import ModelProvider


class Completions:
    """
    Completions is the client to interact with the completions endpoint of the Vendi API.
    """

    def __init__(self, url: str, api_key: str):
        """
        Initialize the Completions client
        :param url: The URL of the Vendi API
        :param api_key: The API key to use for authentication
        """
        self.__api_key = api_key
        self.__client = HttpClient(
            url=url,
            api_key=api_key,
            api_prefix=f"/api/v1/providers/"
        )

    def create(
        self,
        model: str,
        messages: List[Dict[str, str]],
        frequency_penalty: Optional[float] = 0,
        presence_penalty: Optional[float] = 0.5,
        max_tokens: Optional[int] = 256,
        stop: Optional[List[str]] = None,
        n: Optional[int] = 1,
        top_p: Optional[float] = 1,
        top_k: Optional[int] = 40,
        temperature: Optional[float] = 0.7,
        json_schema: Optional[str] = None,
        regex: Optional[str] = None,
    ) -> ChatCompletion:
        """
        Create a completion on a language model with the given parameters
        :param model: The ID of the language model to use for the completion. Should be in the format of <provider>/<model_id>
        :param messages: The messages to use as the prompt for the completion
        :param frequency_penalty: The frequency penalty to use for the completion
        :param presence_penalty: The presence penalty to use for the completion
        :param max_tokens: The maximum number of tokens to generate for the completion
        :param stop: The stop condition to use for the completion
        :param n: The number of completions to generate
        :param top_p: The top p value to use for the completion
        :param top_k: The top k value to use for the completion
        :param temperature: The temperature value to use for the completion
        :param json_schema: The JSON schema to use for the completion (either this or regex should be provided) .
        See https://docs.vendi.ai/docs/completions-api#json-schema for more information
        :param regex: The regex to use for the completion (either this or json_schema should be provided)
        See https://docs.vendi.ai/docs/completions-api#regex for more information
        :return: The generated completion

        """
        data = {
            "messages": messages,
            "model": model,
            "frequency_penalty": frequency_penalty,
            "presence_penalty": presence_penalty,
            "max_tokens": max_tokens,
            "n": n,
            "top_p": top_p,
            "top_k": top_k,
            "temperature": temperature,
            "json_schema": json_schema,
            "regex": regex,
        }

        if stop is not None:
            data["stop"] = stop

        res = self.__client.post(
            uri=f"completions/",
            json_data=data
        )
        return ChatCompletion(**res)

    def create_many_prompts(
        self,
        model,
        conversations: List[List[Dict[str, str]]],
        frequency_penalty: Optional[float] = 0,
        presence_penalty: Optional[float] = 0,
        max_tokens: Optional[int] = 256,
        stop: Optional[List[str]] = None,
        n: Optional[int] = 1,
        top_p: Optional[float] = 1,
        top_k: Optional[int] = 40,
        temperature: Optional[float] = 0.7,
    ) -> List[ChatCompletion]:
        """
        Create multiple completions on the same model with different prompts, while keeping the same parameters
        :param model: The ID of the language model to use for the completion. Should be in the format of <provider>/<model_id>
        :param conversations: A batch of multiple prompt messages to use for the completions
        :param frequency_penalty: The frequency penalty to use for the completion
        :param presence_penalty: The presence penalty to use for the completion
        :param max_tokens: The maximum number of tokens to generate for the completion
        :param stop: The stop condition to use for the completion
        :param n: The number of completions to generate
        :param top_p: The top p value to use for the completion
        :param top_k: The top k value to use for the completion
        :param temperature: The temperature value to use for the completion
        :return: The generated completions

        Examples:
        >>> from vendi import Vendi
        >>> client = Vendi(api_key="my-api-key")
        >>> completions = client.completions.create_many_prompts(
        >>>     model="vendi/mistral-7b-instruct-v2",
        >>>     conversations=[
        >>>         [
        >>>             {
        >>>                 "role": "user",
        >>>                 "content": "Hello"
        >>>             }
        >>>     ],
        >>>     [
        >>>             {
        >>>                 "role": "user",
        >>>                 "content": "Hello what's up with you?"
        >>>            }
        >>>            ]
        >>>     ],
        >>> )

        """

        requests_body = [
            {
                "messages": message,
                "model": model,
                "frequency_penalty": frequency_penalty,
                "presence_penalty": presence_penalty,
                "max_tokens": max_tokens,
                "n": n,
                "top_p": top_p,
                "top_k": top_k,
                "temperature": temperature,
            }
            for message in conversations
        ]

        if stop is not None:
            for req in requests_body:
                req["stop"] = stop

        res = self.__client.post(
            uri=f"completions-many",
            json_data=
            {
                "requests": requests_body
            }
        )
        return [ChatCompletion(**completion) for completion in res]

    def create_many(
        self,
        requests: list[CompletionRequest],
    ) -> List[ChatCompletion]:
        """
        Create multiple completions on different models with the same prompt and parameters
        requests: A list of tuples, where each tuple contains the model parameters and the prompt messages
        Examples:
        >>> import uuid
        >>> from vendi.completions.schema import CompletionRequest
        >>> from vendi import Vendi
        >>>
        >>> client = Vendi(api_key="my-api-key")
        >>> completions = client.completions.create_many(
        >>>     requests=[
        >>>         CompletionRequest(
        >>>             model="openai/gpt-3.5-turbo",
        >>>             messages=[
        >>>                 {"role": "user", "content": "Hey how are you?"}
        >>>             ],
        >>>             request_id=str(uuid.uuid4()),
        >>>         ),
        >>>         CompletionRequest(
        >>>             model="openai/gpt-4",
        >>>             messages=[
        >>>                 {"role": "user", "content": "Hi whats up?"}
        >>>             ],
        >>>             request_id=str(uuid.uuid4()),
        >>>         ),
        >>>     ]
        >>> )
        """

        res = self.__client.post(
            uri=f"completions-many/",
            json_data=
            {
                "requests": [i.model_dump() for i in requests]
            }
        )
        return [ChatCompletion(**completion) for completion in res]

    def create_many_models(
        self,
        models: List[str],
        messages: List[Dict[str, str]],
        frequency_penalty: Optional[float] = 0,
        presence_penalty: Optional[float] = 0,
        max_tokens: Optional[int] = 256,
        stop: Optional[List[str]] = None,
        n: Optional[int] = 1,
        top_p: Optional[float] = 1,
        top_k: Optional[int] = 40,
        temperature: Optional[float] = 0.7,
    ) -> List[ChatCompletion]:
        """
        Create multiple completions on different models with the same prompt and parameters
        :param models: A list of models to use for the completions. Each model should be in the format of <provider>/<model_id>
        :param messages: The messages to use as the prompt for the completions
        :param frequency_penalty: The frequency penalty to use for the completions
        :param presence_penalty: The presence penalty to use for the completions
        :param max_tokens: The maximum number of tokens to generate for the completions
        :param stop: The stop condition to use for the completions
        :param n: The number of completions to generate
        :param top_p: The top p value to use for the completions
        :param top_k: The top k value to use for the completions
        :param temperature: The temperature value to use for the completions
        :return: The generated completions

        Examples:
        >>> from vendi import Vendi
        >>> client = Vendi(api_key="my-api-key")
        >>> completions = client.completions.create_many(
        >>>     models=[
        >>>         "vendi/mistral-7b-instruct-v2",
        >>>         "openai/gpt-3.5-turbo",
        >>>         "openai/gpt4",
        >>>     ],
        >>>     messages=[
        >>>         {
        >>>             "role": "user",
        >>>             "content": "Hello"
        >>>         }
        >>>     ]
        >>> )
        """

        requests_body = [
            {
                "messages": messages,
                "model": model,
                "frequency_penalty": frequency_penalty,
                "presence_penalty": presence_penalty,
                "max_tokens": max_tokens,
                "n": n,
                "top_p": top_p,
                "top_k": top_k,
                "temperature": temperature,
            }
            for model in models
        ]

        if stop is not None:
            for req in requests_body:
                req["stop"] = stop

        res = self.__client.post(
            uri=f"completions-many/",
            json_data=
            {
                "requests": requests_body
            }
        )
        return [ChatCompletion(**completion) for completion in res]

    def available_endpoints(self, provider: ModelProvider) -> List[EndpointInfo]:
        """
        Get the list of available endpoints for the completions API
        :return: The list of available endpoints
        """
        res = self.__client.get(uri=f"{provider}/endpoints")
        return [EndpointInfo(**endpoint) for endpoint in res[provider]]

    def run_batch_job(
        self,
        dataset_id: uuid.UUID,
        model_parameters: list[ModelParameters],
        wait_until_complete: bool = False,
        timeout: int = 3000,
        poll_interval: int = 5,
    ) -> BatchInference:
        """
        Run a batch inference job on a dataset using the specified models .
        :param dataset_id: The ID of the dataset to run the batch inference on
        :param model_parameters: The list of model parameters to use for the batch inference
        :param wait_until_complete: Whether to wait until the batch inference job is complete before continuing
        :param timeout: The maximum time to wait in the client for the batch inference job to complete, in seconds. Valid only if wait_until_complete is True
        :param poll_interval: The interval at which to poll the batch inference job status, in seconds . Valid only if wait_until_complete is True
        :return: The batch inference job
        """

        job = self.__post_batch_job(dataset_id, model_parameters)
        if wait_until_complete:
            start_time = time.time()
            while True:
                status = self.batch_job_status(job.id)
                if status in [BatchInferenceStatus.COMPLETED, BatchInferenceStatus.FAILED]:
                    return job
                if time.time() - start_time > timeout:
                    raise TimeoutError(
                        "The batch job did not complete within the specified timeout. "
                        "You can still check its status by using the batch_job_status method.")

                time.sleep(poll_interval)
        return job

    def __post_batch_job(self, dataset_id: uuid.UUID, model_parameters: list[ModelParameters]) -> BatchInference:
        res = self.__client.post(
            uri="batch_dataset_inference/",
            json_data={
                "dataset_id": str(dataset_id),
                "model_parameters": [i.model_dump() for i in model_parameters]
            }
        )

        return BatchInference(**res)

    def batch_job_status(self, job_id: uuid.UUID) -> BatchInferenceStatus:
        """
        Returns the status of a batch inference job.
        """
        job = self.get_batch_job(job_id)
        return job.status

    def get_batch_job(self, batch_inference_id: uuid.UUID) -> BatchInference:
        """
        Get a batch inference object job by ID
        """
        res = self.__client.get(
            uri=f"batch_dataset_inference/{batch_inference_id}"
        )
        return BatchInference(**res)
