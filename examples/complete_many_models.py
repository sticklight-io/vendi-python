from vendi import Vendi

client = Vendi(
    api_key="my-api-key"
)

results = client.completions.create_many_models(
    models=["openai/gpt-3.5-turbo"],
    messages=[{"role": "user", "content": "Hey how are you?"}],
)

print(results)
