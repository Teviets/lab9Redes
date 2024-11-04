import random
import json
import time
from kafka import KafkaProducer

def generar_datos():
    datos = {
        "temperatura": round(random.gauss(55, 10), 2),  # Centrado en 55 con una desviación estándar
        "humedad": random.randint(0, 100),
        "direccion_viento": random.choice(["N", "NO", "O", "SO", "S", "SE", "E", "NE"])
    }
    return json.dumps(datos)




# Conexión con el servidor Kafka
producer = KafkaProducer(bootstrap_servers='164.92.76.15:9092')
topic = '12345'  # Cambia "12345" por tu número de carné

while True:
    mensaje = generar_datos()
    producer.send(topic, value=mensaje.encode('utf-8'))
    print(f"Mensaje enviado: {mensaje}")
    time.sleep(random.randint(15, 30))
