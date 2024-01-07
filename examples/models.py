from vendi import VendiClient

client = VendiClient(
    api_key="my-api-key"
)


client.models.list()