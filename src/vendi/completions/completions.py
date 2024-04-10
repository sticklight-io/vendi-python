import asyncio
import time
import uuid
from typing import List, Dict, Optional

from vendi.completions.schema import ChatCompletion, ModelParameters, BatchInference, BatchInferenceStatus, \
    CompletionRequest, Endpoint, VendiCompletionResponse
from vendi.core.ahttp_client import AsyncHTTPClient
from vendi.core.http_client import HttpClient


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
        )
        self.__aclient = AsyncHTTPClient(
            base_url=url,
        )
        self.__aclient.set_auth_header(api_key)

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
        checkpoint: str | None = None,
        request_id: str = None,
        openai_compatible: bool = False,
        extra_body: Optional[Dict] = None,
        extra_headers: Optional[Dict] = None,
    ) -> VendiCompletionResponse | ChatCompletion:
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
        See https://docs.vendi-ai.com/docs/completions-api#json-schema for more information
        :param regex: The regex to use for the completion (either this or json_schema should be provided)
        See https://docs.vendi-ai.com/docs/completions-api#regex for more information
        :param checkpoint: The checkpoint to use for the completion (either "latest" or a specific checkpoint ID for lora adapters)
        :param request_id: The request ID to use for the completion (optional)
        :param openai_compatible: Whether to return the response in OpenAI compatible format or the vendi full response format
        :param extra_body: Extra body parameters to include in the request body
        :param extra_headers: Extra headers to include in the request
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
            "checkpoint": checkpoint,
            "request_id": request_id,
            "openai_compatible": openai_compatible,
        }
        if extra_body:
            data.update(extra_body)

        if stop is not None:
            data["stop"] = stop

        _res = self.__client.post(
            uri=f"/v1/chat/completions/",
            json_data=data,
            headers=extra_headers
        )

        if openai_compatible:
            return ChatCompletion(**_res)
        return VendiCompletionResponse(**_res)

    async def acreate(
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
        checkpoint: str | None = None,
        request_id: str = None,
        openai_compatible: bool = False,
        extra_body: Optional[Dict] = None,
        extra_headers: Optional[Dict] = None,
    ) -> VendiCompletionResponse | ChatCompletion:
        """
        Same documentation as completions.create but with async operation
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
            "checkpoint": checkpoint,
            "request_id": request_id,
            "openai_compatible": openai_compatible,
        }

        if extra_body:
            data.update(extra_body)

        if stop is not None:
            data["stop"] = stop

        _res = await self.__aclient.post(
            path=f"/v1/chat/completions/",
            json=data,
            headers=extra_headers
        )
        if openai_compatible:
            return ChatCompletion(**_res)
        return VendiCompletionResponse(**_res)

    async def acreate_many(
        self,
        requests: list[CompletionRequest],
    ) -> List[ChatCompletion] | List[VendiCompletionResponse]:
        """
        Create multiple completions on different models with the same prompt and parameters
        requests: A list of completionr requests
        Examples:
        >>> import uuid
        >>> from vendi.completions.schema import CompletionRequest
        >>> from vendi import Vendi
        >>>
        >>> client = Vendi(api_key="my-api-key")
        >>> completions = asyncio.run(client.completions.acreate_many(
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
        >>>     )
        >>> )
        """

        tasks = [
            self.acreate(
                **request.model_dump(),
            ) for request in requests
        ]

        res = await asyncio.gather(*tasks)
        return res

    def available_endpoints(self) -> List[Endpoint]:
        """
        Get the list of available endpoints , those that are configured and ready to use
        :return: The list of available endpoints
        """
        _endpoints = self.__client.get(uri="/platform/v1/inference/endpoints")
        return [Endpoint(**endpoint) for endpoint in _endpoints]

    def endpoints_catalog(self) -> List[Endpoint]:
        """
        Get the list of all supported endpoints within the platform
        :return: The list of all supported endpoints
        """
        _endpoints = self.__client.get(uri="/platform/v1/inference/endpoints/all")
        return [Endpoint(**endpoint) for endpoint in _endpoints]

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

    async def arun_batch_job(
        self,
        dataset_id: uuid.UUID,
        model_parameters: list[ModelParameters],
        wait_until_complete: bool = False,
        timeout: int = 3000,
        poll_interval: int = 5,
    ) -> BatchInference:
        _res = await self.__aclient.post(
            path="/platform/v1/inference/batch/",
            json={
                "dataset_id": str(dataset_id),
                "model_parameters": [{**i.model_dump(), **i.model_extra} for i in model_parameters]
            }
        )
        job = BatchInference(**_res)

        if wait_until_complete:
            start_time = time.time()
            while True:
                job = await self._aget_batch_job(job.id)
                if job.status in [BatchInferenceStatus.COMPLETED, BatchInferenceStatus.FAILED]:
                    return job
                if time.time() - start_time > timeout:
                    raise TimeoutError(
                        "The batch job did not complete within the specified timeout. "
                        "You can still check its status by using the batch_job_status method.")

                await asyncio.sleep(poll_interval)

    def __post_batch_job(self, dataset_id: uuid.UUID, model_parameters: list[ModelParameters]) -> BatchInference:
        res = self.__client.post(
            uri="/platform/v1/inference/batch/",
            json_data={
                "dataset_id": str(dataset_id),
                "model_parameters": [{**i.model_dump(), **i.model_extra} for i in model_parameters]
            }
        )

        return BatchInference(**res)

    def batch_job_status(self, job_id: uuid.UUID) -> BatchInferenceStatus:
        """
        Returns the status of a batch inference job.
        """
        job = self._get_batch_job(job_id)
        return job.status

    def _get_batch_job(self, batch_inference_id: uuid.UUID) -> BatchInference:
        """
        Get a batch inference object job by ID
        """
        res = self.__client.get(
            uri=f"/platform/v1/inference/batch/{batch_inference_id}"
        )
        return BatchInference(**res)

    async def _aget_batch_job(self, batch_inference_id: uuid.UUID) -> BatchInference:
        """
        Get a batch inference object job by ID
        """
        res = await self.__aclient.get(
            path=f"/platform/v1/inference/batch/{batch_inference_id}"
        )
        return BatchInference(**res)

    def list_batch_jobs(self) -> List[BatchInference]:
        """
        Get all batch inferences
        """
        res = self.__client.get(
            uri="/platform/v1/inference/batch/"
        )
        return [BatchInference(**i) for i in res]

    def delete_batch_job(self, batch_id: uuid.UUID):
        """
        Delete a batch inference job
        """
        return self.__client.delete(f"/platform/v1/inference/batch/{batch_id}")
