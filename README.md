<p align="center">
  <a href="https://github.com/vendi-ai/vendi-python/actions/workflows/test.yaml">
    <img src="https://github.com/vendi-ai/declarai/actions/workflows/test.yaml/badge.svg" alt="Tests">
  </a>
  <a href="https://pypi.org/project/vendi/">
    <img src="https://img.shields.io/pypi/v/vendi?color=%2334D058&label=pypi%20package" alt="Pypi version">
  </a>
    <a href="https://pepy.tech/project/vendi">
    <img src="https://static.pepy.tech/badge/vendi/month" alt="Pypi downloads">
  </a>
</p>

---

**Documentation 📖**: <a href="https://vendi-ai.github.io/declarai" target="_blank">https://docs.vendi-ai.com </a>

**Source Code 💻** : <a href="https://github.com/vendi-ai/declarai" target="_blank">https://github.com/vendi-ai/vendi-python </a>

---

## Vendi Python API Library

The Vendi python library provides convenient access to the Vendi REST API from any Python 3.7+ application.
The library includes all access to the Vendi API, including the ability to create, update, and delete resources.

# Installation

Install the latest version of the library with pip:

```bash
pip install vendi
```

# Usage

The library needs to be configured with your account's API key which is available in the Vendi web interface.

```python

from vendi import Vendi

client = Vendi(api_key="YOUR_API_KEY") 
```

Or you can set the `VENDI_API_KEY` environment variable and the library will automatically use it:

```bash
export VENDI_API_KEY="YOUR_API_KEY"
```

## Inference

The library provides a convenient way to make inference requests to your models.

```python

from vendi import Vendi

client = Vendi(api_key="YOUR_API_KEY")

chat_completion = client.completions.create(
    model_id="vendi/mistral-7b-instruct-v2",
    messages=[
        {
            "role": "user",
            "content": "Hello, I'm looking for a new job. Write me a resume."
        }
    ],
    max_tokens=5,
    temperature=0.5,
    top_p=1,
    frequency_penalty=0.5,
    presence_penalty=0.5,
    stop=["\n"]
)

print(chat_completion.choices[0].text)
```

The inference endpoints are OpenAI compatible, so you can use the same parameters as the OpenAI API or even the OpenAI
Python library.

## Datasets

The library provides a convenient way to upload and download datasets from your account.

```python
from vendi import Vendi

client = Vendi(api_key="YOUR_API_KEY")

dataset = client.datasets.upload(
    name="My Dataset",
    data=[
        {
            "input": "The bill is $5.",
            "output": "5$"
        },
        {
            "name": "They gave us a nice $10 bill.",
            "output": "10$"
        }
    ]
)
```

You can also download datasets from your account.

```python
from vendi import Vendi

client = Vendi(api_key="YOUR_API_KEY")

dataset = client.datasets.get("YOUR_DATASET_ID")

data = dataset.load_data()
```

## Finetune

The library provides a convenient way to finetune models from your account.

```python
from vendi import Vendi

client = Vendi(
    api_key="my-api-key"
)

dataset_id = client.datasets.upload(
    name="my-dataset",
    data_path="conversation.jsonl"
)

finetune_job = client.finetune.run(
    run_name="my-first-finetune",
    model_description="My first finetune",
    model_name="vendi/mistralai/Mistral-7B-Instruct-v0.2",
    dataset_id=dataset_id
)

print(finetune_job)
```

The example above will create a finetune job that will run on the Vendi platform. You can monitor the progress of the
finetune job in the Vendi web interface.

To finetune other models rather than mistralai, you can use the `client.finetune.available_models()` method.

## Models

The models are the finetuned models created out of the finetune jobs. You can list all the models in your account with
the `client.models.list()` method.

```python
from vendi import Vendi

client = Vendi(
    api_key="my-api-key"
)

client.models.list()
```

## Inference on finetuned model

Every finetuned model can be used for inference. You can use the `client.completions.create()` method to make inference
requests to your models just like any other pre-trained models.

```python
from vendi import Vendi

client = Vendi(
    api_key="my-api-key"
)

client.completions.create(
    model_id="<account-name>/<finetuned-model-name>",
    messages=[
        {
            "role": "user",
            "content": "Hello, I'm looking for a new job. Write me a resume."
        }
    ],
    max_tokens=256,
    temperature=0.5,
    top_p=1,
    frequency_penalty=0.5,
    presence_penalty=0.5,
    stop=["\n"]
)
```

📚 For a thorough introduction, features, and best practices, explore
our [official documentation](https://docs.vendi-ai.com/)
and [quickstart](https://docs.vendi-ai.com/quickstart/).

## Contributing 💼

Join our mission to make declarative AI even better together! We welcome contributions from everyone. Please read our
[contributing guide](https://docs.vendi-ai.com/contributing/) to get started.