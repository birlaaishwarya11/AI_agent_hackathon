import requests

url = "https://experiment.app.pheno.ml/auth/token"

headers = {
    "accept": "application/json",
    "authorization": "Basic WW91Z09FTDN5dzljc1lIdkFFMF80UTpRM1lQVFZPanloeU1KZWY4T2ZndW9n"
}

response = requests.post(url, headers=headers)

print(response.text)