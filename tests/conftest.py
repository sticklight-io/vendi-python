import os

import pytest

api_key = os.environ.get("VENDI_API_KEY")


@pytest.fixture()
def vendi_client():
    from vendi import VendiClient
    return VendiClient(
        api_key=api_key
    )
