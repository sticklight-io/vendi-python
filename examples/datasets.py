import json

from vendi import VendiClient

client = VendiClient(
    api_key="my-api-key"
)
my_datasets = client.datasets.list()

with open("my_data.jsonl", "r") as f:
    data_jsonl = [json.loads(line) for line in f.read().splitlines()]

uploaded_dataset_id = client.datasets.upload(data=data_jsonl, name="my_dataset")
