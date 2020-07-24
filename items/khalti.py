import requests

url = "https://khalti.com/api/v2/merchant-transaction/"
payload = {}
headers = {
  "Authorization": "Key test_public_key_643177b971f64dd3b9f0fd4914f8c6b8"
}

response = requests.get(url, payload, headers=headers).json()

