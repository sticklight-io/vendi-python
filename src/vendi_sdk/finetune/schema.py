import uuid
from enum import Enum
from typing import Optional

from pydantic import BaseModel, ConfigDict

from vendi_sdk.core.schema import SchemaMixin


class TrainStatus(str, Enum):
    SCHEDULED = "SCHEDULED"
    PENDING = "PENDING"
    RUNNING = "RUNNING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    CANCELLED = "CANCELLED"
    CRASHED = "CRASHED"
    PAUSED = "PAUSED"
    CANCELLING = "CANCELLING"


class TrainParameters(BaseModel):
    model_max_length: Optional[int] = 1024
    split_eval: Optional[float] = 0.1
    eval_steps: Optional[int] = 10
    save_steps: Optional[int] = 50
    per_device_train_batch_size: Optional[int] = 1
    per_device_eval_batch_size: Optional[int] = 1
    num_train_epochs: Optional[int] = 3
    max_steps: Optional[int] = 50
    save_total_limit: Optional[int] = 5
    load_best_model_at_end: Optional[bool] = True
    learning_rate: Optional[float] = 0.00002
    gradient_accumulation_steps: Optional[int] = 1
    warmup_steps: Optional[int] = 0
    warmup_ratio: Optional[float] = 0.03

    model_config = ConfigDict(
        protected_namespaces=(),
    )


class LoraTrainParams(TrainParameters):
    lora_r: Optional[int] = 32
    lora_alpha: Optional[int] = 32
    lora_dropout: Optional[float] = 0.05
    lora_target_modules: list[str] | None = [
        "q_proj",
        "o_proj",
        "up_proj",
        "v_proj",
        "gate_proj",
        "down_proj",
        "k_proj",
        "lm_head"
    ]
    q_lora: bool = True


class TrainData(BaseModel):
    logs: list[dict]
    chart: list[dict]
    run_config: dict


class CreateTrainJobSchema(BaseModel):
    model_id: uuid.UUID
    prefect_flow_id: uuid.UUID
    type_: str
    status: TrainStatus
    dataset: str
    base_model: str
    compute_resource: str
    training_params: dict


class TrainJob(CreateTrainJobSchema, SchemaMixin):
    pass
