from vendi import Vendi

client = Vendi(
    api_key="my-api-key"
)

dataset_id = client.datasets.upload(
    name="my-dataset",
    data_path="conversation.jsonl"
)

models = client.finetune.available_models()

print(models)

finetune_job = client.finetune.run(
    run_name="my-first-finetune",
    model_description="My first finetune",
    model_name=models[0].name,
    dataset_id=dataset_id
)


print(finetune_job)
