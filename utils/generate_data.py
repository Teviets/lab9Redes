import random
import json

def generate_data():
    temp = round(random.gauss(55, 10), 2)
    temp = max(0, min(temp, 110)) # Limitar la temperatura entre 0 y 110
    datos = {
        "temperatura": temp,
        "humedad": random.randint(0, 100),
        "direccion_viento": random.choice(["N", "NO", "O", "SO", "S", "SE", "E", "NE"])
    }
    return json.dumps(datos)