from vendi import Vendi

client = Vendi(
    api_key="dev-tenant-api-key"
)

results = client.completions.create_many_prompts(
    model="openai/gpt-3.5-turbo",
    conversations=[[{"role": "user", "content": "Hey how are you?"}] for i in range(3)],
)

print(results)
