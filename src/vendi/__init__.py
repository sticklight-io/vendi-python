"""
Vendi is a Python client for the Vendi API. It provides a convenient way to access the Vendi API from a Python application.
This is the main entrypoint for the Vendi SDK.
"""
from vendi.core.config import vendi_config
from vendi.datasets import Datasets
from vendi.finetune import Finetune
from vendi.deployments.deployments import Deployments
from vendi.models import Models
from vendi.completions import Completions

VENDI_API_URL = vendi_config.VENDI_API_URL


class Vendi:
    def __init__(
        self,
        *,
        api_url: str | None = None,
        api_key: str | None = None,
    ):
        self._base_url = api_url or vendi_config.VENDI_API_URL

        if api_key:
            self.api_key = api_key
        else:
            self.api_key = vendi_config.VENDI_API_KEY

        self.models = Models(url=self._base_url, api_key=self.api_key)
        self.deployments = Deployments(url=self._base_url, api_key=self.api_key)
        self.datasets = Datasets(url=self._base_url, api_key=self.api_key)
        self.completions = Completions(url=self._base_url, api_key=self.api_key)
        self.finetune = Finetune(url=self._base_url, api_key=self.api_key)
