from flask import Blueprint, request, jsonify
from database import obtener_conexion
from schemas import PacienteSchema # Importamos el esquema
from marshmallow import ValidationError

pacientes_bp = Blueprint('pacientes', __name__)
paciente_schema = PacienteSchema() # Instanciamos el esquema
pacientes_schema = PacienteSchema(many=True)

@pacientes_bp.route("/pacientes", methods=["GET"])
def obtener_pacientes():
    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True) #Crea un cursor que devuelve resultados
    cursor.execute("SELECT id, nombre, dni, telefono FROM pacientes") #Ejecuta la consulta
    resultados = cursor.fetchall() # Trae todos los pacientes
    cursor.close()
    conexion.close() 
    
    pacientes = []
    for fila in resultados:
        pacientes.append({
            "id": fila["id"],
            "nombre": fila["nombre"],
            "dni": fila["dni"],
            "telefono": fila["telefono"]
        })                
        
    return jsonify(pacientes)

@pacientes_bp.route("/pacientes", methods=["POST"])
def agregar_paciente():
    json_data = request.get_json()
    print("DATOS RECIBIDOS:", json_data)
    if not json_data:
        return jsonify({"mensaje": "No se enviaron datos"}), 400
    
    try:
        # Validacion: Marshmallow revisa si faltan campos o si el formato es malo
        datos = paciente_schema.load(json_data)
    except ValidationError as err:
        return jsonify(err.messages), 400 # Devuelve que campo fallo y por que
    
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute(
        "INSERT INTO pacientes (nombre, dni, telefono) VALUES (%s, %s, %s)",
        (datos['nombre'], datos['dni'], datos.get('telefono'))
    )
    conexion.commit()
    cursor.close()
    conexion.close()
    
    return jsonify({"mensaje": "Paciente agregado correctamente"}), 201

@pacientes_bp.route("/pacientes/<int:id>", methods=["PUT"]) 
def actualizar_paciente(id):
    datos = request.get_json()
    nombre = datos.get("nombre")
    dni = datos.get("dni")
    telefono = datos.get("telefono")
    
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute(
        "UPDATE pacientes SET nombre = %s, dni = %s, telefono = %s WHERE id = %s",
        (nombre, dni, telefono, id)
    )
    filas_afectadas = cursor.rowcount
    conexion.commit()
    cursor.close()
    conexion.close()
    
    if filas_afectadas == 0:
        return jsonify({"mensaje": f"No existe paciente con ID {id}"}), 404
    
    return jsonify({"mensaje": f"Paciente con ID {id} actualizado correctamente"})

@pacientes_bp.route("/pacientes/<int:id>", methods=["DELETE"]) 
def eliminar_paciente(id):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute("DELETE FROM pacientes WHERE id = %s", (id,))
    filas_afectadas = cursor.rowcount
    conexion.commit()
    cursor.close()
    conexion.close()
    
    if filas_afectadas == 0:
        return jsonify({"mensaje": f"No existe paciente con ID {id}"}), 404
    
    return jsonify({"mensaje": f"Paciente con ID {id} eliminado correctamente"})