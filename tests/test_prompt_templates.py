import pytest
from requests import HTTPError

from conftest import vendi_client


def test_prompt_templates(vendi_client):
    prompt_templates = vendi_client.prompt_templates.list()
    new_prompt_template = vendi_client.prompt_templates.create(name="test_prompt_template",
                                                               prompt_template="test_prompt_template")
    get_new_prompt_template = vendi_client.prompt_templates.get(prompt_templates[0].id)
    res = vendi_client.prompt_templates.delete(get_new_prompt_template.id)
    assert res is True
    with pytest.raises(HTTPError) as exc:
        vendi_client.prompt_templates.get(get_new_prompt_template.id)
    assert exc.value.response.status_code == 409


def test_update_prompt_template(vendi_client):
    prompt_templates = vendi_client.prompt_templates.list()
    new_prompt_template = vendi_client.prompt_templates.create(name="test_prompt_template",
                                                               prompt_template="test_prompt_template")
    get_new_prompt_template = vendi_client.prompt_templates.get(prompt_templates[0].id)
    res = vendi_client.prompt_templates.update(get_new_prompt_template.id, name="test_prompt_template_updated")
    assert res.name == "test_prompt_template_updated"
    res = vendi_client.prompt_templates.delete(get_new_prompt_template.id)
    assert res is True
    with pytest.raises(HTTPError) as exc:
        vendi_client.prompt_templates.get(get_new_prompt_template.id)
    assert exc.value.response.status_code == 409
