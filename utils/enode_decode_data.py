import json

# Mapear las direcciones de viento a valores binarios
direccion_viento_map = {
    "N": 0b000, "NO": 0b001, "O": 0b010, "SO": 0b011,
    "S": 0b100, "SE": 0b101, "E": 0b110, "NE": 0b111
}

# Encode: JSON a Bytes
def encode(data_json):
    data = json.loads(data_json)
    
    # Convertir temperatura a un entero en el rango de 0 a 11000
    temp_int = int(data["temperatura"] * 100)  # Escalar la temperatura
    
    # Obtener humedad (0-100) y dirección de viento
    humedad = data["humedad"]
    direccion_viento = direccion_viento_map[data["direccion_viento"]]
    
    # Empaquetar los datos en 24 bits
    packed_data = (temp_int << 10) | (humedad << 3) | direccion_viento
    
    # Convertir a bytes (3 bytes, o 24 bits en total)
    return packed_data.to_bytes(3, 'big')

# Decode: Bytes a JSON
def decode(encoded_bytes):
    # Convertir los bytes de regreso a un entero de 24 bits
    packed_data = int.from_bytes(encoded_bytes, 'big')
    
    # Extraer cada campo usando operaciones de bitwise
    direccion_viento = packed_data & 0b111
    humedad = (packed_data >> 3) & 0b1111111
    temp_int = (packed_data >> 10) & 0b11111111111111
    
    # Convertir de nuevo la temperatura a punto flotante
    temperatura = temp_int / 100.0
    
    # Decodificar dirección de viento
    direccion_viento_rev_map = {v: k for k, v in direccion_viento_map.items()}
    direccion_viento_str = direccion_viento_rev_map[direccion_viento]
    
    # Crear JSON de salida
    datos = {
        "temperatura": temperatura,
        "humedad": humedad,
        "direccion_viento": direccion_viento_str
    }
    
    return json.dumps(datos)
  
if __name__ == "__main__":
  
  from generate_data import generate_data
  
  data_json = generate_data()
  print("Datos originales:", data_json)

  encoded_bytes = encode(data_json)
  print("Datos codificados en bytes:", encoded_bytes)
  print("Longitud de los bytes:", len(encoded_bytes))

  decoded_data = decode(encoded_bytes)
  print("Datos decodificados:", decoded_data)