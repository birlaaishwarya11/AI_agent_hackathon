import requests

url = "https://experiment.app.pheno.ml/agent/chat"

headers = {
    "accept": "application/json",
    "content-type": "application/json",
    "authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJjb2xsZWN0aW9uSWQiOiJfcGJfdXNlcnNfYXV0aF8iLCJleHAiOjE3NjA4MjI5NTksImlkIjoidWk0YXIycmllazRiYnZ3IiwidHlwZSI6ImF1dGhSZWNvcmQifQ.PiDnwpxwFpiroXvIRHoScdyBCdGAdKdKi2n_NAt4oAY"
}

response = requests.post(url, headers=headers)

print(response.text)