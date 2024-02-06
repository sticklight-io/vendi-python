from vendi import Vendi

client = Vendi(
    api_key="my-api-key"
)

prompt = "What is in the image?"

messages = [
    {
        "role": "user",
        "content": [
            {"type": "text", "text": prompt},
            {"type": "image_url", "image_url": {
                "url": "https://images.unsplash.com/photo-1530595467537-0b5996c41f2d?w=800&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxleHBsb3JlLWZlZWR8MXx8fGVufDB8fHx8fA%3D%3D"}
             }
        ]
    }
]
completion = client.completions.create(
    model="vendi/llava-v1-6-mistral-7b",
    messages=messages,
)

print(completion)
