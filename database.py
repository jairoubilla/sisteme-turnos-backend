import mysql.connector # Conecta con mysql

# Conexion a MYSQL
def obtener_conexion():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="549204290Ali",
        database="hospital_turnos"
)