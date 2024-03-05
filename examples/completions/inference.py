from vendi import Vendi

client = Vendi(
    api_key="my-api-key"
)

prompt = "This is the first ever loop closed in vendi platform. what a tremendous milestone. what do you think?"

available_endpoints = client.completions.available_endpoints()
catalog = client.completions.endpoints_catalog()

messages = [{"role": "user", "content": prompt}]
completion = client.completions.create(
    model="vendi/phi2",
    messages=messages,
    regex="yes|no|maybe"
)

print(completion)
