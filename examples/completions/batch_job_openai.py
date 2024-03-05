from vendi import Vendi
from vendi.completions.schema import ModelParameters

client = Vendi(
    api_key="my-api-key"
)

batch_data = client.datasets.upload(
    data=[
        {"messages": [
            {
                "content": "This is the first ever loop closed in vendi platform. what a tremendous milestone. what do you think?",
                "role": "user"
            }
        ]
        },
    ],
    name="batch_dataset"
)

job = client.completions.run_batch_job(
    dataset_id=batch_data.id,
    model_parameters=[
        ModelParameters(
            model="openai/gpt-3.5-turbo",
            stop=["</s>"]
        ),
        ModelParameters(
            model="openai/gpt-4",
            stop=["</s>"]
        )
    ],
    wait_until_complete=True
)
### If wait until complete is False, you can check the status of the job
client.completions.batch_job_status(job.id)

### Once the job is complete, you can download the output dataset
print(client.datasets.generate_download_link(job.output_dataset_id))
