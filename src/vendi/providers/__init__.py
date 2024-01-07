"""
This package contains the managing all of the providers that Vendi exposes.
Providers are llm-as-a-service providers that can be used to generate text completions.
Providers can be any of the following:
- OpenAI
- Google
- Bedrock
- Cohere

Vendi exposes a single API that can be used to generate text completions from any of the providers.

Vendi's models and finetunes are exposed under `Vendi` provider.
"""
from .providers import Providers
