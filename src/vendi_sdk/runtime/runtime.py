import json
import threading
from typing import Any
from vendi_sdk.core.http_client import HttpClient
from vendi_sdk.core.ahttp_client import AsyncHTTPClient
from vendi_sdk.runtime.instrument import Instrument


class Runtime:
    def __init__(
            self,
            url: str,
            api_key: str,
            project_id: str | None = None,
    ):
        self._project_id = project_id
        self._client = HttpClient(
            url=url,
            api_key=api_key,
            api_prefix=f"/api/v1"
        )
        self._aclient = AsyncHTTPClient(
            base_url=f"{url}/api/v1",
        )
        self._aclient.set_auth_header(api_key)

    def get_task_config(
            self,
            project_id: str | None = None,
            task_name: str | None = None,
            tags: dict[str, Any] | None = None,
    ) -> dict:
        """
        Get the current runtime configuration
        """
        project_id = project_id or Instrument.project_id()
        task_name = task_name or Instrument.task_name()
        _res = self._client.post(uri=f"/config-manager/runtime/{project_id}/{task_name}/config",
                                 json_data={"tags": tags or {}})
        if "value" in _res:
            _res["value"] = json.loads(_res["value"])
        return _res

    def feedback(
            self,
            name: str,
            id: str | int,
            value: dict[str, Any],
            project_id: str | None = None,
            use_as_callback: bool = False,
    ):
        _project_id = project_id or self._project_id
        if not use_as_callback:
            self._send_feedback(name, id, value, _project_id)
        else:
            # Create a new thread that will execute the request in the background
            thread = threading.Thread(target=self._send_feedback, args=(name, id, value, _project_id))
            thread.start()

    def _send_feedback(self, name: str, id: str | int, value: dict[str, Any], project_id: str):
        self._client.post(
            uri=f"/analytics-collector/{project_id}/feedback/",
            json_data={
                "tag_name": name,
                "tag_value": id,
                "feedback": value
            }
        )

    async def afeedback(
            self,
            name: str,
            id: str | int,
            value: dict[str, Any],
            project_id: str | None = None,
    ):
        _project_id = project_id or self._project_id
        await self._aclient.post(
            path=f"/analytics-collector/{_project_id}/feedback",
            json=value
        )
