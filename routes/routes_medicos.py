from flask import Blueprint, request, jsonify
from database import obtener_conexion
from schemas import medico_schema, medicos_schema
from marshmallow import ValidationError

medicos_bp = Blueprint('medicos', __name__)

# GET: listar medicos
@medicos_bp.route("/medicos", methods=["GET"])
def obtener_medicos():
    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)
    # 1. Agregamos 'consultorio' a la consulta SQL
    cursor.execute("SELECT id, nombre, especialidad, telefono, matricula, consultorio FROM medicos") 
    resultados = cursor.fetchall()
    cursor.close()
    conexion.close()
    
    medicos = []
    for fila in resultados:
        medicos.append({
            "id": fila["id"],
            "nombre": fila["nombre"],
            "especialidad": fila["especialidad"],
            "telefono": fila["telefono"],
            "matricula": fila["matricula"],
            "consultorio": fila.get("consultorio") # 2. Lo agregamos a la respuesta
        })              
        
    return jsonify(medicos)

# POST: agregar medico
@medicos_bp.route("/medicos", methods=["POST"])
def agregar_medico():
    json_data = request.get_json()
    if not json_data:
        return jsonify({"mensaje": "No se enviaron datos"}), 400
    try:
        # Nota: Asegurate que en tu archivo schemas.py, el medico_schema también acepte 'consultorio'
        datos = medico_schema.load(json_data)
    
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        # 3. Agregamos 'consultorio' al INSERT
        cursor.execute(
            "INSERT INTO medicos (nombre, especialidad, telefono, matricula, consultorio) VALUES (%s, %s, %s, %s, %s)",
            (datos['nombre'], datos['especialidad'], datos.get('telefono'), datos['matricula'], datos.get('consultorio'))
        )
        conexion.commit()
        cursor.close()
        conexion.close()
    
        return jsonify({"mensaje": "Medico agregado correctamente"}), 201
    except ValidationError as err:
        return jsonify(err.messages), 400

# PUT: actualizar medico
@medicos_bp.route("/medicos/<int:id>", methods=["PUT"]) 
def actualizar_medico(id):
    datos = request.get_json()
    nombre = datos.get("nombre")
    especialidad = datos.get("especialidad")
    telefono = datos.get("telefono")
    consultorio = datos.get("consultorio") # 4. Recibimos el consultorio
    
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    # 5. Lo agregamos al UPDATE
    cursor.execute(
        "UPDATE medicos SET nombre = %s, especialidad = %s, telefono = %s, consultorio = %s WHERE id = %s",
        (nombre, especialidad, telefono, consultorio, id)
    )
    filas_afectadas = cursor.rowcount
    conexion.commit()
    cursor.close()
    conexion.close()
    
    if filas_afectadas == 0:
        return jsonify({"mensaje": f"No existe médico con ID {id}"}), 404
    
    return jsonify({"mensaje": f"Médico con ID {id} actualizado correctamente"})

# DELETE: eliminar médico (Se mantiene igual)
@medicos_bp.route("/medicos/<int:id>", methods=["DELETE"]) 
def eliminar_medico(id):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute("DELETE FROM medicos WHERE id = %s", (id,))
    filas_afectadas = cursor.rowcount
    conexion.commit()
    cursor.close()
    conexion.close()
    
    if filas_afectadas == 0:
        return jsonify({"mensaje": f"No existe médico con ID {id}"}), 404
    
    return jsonify({"mensaje": f"Médico con ID {id} eliminado correctamente"})