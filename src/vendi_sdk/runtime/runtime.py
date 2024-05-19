import json
from typing import Any
from vendi_sdk.core.http_client import HttpClient
from vendi_sdk.core.ahttp_client import AsyncHTTPClient
from vendi_sdk.runtime.instrument import Instrument


class Runtime:
    def __init__(self, url: str, api_key: str):
        self._client = HttpClient(
            url=url,
            api_key=api_key,
            api_prefix=f"/v1/config-manager/runtime"
        )
        self._aclient = AsyncHTTPClient(
            base_url=f"{url}/config-manager/runtime",
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
        _res = self._client.post(uri=f"/{project_id}/{task_name}/config", json_data={"tags": tags or {}})
        if "value" in _res:
            _res["value"] = json.loads(_res["value"])
        return _res
