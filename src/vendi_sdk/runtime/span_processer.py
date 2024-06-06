import logging
from typing import Optional

from opentelemetry import context as context_api
from opentelemetry.context import get_value
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from traceloop.sdk.tracing.tracing import SimpleSpanProcessor

from vendi_sdk.runtime.constants import USER_KEY


def get_exporter(api_endpoint: str, headers: dict[str, str]) -> OTLPSpanExporter:
    return OTLPSpanExporter(endpoint=f"{api_endpoint}/api/v1/analytics-collector/activity", headers=headers)


class InstrumentSpanProcessor(SimpleSpanProcessor):
    def __init__(self, span_exporter: OTLPSpanExporter):
        super().__init__(span_exporter=span_exporter)

    def on_start(
        self,
        span: "Span",
        parent_context: Optional[context_api.Context] = None,
    ) -> None:
        workflows = get_value("workflows")
        if workflows is not None:
            span.set_attribute("workflows", workflows)
        user = get_value(USER_KEY)
        if user is not None:
            span.set_attribute(USER_KEY, user)
