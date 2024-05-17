import requests
import json
import time
import pandas as pd
import hashlib
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization

# Se carga el archivo .csv a un dataframe de pandas
df = pd.read_csv('C:/Users/gilhe/datos/datos_medidor.csv')

# Se carga la clave privada del archivo
with open("C:/Users/gilhe/claves/private_key.pem", "rb") as f:
    private_key = serialization.load_pem_private_key(
        f.read(),
        password=None,
    )


url = 'https://18.191.206.122/receive_data'

# Contador para el número de registros enviados
count = 0

for index, row in df.iterrows():
    if count >= 5:
        break

    data = {
        'EntryID': row['EntryID'],  # Assuming 'EntryID' is a column in your CSV
        'ID': row['ID'],
        'ConsumptionOrProduction': row['ConsumptionOrProduction'],
        'Day': row['Day'],
        'Month': row['Month'],
        'Year': row['Year'],
        'Time': row['Time'],
        'Reading': row['Reading']
    }

    # Se crea el hash de los datos
    data_string = json.dumps(data)
    data_hash = hashlib.sha256(data_string.encode()).hexdigest()

    # Se firman los datos 
    signature = private_key.sign(
        data_string.encode(),
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )

    # Se incluyen el hash y la firma en los datos enviados al servidor
    data['hash'] = data_hash
    data['signature'] = signature.hex()

    response = requests.post(url, data=json.dumps(data), headers={'Content-Type': 'application/json'}, verify='C:\\Users\\gilhe\\claves\\apache-selfsigned.crt')

    # Se imprime el status de respuesta
    print(response.status_code)

    # Pasan 2 segundos
    time.sleep(2)

    # Se incrementa el contador
    count += 1
