from vendi import VendiClient

client = VendiClient(
    api_key="my-api-key"
)

deployments = client.deployments.list()

for deployment in deployments:
    if deployment.name == "mistral-7b-sdk":
        client.deployments.delete(
            deployment_id=deployment.id
        )
        print("Deployment deleted")