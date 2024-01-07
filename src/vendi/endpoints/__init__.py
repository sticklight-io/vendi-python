"""
Endpoints is the interface to the managing model endpoints that can be accessed to make predictions.
Each model trained on the Vendi platform has an endpoint that can be used to make predictions.
Each vendi managed base model also has an endpoint that can be used to make predictions.
Managing endpoints is only available to users with private deployments access.

Endpoints are one-to-one with deployments. Each endpoint is associated with a single deployment.
The deployment must be active for the endpoint to be active.
"""
from .endpoints import Endpoints
