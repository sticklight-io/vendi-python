from pydantic import BaseModel, ConfigDict

from vendi.core.schema import SchemaMixin
from vendi.endpoints.schema import EndpointInfo
from vendi.models.schema import ModelInfo, ModelProvider


class CreateProviderSchema(BaseModel):
    name: ModelProvider
    """The name of the provider."""
    config: dict | None = {}
    """The configuration of the provider."""


class Provider(CreateProviderSchema, SchemaMixin):
    models: list[ModelInfo] = []
    """The models that are available for the provider."""
    endpoints: list[EndpointInfo] = []
    """The endpoints that are available for the provider. Endpoint is the interface that the provider exposes to 
    generate predictions"""
    model_config = ConfigDict(
        protected_namespaces=(),
    )
