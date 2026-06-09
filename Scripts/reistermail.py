import requests
import json

# URL de la API de registro
register_url = "http://localhost:8000/api/register/"

# Datos de usuario para el registro
user_data = {
    "username": "isaac2",
    "first_name": "isaac",
    "last_name": "Gonzalez Morera",
    "email": "isaacggm@gmail.com",
    "password": "super3super3",
    "password_confirm": "super3super3",
    "is_active": False
}

# Realizar una petición POST a la API de registro con los datos del usuario
response = requests.post(register_url, data=user_data)

