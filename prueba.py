import pymysql.cursors

def db_connection():
    return pymysql.connect(host='dbcripto.ct1hupiz0cef.us-east-2.rds.amazonaws.com',
                           user='usuariomaestro',
                           password='usuariomaestro',
                           db='dbcripto',
                           charset='utf8mb4',
                           cursorclass=pymysql.cursors.DictCursor)

connection = db_connection()

try:
    with connection.cursor() as cursor:
        sql = "SELECT * FROM `MeterReadings`"
        cursor.execute(sql)
        result = cursor.fetchall()
        print(result)
finally:
    connection.close()

