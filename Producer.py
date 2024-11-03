from kafka import KafkaProducer
import json
from utils.generate_data import generate_data
from utils.enode_decode_data import encode
from time import sleep
import random

producer = KafkaProducer(
    bootstrap_servers='164.92.76.15:9092',
)

topic = "21762"

def send_message(topic, message):
    producer.send(topic, value=message)
    producer.flush()  # Asegurar que todos los mensajes se envían

if __name__ == '__main__':
    while True:
        message = generate_data()
        encoded_message = encode(message)
        
        send_message(topic, encoded_message)
        print(f"Mensaje original: {message}")
        print(f"Mensaje enviado codificado: {encoded_message}", ", longitud:", len(encoded_message))
        sleep(random.randint(15, 30))  # Espera entre 15 y 30 segundos
    
