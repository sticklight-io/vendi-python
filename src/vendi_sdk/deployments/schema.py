import uuid
from enum import Enum
from typing import Literal

from pydantic import BaseModel, ConfigDict

from vendi_sdk.core.schema import SchemaMixin


class DeploymentStatus(str, Enum):
    LIVE = "LIVE"
    """The deployment is live and ready to be used."""
    DOES_NOT_EXIST = "DOES_NOT_EXIST"
    """The deployment does not exist."""
    ERROR = "ERROR"
    """The deployment is in an error state."""
    UNKNOWN = "UNKNOWN"
    """The deployment is in an unknown state."""
    STOPPED = "STOPPED"
    """The deployment is stopped and not ready to be used."""
    STOPPING = "STOPPING"
    """The deployment is being stopped. This is a temporary state."""
    NOT_READY = "NOT_READY"
    """The deployment is not ready yet to be used."""


class DeploymentConfig(BaseModel):
    name: str
    """The name of the deployment."""
    namespace: str
    """The namespace of the deployment in the cluster."""
    version: str
    """The image version of the deployment."""
    scale_to_zero: bool
    """Whether or not to scale the deployment to zero when it is not in use. This value must be a boolean."""
    scale_to_zero_timeout_seconds: int
    """The number of seconds to wait before scaling the deployment to zero when it is not in use. This value must be between 0 and inf."""


class ModelConfig(BaseModel):
    model_name: str
    """The name of the model to deploy."""
    backend: Literal["pt", "ctranslate", "vllm", "gguf"] = "pt"
    """The backend to use for the model."""
    dtype: str = "float16"
    """The data type to use for the model. float16 is recommended for most models. For newer GPUs, bfloat16 is better."""
    gpu_memory_utilization: float = 0.8
    """The maximum percentage of GPU memory to use for the model."""
    max_model_len: int = 8192
    """The maximum length of the model to use for the deployment. This value must be between 0 and inf. Make sure this value is suitable for your model card on huggingface."""
    quantization: str | None = None
    """The quantization to use for the model. Please see the vendi documentation for a list of supported quantizations."""

    model_config = ConfigDict(
        protected_namespaces=(),
    )


class Deployment(SchemaMixin):
    name: str
    """The name of the deployment."""
    address: str
    """The address of the deployment in the cluster."""
    resource_name: str
    """The compute resource name of the deployment in the cluster."""
    provider: str
    """The provider of the deployment. vendi/azure/gcp/aws/tenant"""
    model_configuration: ModelConfig
    """The model configuration of the deployment."""
    deploy_configuration: DeploymentConfig
    """The deployment configuration of the deployment."""
    status: DeploymentStatus
    """The status of the deployment."""

    model_config = ConfigDict(
        protected_namespaces=(),
    )
