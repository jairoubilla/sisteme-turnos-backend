import mysql.connector # Conecta con mysql

# Conexion a MYSQL
def obtener_conexion():
    return mysql.connector.connect(
        host="trolley.proxy.rlwy.net",
        user="root",
        password="TBIXjsnZuuVevTwtUeDcRJkEuNyFTdZe",
        database="railway",
        port=40353
)