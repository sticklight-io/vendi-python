import base64

from vendi import Vendi
import requests
from io import BytesIO

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
                "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/3a/Cat03.jpg/481px-Cat03.jpg"
                # "url": f"data:image/jpeg;base64,{base64_image}"
            }
             },
        ]
    },
]

completion = client.completions.create(
    model="vendi/llava-v1-6-mistral-7b",
    messages=messages
)

print(completion)
