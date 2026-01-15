import mysql.connector # Conecta con mysql

# Conexion a MYSQL
def obtener_conexion():
    return mysql.connector.connect(
        host="mysql.railway.internal",
        user="root",
        password="TBIXjsnZuuVevTwtUeDcRJkEuNyFTdZe",
        database="railway"
        port=3306
)