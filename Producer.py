from kafka import KafkaProducer
import json
from utils.generate_data import generate_data
from time import sleep
import random

producer = KafkaProducer(
    bootstrap_servers='164.92.76.15:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')  # Serializador para convertir el mensaje a JSON
)

topic = "21762"

def send_message(topic, message):
    producer.send(topic, value=message)
    producer.flush()  # Asegurar que todos los mensajes se envían

if __name__ == '__main__':
    while True:
        message = generate_data()
        send_message(topic, message)
        print(f"Mensaje enviado: {message}")
        sleep(random.randint(15, 30))  # Espera entre 15 y 30 segundos
    
