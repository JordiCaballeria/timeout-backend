import requests

url = 'http://localhost:8000/enviar-email/'

data = {
    'user_ids[]': ['1', '2'],
    'subject': 'Prova amb array',
    'message': 'A dos mans nen, a dos mans i mirant-me als ulls'
}

response = requests.post(url, data=data)

print(response.json())