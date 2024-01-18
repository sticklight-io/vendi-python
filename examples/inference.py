from vendi import Vendi

client = Vendi(
    api_key="my-api-key"
)

prompt = "This is the first ever loop closed in vendi platform. what a tremendous milestone. what do you think?"


endpoints = client.completions.available_endpoints("vendi")


print(endpoints)
messages = [{"role": "user", "content": prompt}]
completion = client.completions.create(
    model="vendi/phi-2",
    messages=messages,
    regex="yes|no|maybe"
)

print(completion)
