from conftest import vendi_client


def test_providers(vendi_client):
    res = vendi_client.providers.create(
        "openai",
        {
            "api_key": "sk-1234567890"
        }
    )
    assert res.config == {
        "api_key": "sk-1234567890"
    }

    assert res.name == "openai"
    my_providers = vendi_client.providers.get("openai")
    assert my_providers is not None

    res = vendi_client.providers.delete("openai")
    assert res is True
