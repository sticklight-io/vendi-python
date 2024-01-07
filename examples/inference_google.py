from vendi import Vendi

client = Vendi(
    api_key="dev-tenant-api-key"
)

res = client.completions.create(
    model="google/gemini-pro",
    messages=[{"role": "user", "content": "I want to buy a car"}]
)

print(res)