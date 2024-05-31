from typing import Any
import uuid

from pydantic import BaseModel, Field


def generate_str_uuid():
    return str(uuid.uuid4())


class Workflow(BaseModel):
    run_id: Any | None = Field(default_factory=generate_str_uuid)
    name: str


workflow = Workflow(name="test")
workflow_2 = Workflow(name="test2")

assert not workflow.run_id == workflow_2.run_id
