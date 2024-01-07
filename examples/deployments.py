from vendi import VendiClient


client = VendiClient(
    api_key="my-api-key"
)

model = client.models.import_model(
    model_name="mistralai/Mistral-7B-Instruct-v0.2",
    model_provider="huggingface",
)


deployment = client.deployments.create(
    name="mistral-7b-sdk",
    model_name=model.name,
    model_id=str(model.id),
    backend="vllm",
    dtype="float16",
    gpu_memory_utilization=0.8,
    max_model_len=4092,
    quantize="int4"
)





