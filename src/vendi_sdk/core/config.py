from pydantic_settings import BaseSettings


class VendiConfig(BaseSettings):
    VENDI_API_KEY: str = ""
    """The API key to use when making requests to the Vendi API. Use the `VENDI_API_KEY` environment variable to set this value."""
    VENDI_API_URL: str = "https://api.vendi-ai.com"
    """The URL of the Vendi API. Use the `VENDI_API_URL` environment variable to set this value."""


vendi_config = VendiConfig()
