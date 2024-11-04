from kafka import KafkaConsumer
import json
import matplotlib.pyplot as plt
import time
from datetime import datetime
from utils.enode_decode_data import decode

temp = []
hum = []
dir_viento = []
time_data = []  # Para almacenar el tiempo

topic = '21762'

consumer = KafkaConsumer(
    topic,
    bootstrap_servers='164.92.76.15:9092',
    group_id='my-group',
    auto_offset_reset='earliest'
)
print(f"Esperando mensajes en el topic {topic}")

# Inicializar una figura con tres subplots
plt.ion()
fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(10, 6))

# Ajustar el espacio entre los subplots
plt.subplots_adjust(hspace=1)

# Control de frecuencia de actualización
last_update_time = time.time()
update_interval = 2  # Actualizar cada 2 segundos

# Definir las etiquetas para la dirección del viento
direccion_mapping = {"N": 0, "NO": 1, "O": 2, "SO": 3, "S": 4, "SE": 5, "E": 6, "NE": 7}
direccion_labels = ["N", "NO", "O", "SO", "S", "SE", "E", "NE"]

for message in consumer:
    print("Mensaje recibido sin decodificar:", message.value, ", longitud:", len(message.value))
    decoded_message = decode(message.value)
    print(f"Mensaje recibido: {decoded_message}")
    
    try:
        # Decodifica el JSON y elimina comillas extra si es necesario
        payload_str =decoded_message
        payload = json.loads(payload_str)

        if isinstance(payload, str):
            payload = json.loads(payload)

        if isinstance(payload, dict):
            temp.append(payload['temperatura'])
            hum.append(payload['humedad'])
            # Mapear la dirección del viento a su valor numérico
            dir_viento.append(direccion_mapping.get(payload['direccion_viento'], None))
            current_time = datetime.now().strftime("%H:%M:%S")  # Formato de hora
            time_data.append(current_time)  # Guarda la hora actual

            # Actualiza las gráficas solo si ha pasado el intervalo
            if time.time() - last_update_time > update_interval:
                # Actualiza la gráfica de Tiempo vs Temperatura
                ax1.clear()
                ax1.plot(time_data, temp, 'ro-')  # Línea roja con puntos
                ax1.set_xlabel('Tiempo (HH:MM:SS)')
                ax1.set_ylabel('Temperatura')
                ax1.set_xticks(range(len(time_data)))  # Establecer los ticks
                ax1.set_xticklabels(time_data, rotation=45, ha='right')  # Actualiza las etiquetas
                ax1.grid(True)  # Activa la cuadrícula para la gráfica de Temperatura

                # Actualiza la gráfica de Tiempo vs Humedad
                ax2.clear()
                ax2.plot(time_data, hum, 'bo-')  # Línea azul con puntos
                ax2.set_xlabel('Tiempo (HH:MM:SS)')
                ax2.set_ylabel('Humedad')
                ax2.set_xticks(range(len(time_data)))  # Establecer los ticks
                ax2.set_xticklabels(time_data, rotation=45, ha='right')  # Actualiza las etiquetas
                ax2.grid(True)  # Activa la cuadrícula para la gráfica de Humedad

                # Actualiza la gráfica de Tiempo vs Dirección del Viento
                ax3.clear()
                ax3.plot(time_data, dir_viento, 'go-')  # Línea verde con puntos
                ax3.set_xlabel('Tiempo (HH:MM:SS)')
                ax3.set_ylabel('Dirección del Viento')
                ax3.set_yticks(range(len(direccion_labels)))
                ax3.set_yticklabels(direccion_labels)
                ax3.set_xticks(range(len(time_data)))
                ax3.set_xticklabels(time_data, rotation=45, ha='right')
                ax3.grid(True)

                # Pausa para actualizar las gráficas
                plt.pause(0.1)
                last_update_time = time.time()
    except json.JSONDecodeError as e:
        print(f"Error al decodificar JSON: {e}")
