import json

from vendi import Vendi

client = Vendi(
    api_key="my-api-key"
)

my_datasets = client.datasets.list()

with open("../conversation.jsonl", "r") as f:
    data_jsonl = [json.loads(line) for line in f.read().splitlines()]

uploaded_dataset_id = client.datasets.upload(data=data_jsonl, name="my_dataset")
