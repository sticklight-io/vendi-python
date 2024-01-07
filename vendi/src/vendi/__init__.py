"""
Vendi is a Python client for the Vendi API. It provides a convenient way to access the Vendi API from a Python application.
This is the main entrypoint for the Vendi SDK.
"""
from vendi.core.config import vendi_config
from vendi.datasets import Datasets
from vendi.endpoints import Endpoints
from vendi.prompte_templates.prompt_templates import PromptTemplates
from vendi.deployments.deployments import Deployments
from vendi.evaluations.evaluation import Evaluations
from vendi.models import Models
from vendi.completions import Completions
from vendi.providers import Providers

VENDI_API_URL = vendi_config.VENDI_API_URL


class VendiClient:
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
        self.evaluations = Evaluations(url=self._base_url, api_key=self.api_key)
        self.datasets = Datasets(url=self._base_url, api_key=self.api_key)
        self.prompt_templates = PromptTemplates(url=self._base_url, api_key=self.api_key)
        self.completions = Completions(url=self._base_url, api_key=self.api_key)
        self.providers = Providers(url=self._base_url, api_key=self.api_key)
        self.endpoints = Endpoints(url=self._base_url, api_key=self.api_key)
