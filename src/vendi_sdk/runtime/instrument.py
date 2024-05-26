import os
import uuid
from typing import Any, List, Dict
from traceloop.sdk import Traceloop
from traceloop.sdk.telemetry import Telemetry
from opentelemetry.trace import get_current_span, NonRecordingSpan
from opentelemetry.context import get_value, attach, set_value, get_current, create_key
import json
from pydantic import BaseModel

PROJECT_ID_HEADER = "X-Project-Id"
PROJECT_ID = "project_id"
TASK_NAME = "task_name"
WORKFLOW_NAME = "workflow_name"
ENVIRONMENT = "environment"
WORKFLOW_KEY = "workflows"
CUSTOM_TAGS_KEY = "custom_tags"
PROPERTIES_KEY = "association_properties"


class Workflow(BaseModel):
    id: Any
    name: str


class Instrument:
    def __init__(
            self,
            project_id: str | None = None,
            api_endpoint: str = "http://localhost:8091/api/v1/traces",
            api_key: str = None,
            environment: str = None,
            tags: dict[str, Any] = None,
            **kwargs
    ):
        vendi_api_key = api_key if api_key else os.getenv("VENDI_API_KEY")
        headers = {}
        if vendi_api_key:
            headers["Authorization"] = f"Bearer {vendi_api_key}"
        if project_id:
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
    def validate_data(cls, data: List[Dict[str, Any]]) -> bool:
        valid_types = (bool, str, bytes, int, float)
        for item in data:
            if not all(isinstance(value, valid_types) for value in item.values()):
                return False
        return True

    @classmethod
    def update_properties(
            cls,
            key: str,
            new_data: List[Dict[str, Any]] | Dict[str, Any]
    ):
        if isinstance(new_data, dict):
            new_data = [new_data]

        if not cls.validate_data(new_data):
            raise ValueError(
                "Invalid type for attribute! "
                "Expected one of ['bool', 'str', 'bytes', 'int', 'float'] or a sequence of those types"
            )

        current_context = get_current()
        if current_context:
            current_properties = cls.get_tags()
            current_data = current_properties.get(key) or []
            if current_data and isinstance(current_data, str):
                current_data = json.loads(current_data)

            new_properties = {key: json.dumps(current_data + new_data)}
            current_properties.update(new_properties)
            attach(set_value(PROPERTIES_KEY, current_properties))

    @classmethod
    def set_tags(
            cls,
            tags: List[Dict[str, Any]] | Dict[str, Any]
    ):
        cls.update_properties(CUSTOM_TAGS_KEY, tags)

    # @classmethod
    # def set_workflows(
    #         cls,
    #         workflows: List[Dict[str, Any]] | Dict[str, Any],
    # ):
    #     cls.update_properties(WORKFLOW_KEY, workflows)

    @classmethod
    def set_tag(cls, name: str, value: Any):
        cls.set_tags([{name: value}])

    # @classmethod
    # def set_workflow(cls, name: str, correlation_id: uuid.UUID):
    #     cls.set_workflows([{name: correlation_id}])

    @classmethod
    def set_task_name(cls, name: str):
        cls.set_tags(
            {TASK_NAME: name}
        )

    # @classmethod
    # def set_workflow_name(cls, name: str):
    #     cls.set_tags(
    #         {WORKFLOW_NAME: name}
    #     )

    @classmethod
    def get_tags(cls) -> dict[str, Any]:
        return get_value(PROPERTIES_KEY) or {}

    @classmethod
    def project_id(cls):
        return cls.get_tags().get(PROJECT_ID)

    @classmethod
    def task_name(cls):
        return cls.get_tags().get(TASK_NAME)

    # @classmethod
    # def feedback(cls, workflow_correlation_id, event_properties: Dict[str, any]):
    #     # event_properties.update({"workflow_correlation_id": workflow_correlation_id})
    #     self.traceloop.report_score(
    #         association_property_name="chat_id",
    #         association_property_id="12345",
    #         score=1
    #     )

    @classmethod
    def set_workflow(cls, name: str, id: Any):
        workflow = Workflow(name=name, id=id)
        current_span = get_current_span()
        workflows = json.loads(current_span.__dict__["_attributes"].get(WORKFLOW_KEY, '[]'))
        workflow_data = json.dumps([workflow.model_dump()] + workflows)
        attach(set_value(WORKFLOW_KEY, workflow_data))
        current_span.set_attribute(
            WORKFLOW_KEY, workflow_data
        )

    @classmethod
    def unset_workflow(cls):
        current_span = get_current_span()
        if not isinstance(current_span, NonRecordingSpan):
            workflows = json.loads(get_value(WORKFLOW_KEY) or '[]')
            if workflows:
                workflows.pop(-1)
            attach(set_value(WORKFLOW_KEY, json.dumps(workflows)))
