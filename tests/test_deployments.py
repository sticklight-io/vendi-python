import time

import pytest
from requests import HTTPError

from conftest import vendi_client
from vendi.deployments.schema import DeploymentStatus


def test_deployments(vendi_client):
    model = vendi_client.models.import_model(
        model_name="mistralai/Mistral-7B-Instruct-v0.2",
        model_provider="huggingface",
    )
    deployments = vendi_client.deployments.list()
    if len(deployments) > 0:
        for deployment in deployments:
            res = vendi_client.deployments.delete(deployment.id)
            assert res is True

    # Let the uninstall chart finish running
    time.sleep(5)

    new_deployment = vendi_client.deployments.create(
        name="sdk_test_deployment",
        model_name=model.name,
        model_id=str(model.id),
        backend="vllm",
        dtype="float16",
        gpu_memory_utilization=0.8,
        max_model_len=4092,
        quantize="int4"
    )

    # Let the install chart finish running
    time.sleep(5)

    assert new_deployment.name == "sdk_test_deployment"
    assert new_deployment.model_configuration.model_name == "mistralai/Mistral-7B-Instruct-v0.2"
    assert new_deployment.model_configuration.backend == "vllm"
    assert new_deployment.model_configuration.dtype == "float16"
    assert new_deployment.model_configuration.gpu_memory_utilization == 0.8
    assert new_deployment.model_configuration.max_model_len == 4092
    assert new_deployment.model_configuration.quantize == "int4"
    assert new_deployment.deploy_configuration.scale_to_zero is True
    assert new_deployment.deploy_configuration.scale_to_zero_timeout_seconds == 900

    get_new_deployment = vendi_client.deployments.get(new_deployment.id)

    updated_deployment = vendi_client.deployments.update(
        deployment_id=get_new_deployment.id,
        scale_to_zero=False,
        scale_to_zero_timeout_seconds=600,
    )
    assert updated_deployment.deploy_configuration.scale_to_zero is False
    assert updated_deployment.deploy_configuration.scale_to_zero_timeout_seconds == 600

    res = vendi_client.deployments.get(get_new_deployment.id)
    stopped_deployment = vendi_client.deployments.stop(deployment_id=get_new_deployment.id)
    assert stopped_deployment.status == DeploymentStatus.STOPPING

    started_deployment = vendi_client.deployments.start(deployment_id=get_new_deployment.id)
    assert started_deployment.status == DeploymentStatus.CREATING

    res = vendi_client.deployments.delete(get_new_deployment.id)
    assert res is True
    with pytest.raises(HTTPError) as exc:
        vendi_client.deployments.get(get_new_deployment.id)
    assert exc.value.response.status_code == 404
