import asyncio
import uuid

from vendi.completions.schema import CompletionRequest
from vendi import Vendi

client = Vendi(
    api_key="my-api-key"
)
completions = asyncio.run(client.completions.acreate_many(
    requests=[
        CompletionRequest(
            model="openai/gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": "Hey how are you?"}
            ],
            request_id=str(uuid.uuid4()),
        ),
        CompletionRequest(
            model="openai/gpt-4",
            messages=[
                {"role": "user", "content": "Hi whats up?"}
            ],
            request_id=str(uuid.uuid4()),
        ),
    ]
)
)

print(completions)
