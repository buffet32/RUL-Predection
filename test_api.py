import requests

response = requests.get("http://localhost:8000/api/v1/maintenance/summary")
print(f"Status Code: {response.status_code}")
print(f"Response: {response.json()}")