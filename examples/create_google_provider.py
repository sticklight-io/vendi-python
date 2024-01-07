from vendi import VendiClient

vendi_client = VendiClient(
    api_key="my-api-key"
)

vendi_client.providers.create("google", {"api_key": "google-api-key"})
