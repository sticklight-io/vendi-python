import json
import logging
import uuid
from typing import List, Dict, Union, Optional

import pandas as pd

from vendi.core.http_client import HttpClient
from vendi.datasets.schema import Dataset, DatasetType

logger = logging.getLogger(__name__)


class Datasets:
    """
    Datasets is the client to interact with the datasets endpoint of the Vendi API.
    """

    def __init__(self, url: str, api_key: str):
        self.__client = HttpClient(
            url=url,
            api_key=api_key,
            api_prefix=f"/api/v1/datasets"
        )

    def get(self, dataset_id: str) -> Dataset:
        """
        Get dataset metadata by ID
        :param dataset_id: The ID of the dataset to get
        """
        res = self.__client.get(uri=f"/{dataset_id}")
        dataset = Dataset(**res)

        def load_data() -> pd.DataFrame:
            """
            Download and load the dataset data into a pandas DataFrame
            """
            data = self.__client.get(uri=f"/{dataset_id}/data")
            dataset._data = pd.DataFrame(data['data'])
            return dataset.data

        dataset.load_data = load_data
        return dataset

    def list(self) -> list[Dataset]:
        """
        Get a list of the datasets available to the user
        :return: A list of datasets metadata
        """
        res = self.__client.get(uri=f"/")
        return [Dataset(**dataset) for dataset in res]

    def delete(self, dataset_id: str) -> None:
        """
        Delete a dataset by ID
        :param dataset_id: The ID of the dataset to delete
        """
        res = self.__client.delete(uri=f"/{dataset_id}")
        return res

    def upload(
        self,
        name: str,
        data: Optional[List[dict]] = None,
        data_path: Optional[str] = None,
        tags: Union[Dict, None] = None,
        path: Union[str, None] = None,
        dataset_type: Union[DatasetType, None] = None,
    ) -> Dataset:
        """
        Upload a dataset to the Vendi API
        :param name: The name of the dataset
        :param data: The data to upload. Should be a valid list of JSON objects
        :param data_path: The path to the data to upload. Should be a valid path to a JSON file
        :param tags: The tags to apply to the dataset. Should be a dictionary of key/value pairs. For example:
        {"version": "v3", "language": "en"}
        :param path: The path to the dataset. Should be a string, for example: "datasets/financial". Defaults to None
        :param dataset_type: The type of dataset to upload. Should be a DatasetType enum value.
        If the dataset is a conversation dataset, with 'messages' key use "conversation". If the dataset is a raw dataset columns, use "raw"
        :return: The ID of the uploaded dataset

        """
        if not data and not data_path:
            raise ValueError("You must provide either data or data_path when uploading data")

        if data_path:
            with open(data_path, "r") as f:
                try:
                    data = [json.loads(line) for line in f.read().splitlines()]
                except json.decoder.JSONDecodeError:
                    raise ValueError(f"Could not parse JSON from {data_path} file. The file must be a valid JSONL file")

        if tags is None:
            tags = {}
        str_data = ""
        for row in data:
            str_data += json.dumps(row) + "\n"

        if not dataset_type:
            if "messages" in data[0]:
                dataset_type = DatasetType.CONVERSATION
                logger.info("Detected conversation dataset, since there is a 'messages' key in the data")
            else:
                dataset_type = DatasetType.RAW
                logger.info("Detected raw dataset")

        res = self.__client.post(
            uri=f"/upload",
            json_data={
                "name": f"{name}.jsonl",
                "type": dataset_type,
                "tags": tags,
                "data": str_data,
                "path": path,
            }
        )
        return Dataset(**res)

    def generate_download_link(self, dataset_id: str) -> str:
        """
        Generate a download link for a dataset
        :param dataset_id: The ID of the dataset to download
        :return: The download link
        """
        res = self.__client.get(uri=f"/{dataset_id}/download-link")
        return res
