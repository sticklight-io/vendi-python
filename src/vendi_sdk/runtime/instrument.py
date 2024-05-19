import os
import uuid
from typing import Any
from traceloop.sdk import Traceloop
from opentelemetry.context import get_value, attach, set_value, get_current

PROJECT_ID_HEADER = "X-Project-Id"
PROJECT_ID = "project_id"
TASK_NAME = "task_name"
ENVIRONMENT = "environment"


class Instrument:
    def __init__(
        self,
        project_id: str | None = None,
        api_endpoint: str = "http://localhost:8091/api/v1/traces",
        vendi_api_key: str = None,
        environment: str = None,
        tags: dict[str, Any] = None,
        **kwargs
    ):
        vendi_api_key = vendi_api_key if vendi_api_key else os.getenv("VENDI_API_KEY")
        headers = {}
        if vendi_api_key:
            headers["Authorization"] = f"Bearer {vendi_api_key}"
        if project_id:
            # TODO validate project-id exists in vendi
            headers[PROJECT_ID_HEADER] = str(project_id)

        Traceloop.init(
            api_endpoint=api_endpoint,
            headers=headers,
            **kwargs
        )

        properties = {}
        if environment:
            properties[ENVIRONMENT] = environment
        if project_id:
            properties[PROJECT_ID] = project_id
        properties.update(tags or {})
        self.set_tags(properties)

    @classmethod
    def set_tags(
        cls,
        tags: dict[str, Any]
    ):
        current_context = get_current()
        if current_context:
            current_tags = get_value("association_properties")
            if current_tags and isinstance(current_tags, dict):
                tags.update(current_tags)

        attach(set_value("association_properties", tags))

    @classmethod
    def set_task_name(cls, name: str):
        cls.set_tags(
            {TASK_NAME: name}
        )

    @classmethod
    def get_tags(cls) -> dict[str, Any]:
        return get_value("association_properties") or {}

    @classmethod
    def project_id(cls):
        return cls.get_tags().get(PROJECT_ID)

    @classmethod
    def task_name(cls):
        return cls.get_tags().get(TASK_NAME)
