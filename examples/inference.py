from vendi import VendiClient

client = VendiClient(
    api_key="my-api-key"
)

prompt = "This is the first ever loop closed in vendi platform. what a tremendous milestone. what do you think?"

messages = [{"role": "user", "content": prompt}]
completion = client.completions.create(
    model="vendi/mistral-7b-sdk",
    messages=messages,
)

print(completion)
