import uuid
from enum import Enum

from pydantic import BaseModel

from vendi.core.schema import SchemaMixin
from vendi.deployments.schema import DeploymentStatus


class UsableEndpoint(BaseModel):
    id: uuid.UUID | str
    """The ID of the endpoint."""
    name: str
    """The name of the endpoint. This name is derived from the name of the model."""
    status: str | None = None


class EndpointType(str, Enum):
    MODEL = "model"
    """A model endpoint is an endpoint that serves predictions be vendi base models"""
    FINE_TUNE = "fine_tune"
    """A fine-tune endpoint is an endpoint that serves predictions by a fine-tuned model created with vendi"""
    EXTERNAL = "external"
    """An external endpoint is an endpoint that serves predictions by an external model"""


class CreateEndpointSchema(SchemaMixin):
    name: str
    """The name of the endpoint."""
    is_public: bool = False
    """Whether the endpoint is public or not. A public endpoint is available to all vendi's customers"""
    type_: EndpointType
    """The type of the endpoint. This value must be one EndpointType."""
    deployment_id: uuid.UUID | None = None  # For model endpoints
    """
    The ID of the deployment to use for the endpoint. This value must be the ID of a deployment that is live and ready to be used.
    Each endpoint must be associated with a single deployment.
    """
    model_id: uuid.UUID | None = None  # For fine-tune endpoints
    """The ID of the model to use for the endpoint. This value shows the model id that runs within the deployment id."""


class Endpoint(CreateEndpointSchema):
    provider: str | None = None
    """The provider of the endpoint. vendi/openai/google/etc.."""
    status: DeploymentStatus | None = None
    """The status of the endpoint. A replica of the deployment id status"""
