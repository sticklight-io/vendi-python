from vendi import Vendi
from vendi.completions.schema import ModelParameters

client = Vendi(
    api_key="my-api-key"
)
batch_data = client.datasets.upload(
    data=[
        {"messages": [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "Is there a bear in the image?"},
                    {"type": "image_url", "image_url": {
                        "url": "https://images.unsplash.com/photo-1530595467537-0b5996c41f2d?w=800&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxleHBsb3JlLWZlZWR8MXx8fGVufDB8fHx8fA%3D%3D"}
                     },
                ]
            }
        ]},
        {"messages": [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "Is there a bear in the image?"},
                    {"type": "image_url", "image_url": {
                        "url": "https://images.unsplash.com/photo-1530595467537-0b5996c41f2d?w=800&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxleHBsb3JlLWZlZWR8MXx8fGVufDB8fHx8fA%3D%3D"}
                     },
                ]
            }
        ]},
        {"messages": [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "Is there a bear in the image?"},
                    {"type": "image_url", "image_url": {
                        "url": "https://images.unsplash.com/photo-1530595467537-0b5996c41f2d?w=800&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxleHBsb3JlLWZlZWR8MXx8fGVufDB8fHx8fA%3D%3D"}
                     },
                ]
            }
        ]},
        {"messages": [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "Is there a bear in the image?"},
                    {"type": "image_url", "image_url": {
                        "url": "https://images.unsplash.com/photo-1530595467537-0b5996c41f2d?w=800&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxleHBsb3JlLWZlZWR8MXx8fGVufDB8fHx8fA%3D%3D"}
                     },
                ]
            }
        ]}
    ],
    name="batch_dataset_llava"
)

job = client.completions.run_batch_job(
    dataset_id=batch_data.id,
    model_parameters=[
        ModelParameters(
            model="vendi/llava-v1-6-mistral-7b",
        )
    ],
    wait_until_complete=False
)
### If wait until complete is False, you can check the status of the job
client.completions.batch_job_status(job.id)

### Once the job is complete, you can download the output dataset
print(client.datasets.generate_download_link(job.output_dataset_id))
