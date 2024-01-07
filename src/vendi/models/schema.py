import uuid
from enum import Enum
from typing import List

from pydantic import BaseModel, ConfigDict

from vendi.core.schema import SchemaMixin


class ModelType(str, Enum):
    PRE_TRAINED = "pre_trained"
    FULLY_TRAINED = "fully_trained"
    FINE_TUNED = "fine_tuned"
    EXTERNAL = "external"


class ModelProvider(str, Enum):
    VENDI = "vendi"
    """A model that is created by vendi for you"""
    HUGGINGFACE = "huggingface"
    """A model that is present on and was imported from huggingface"""
    TRAINING = "training"
    """A model that is created by finetuning a vendi model"""
    OPENAI = "openai"
    """A model that openai exposes through its api"""
    GOOGLE = "google"
    """A model that google exposes through its api"""


class ModelInfo(BaseModel):
    name: str
    """The name of the model"""
    source: ModelProvider
    """The provider of the model"""
    type_: ModelType
    """The type of the model"""
    model_config = ConfigDict(
        protected_namespaces=(),
    )


class Model(SchemaMixin):
    name: str
    source: str
    type_: str
    description: str
    is_public: bool
    base_model_id: uuid.UUID | str | None = None
    status: str | None


class HuggingFaceModel(BaseModel):
    hf_model_name: str
    hf_model_repo: str
    language: List[str]
    license: str
    tags: List[str]
