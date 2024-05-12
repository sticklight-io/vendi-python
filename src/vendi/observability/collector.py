import os
import uuid

from traceloop.sdk import Traceloop


class Collector:
    @classmethod
    def init(
        cls,
        api_endpoint="http://localhost:8091/api/v1/traces",
        vendi_api_key=None,
        **kwargs
    ):
        vendi_api_key = vendi_api_key if vendi_api_key else os.getenv("VENDI_API_KEY")
        Traceloop.init(
            api_endpoint=api_endpoint,
            headers={"Authorization": f"Bearer {vendi_api_key}"},
            **kwargs
        )

    @classmethod
    def set_id(cls, id: str | int | uuid.UUID):
        Traceloop.set_association_properties(
            {"id": id}
        )

    @classmethod
    def set_task_name(cls, name: str):
        Traceloop.set_association_properties(
            {"vendiTaskName": name}
        )

    @classmethod
    def set_association_properties(cls, properties: dict):
        Traceloop.set_association_properties(properties)
