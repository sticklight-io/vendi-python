import uuid
from enum import Enum
from typing import Callable, Any

import pandas as pd
from pydantic import BaseModel

from vendi_sdk.core.schema import SchemaMixin


class DatasetType(str, Enum):
    RAW = "raw"
    """A raw dataset is a dataset that has not been processed in any way. It is the most basic form of a dataset with random structure/dataset column names"""
    CONVERSATION = "conversation"
    """A conversation dataset is a dataset has a 'messages' key where each 'message' has 'role' and 'content' keys"""


class Dataset(SchemaMixin):
    name: str
    """The name of the dataset."""
    path: str
    """The path of the dataset."""
    storage: str | None = None
    """The storage the dataset is stored in."""
    _data: Any = None
    """The dataset data, only available after calling `load_data()`."""
    load_data: Callable[[], Any] | None = None
    """The function to call to load the dataset data. Populated after calling `get()` or `list()`."""

    @property
    def data(self) -> pd.DataFrame:
        """
        Get the dataset data as a pandas DataFrame
        """
        if self._data is None:
            raise ValueError("Dataset data is not loaded, run `load_data()` first")
        return self._data
