from flask import Flask, request
import pymysql
import json
import hashlib
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import hashes

app = Flask(__name__)

# Cargar la clave pública del archivo
with open("/home/ec2-user/flask_app/public_key.pem", "rb") as f:
    public_key = serialization.load_pem_public_key(f.read())

def db_connection():
    return pymysql.connect(host='dbcripto.ct1hupiz0cef.us-east-2.rds.amazonaws.com',
                           user='usuariomaestro',
                           password='usuariomaestro',
                           db='dbcripto',
                           charset='utf8mb4',
                           cursorclass=pymysql.cursors.DictCursor)

@app.route('/receive_data', methods=['POST'])
def receive_data():
    data = request.get_json()

    # Verificar el hash
    data_string = json.dumps({k: v for k, v in data.items() if k not in ['hash', 'signature']})
    data_hash = hashlib.sha256(data_string.encode()).hexdigest()
    if data_hash != data['hash']:
        return 'Hash verification failed', 400

    # Verificar la firma
    try:
        public_key.verify(
            bytes.fromhex(data['signature']),
            data_string.encode(),
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
    except Exception as e:
        return 'Signature verification failed', 400

    connection = db_connection()
    try:
        with connection.cursor() as cursor:
            sql = "INSERT INTO `MeterReadings` (`EntryID`, `ID`, `ConsumptionOrProduction`, `Day`, `Month`, `Year`, `Time`, `Reading`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
            cursor.execute(sql, (data['EntryID'], data['ID'], data['ConsumptionOrProduction'], data['Day'], data['Month'], data['Year'], data['Time'], data['Reading']))
        connection.commit()
    finally:
        connection.close()

    return '', 204

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=443, ssl_context=('/etc/pki/tls/certs/apache-selfsigned.crt', '/etc/pki/tls/private/apache-selfsigned.key'))

