from typing import Dict, Optional, Any

import requests
from requests import Response


class HttpClient:
    def __init__(self, api_key: str, url: str | None = None, api_prefix: Optional[str] = None):
        self.__url: str = url
        self.__api_url: str = url + api_prefix if api_prefix else url
        self.__api_key: str = api_key

    @property
    def base_url(self) -> str:
        return self.__url

    @property
    def api_url(self) -> str:
        return self.__api_url

    # @retry(wait=wait_exponential(max=3), stop=stop_after_attempt(3), reraise=True)
    def put(
        self,
        uri: str,
        json_data: Any = None,
        data: Any = None,
        headers: Optional[Dict] = None,
    ) -> Any:
        _headers = self._set_headers(headers)
        url = self.__urljoin(uri)
        res = requests.put(url, json=json_data, data=data, headers=_headers)
        return self.__handle_response(res)

    # @retry(wait=wait_exponential(max=3), stop=stop_after_attempt(3), reraise=True)
    def post(
        self,
        uri: str,
        json_data: Any = None,
        data: Any = None,
        headers: Optional[Dict] = None,
    ) -> Any:
        _headers = self._set_headers(headers)
        url = self.__urljoin(uri)
        res = requests.post(url, json=json_data, data=data, headers=_headers, allow_redirects=True)
        return self.__handle_response(res)

    def _set_headers(self, headers: Dict[str, str]) -> Dict[str, str]:
        _headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.__api_key}",
        }
        if headers:
            _headers.update(headers)
        return _headers

    # @retry(wait=wait_exponential(max=3), stop=stop_after_attempt(3), reraise=True)
    def get(
        self, uri: str | None = None, *, params: Optional[Dict] = None, headers: Optional[Dict] = None
    ) -> Any:
        _headers = self._set_headers(headers)
        url = self.__urljoin(uri)
        translate_params = {}
        if params:
            for k, v in params.items():
                if isinstance(v, bool):
                    v = "true" if v else "false"
                translate_params[k] = v

        res = requests.get(url, params=translate_params, headers=_headers)
        return self.__handle_response(res)

    # @retry(wait=wait_exponential(max=3), stop=stop_after_attempt(3), reraise=True)
    def delete(
        self,
        uri: str,
        params: Optional[Dict] = None,
        headers: Optional[Dict] = None,
    ) -> Any:
        _headers = self._set_headers(headers)
        url = self.__urljoin(uri)
        translate_params = {}
        if params:
            for k, v in params.items():
                if isinstance(v, bool):
                    v = "true" if v else "false"
                translate_params[k] = v

        res = requests.delete(url, params=translate_params, headers=_headers)
        return self.__handle_response(res)

    def __urljoin(self, uri: str) -> str:
        if not uri:
            return self.__api_url
        return self.__api_url + uri

    @staticmethod
    def __handle_response(resp: Response) -> Any:
        try:
            resp.raise_for_status()
        except requests.exceptions.HTTPError as e:
            message = e.args[0]
            try:
                message += f", Response from server: {resp.text}"
            except ValueError:
                pass
            raise requests.exceptions.HTTPError(message, response=e.response)
        return resp.json() if resp.content else None

    def patch(
        self,
        uri: str,
        json_data: Any = None,
        data: Any = None,
        headers: Optional[Dict] = None,
    ) -> Any:
        _headers = self._set_headers(headers)
        url = self.__urljoin(uri)
        res = requests.patch(url, json=json_data, data=data, headers=_headers)
        return self.__handle_response(res)
