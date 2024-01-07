from vendi import VendiClient

client = VendiClient(
    api_key="my-api-key"
)

dataset_id = 'dcea437a-6e23-4f45-ad1b-a57fd16f78eb'

dataset = client.datasets.get(dataset_id)
df = dataset.load_data()

num_rows = 3
df = df.head(num_rows)

results = client.completions.create_batch(
    model="google/gemini-pro",
    batch_messages=[[{"role": "user", "content": "Hey how are you?"}] for i in range(len(df))],
)

print(results)




