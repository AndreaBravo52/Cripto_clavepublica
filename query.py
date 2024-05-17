import csv
import paramiko

# Establecer conexión SSH con la instancia EC2
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('18.191.206.122', username='ec2-user', key_filename='C:/Users/gilhe/claves/claves_proyecto.pem')

# Hace una pregunta a la base
stdin, stdout, stderr = ssh.exec_command("mysql -h dbcripto.ct1hupiz0cef.us-east-2.rds.amazonaws.com -u usuariomaestro -p'usuariomaestro' dbcripto -e 'SELECT * FROM AllMeterReadings WHERE EntryID < 5;'")

# Obtiene el output del comando
output = stdout.read().decode()

# COnvierte el output a una lista de filas
rows = [line.split('\t') for line in output.strip().split('\n')]

# Lo guarda en un CSV
with open('resultados.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerows(rows)

# Cierra la conexión SSH
ssh.close()

