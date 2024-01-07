"""
Deployments is an internal class that is used to interact with the Vendi Deployments API.
This one is used only for users with private deployments access.
Please contact us if you would like to use this feature.

Each deployment is associated with a single model and a single backend.
The model must be registered with vendi models and available to the user when running vendi.models.list().
"""
from .deployments import Deployments
