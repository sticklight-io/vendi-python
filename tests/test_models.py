import pytest
from requests import HTTPError

from conftest import vendi_client


def test_models(vendi_client):
    models = vendi_client.models.list()
    new_model = vendi_client.models.import_model(model_name="mistralai/Mistral-7B-Instruct-v0.2",
                                                 model_provider="huggingface")
    get_new_model = vendi_client.models.get(models[0].id)
    res = vendi_client.models.delete(get_new_model.id)
    assert res is True
    with pytest.raises(HTTPError) as exc:
        vendi_client.models.get(get_new_model.id)
    assert exc.value.response.status_code == 404


def test_set_model_public(vendi_client):
    new_model = vendi_client.models.import_model(model_name="mistralai/Mistral-7B-Instruct-v0.2",
                                                 model_provider="huggingface")

    res = vendi_client.models.set_public(new_model.id, True)

    assert res is True
    get_new_model = vendi_client.models.get(new_model.id)
    assert get_new_model.is_public is True

    res = vendi_client.models.delete(get_new_model.id)
    assert res is True
