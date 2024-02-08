import base64

from vendi import Vendi

client = Vendi(
    api_key="my-api-key"
)

prompt = "What is in the image?"


def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')


# Path to your image
image_path = "/Users/matankleyman/Downloads/Screenshot 2023-11-08 at 14.56.47.png"

# Getting the base64 string
base64_image = encode_image(image_path)

messages = [
    {
        "role": "user",
        "content": [
            {"type": "text", "text": prompt},
            {"type": "image_url", "image_url": {
                "url": "https://images.unsplash.com/photo-1530595467537-0b5996c41f2d?w=800&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxleHBsb3JlLWZlZWR8MXx8fGVufDB8fHx8fA%3D%3D"}
             },
        ]
    },
    {"role": "assistant", "content": "A cat"},
    {"role": "user", "content": "Are you sure?"}
]

completion = client.completions.create(
    model="vendi/qwen-vl-chat",
    messages=messages,
)

print(completion)
