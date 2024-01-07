from vendi import Vendi

vendi_client = Vendi(
    api_key="my-api-key"
)

vendi_client.providers.create("google", {"api_key": "google-api-key"})
