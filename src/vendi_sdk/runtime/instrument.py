import os
import uuid
from typing import Any

from traceloop.sdk import Traceloop
from opentelemetry.trace import get_current_span, NonRecordingSpan
from opentelemetry.context import get_value, attach, set_value, get_current
from pydantic import BaseModel
from .span_processer import InstrumentSpanProcessor, get_exporter
import json
import logging
from opentelemetry.context.contextvars_context import ContextVarsRuntimeContext

PROJECT_ID_HEADER = "X-Project-Id"
PROJECT_ID = "project_id"
TASK_NAME = "task_name"
WORKFLOW_NAME = "workflow_name"
ENVIRONMENT = "environment"
WORKFLOW_KEY = "workflows"  # {"name": "chat": {"name": "chat", "run_id": "1234", "tags": {}}, "name": "chat2": {"name": "chat2", "run_id": "1234", "tags": {}}
GLOBAL_WORKFLOW_KEY = "_global"
PROPERTIES_KEY = "association_properties"

logger = logging.getLogger(__name__)


def str_uuid():
    return str(uuid.uuid4())


def turn_traceloop_off():
    """
    Turn off the traceloop telemetry and metrics
    """
    os.environ["TRACELOOP_TELEMETRY"] = "false"
    os.environ["TRACELOOP_METRICS_ENABLED"] = "false"


class Workflow(BaseModel):
    # instance_id: str = Field(default_factory=str_uuid)
    run_id: str | None = None
    name: str
    tags: dict[str, Any] = {}

    def to_span_dict(self) -> dict[str, dict[str, Any]]:
        return {
            self.name: self.model_dump()
        }

    @classmethod
    def from_span_dict(cls, span_dict: dict[str, Any]) -> "Workflow":
        return Workflow(**span_dict)


class InstrumentContext(ContextVarsRuntimeContext):
    # @classmethod
    # def validate_data(cls, data: List[Dict[str, Any]]) -> bool:
    #     valid_types = (bool, str, bytes, int, float)
    #     for item in data:
    #         if not all(isinstance(value, valid_types) for value in item.values()):
    #             return False
    #     return True
    @classmethod
    def context_run_id(cls):
        _workflow = cls._get_workflow(cls.current_workflow_name())
        return _workflow.run_id

    @classmethod
    def _set_attribute(cls, attribute_key: str, value: dict, default_value: dict = None):
        _updated_values = value.copy()
        if default_value is None:
            default_value = {}

        current_span = get_current_span()
        in_span_context = not isinstance(current_span, NonRecordingSpan)
        if in_span_context:
            _current_values = json.loads(
                current_span.__dict__["_attributes"].get(attribute_key, json.dumps(default_value))
            )
        else:
            _current_values = json.loads(get_current().get(attribute_key, json.dumps(default_value)))
        _current_values.update(_updated_values)
        current_values = json.dumps(_current_values)
        if in_span_context:
            current_span.set_attribute(
                attribute_key, current_values
            )
        attach(set_value(attribute_key, current_values))

    @classmethod
    def _unset_attribute(cls, attribute_key: str, key: str):
        current_span = get_current_span()
        if not isinstance(current_span, NonRecordingSpan):
            values = json.loads(get_value(attribute_key) or '{}')
            try:
                values.pop(key)
            except KeyError:
                logger.warning(f"Key {key} not found in {attribute_key}")
            attach(set_value(attribute_key, values))

    @classmethod
    def set_workflow_name(cls, workflow_name: str) -> None:
        attach(set_value("_workflow_name", workflow_name))

    @classmethod
    def current_workflow_name(cls) -> str | None:
        return get_value("_workflow_name")

    @classmethod
    def set_workflow(cls, name: str, run_id: Any | None = None, tags: dict[str, Any] | None = None) -> Workflow:
        if not tags:
            tags = {}
        workflow = Workflow(name=name, id=run_id, tags=tags)
        cls.set_workflow_name(name)
        cls._set_attribute(
            attribute_key=WORKFLOW_KEY,
            value=workflow.to_span_dict()
        )
        return workflow

    @classmethod
    def set_tags(cls, tags: dict[str, Any]):
        _workflows = cls._get_workflows()
        current_workflow = cls._get_workflow(cls.current_workflow_name())
        current_workflow.tags.update(tags)
        _workflows.update(current_workflow.to_span_dict())
        cls._set_attribute(WORKFLOW_KEY, _workflows)

    @classmethod
    def unset_workflow(cls, workflow_name: str):
        cls._unset_attribute(
            attribute_key=WORKFLOW_KEY,
            key=workflow_name
        )

    @classmethod
    def set_tag(cls, tag_name: str, tag_value: Any):
        return cls.set_tags({tag_name: tag_value})

    @classmethod
    def set_run_id(cls, run_id: Any):
        _workflows = cls._get_workflows()
        current_workflow = cls._get_workflow(cls.current_workflow_name())
        current_workflow.run_id = run_id
        _workflows.update(current_workflow.to_span_dict())
        cls._set_attribute(WORKFLOW_KEY, _workflows)

    @classmethod
    def _get_workflows(cls) -> dict:
        _workflows = json.loads(get_value(WORKFLOW_KEY) or '{}')
        return _workflows

    @classmethod
    def _get_workflow(cls, workflow_name: str) -> Workflow:
        workflows = cls._get_workflows()
        for name, value in workflows.items():
            if name == workflow_name:
                return Workflow.from_span_dict(value)
        raise ValueError(f"Workflow {workflow_name} not found")


class Instrument:
    api_key: str | None = None
    project_id: str | None = None

    def __init__(
        self,
        project_id: str | None = None,
        api_endpoint: str = "https://api.vendi-ai.com",
        api_key: str = None,
        environment: str = None,
        tags: dict[str, Any] = None,
        **kwargs
    ):
        vendi_api_key = api_key or self.api_key or os.getenv("VENDI_API_KEY")
        project_id = project_id or self.project_id or os.getenv("VENDI_PROJECT_ID")
        headers = {}
        if vendi_api_key:
            headers["Authorization"] = f"Bearer {vendi_api_key}"
        if project_id:
            headers[PROJECT_ID_HEADER] = str(project_id)
        turn_traceloop_off()
        Traceloop.init(
            api_endpoint=api_endpoint,
            processor=InstrumentSpanProcessor(get_exporter(api_endpoint, headers)),
            headers=headers,
            **kwargs
        )

        properties = {}
        if environment:
            properties[ENVIRONMENT] = environment
        if project_id:
            properties[PROJECT_ID] = project_id
        properties.update(tags or {})
        InstrumentContext.set_workflow(name=GLOBAL_WORKFLOW_KEY, tags=properties)


def get_context() -> InstrumentContext:
    return InstrumentContext()
