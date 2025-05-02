import requests

url = "http://localhost:8091/api/SetTextCP?token=N3bPkOuJ4ds02RCR"
headers = {
    "Content-Type": "application/json"
}
data = {
    "text": "Teste direto do Python",
    "show": True,
    "display_ahead": True
}

response = requests.post(url, json=data, headers=headers)
print("Status:", response.status_code)
print("Resposta:", response.text)
