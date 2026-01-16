from flask import Blueprint, request, jsonify
from database import obtener_conexion
from schemas import TurnoSchema 
from marshmallow import ValidationError

turnos_bp = Blueprint('turnos', __name__)
turno_schema = TurnoSchema()

# GET: listar turnos

@turnos_bp.route("/turnos", methods=["GET"])
def obtener_turnos():
    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True) #Crea un cursor que devuelve resultados
    query = """
        SELECT t.id, p.nombre AS paciente, p.telefono AS telefono_paciente,
                m.nombre AS medico, t.fecha, t.hora, t.motivo
        FROM turnos t
        JOIN pacientes p ON t.paciente_id = p.id
        JOIN medicos m ON t.medico_id = m.id
    """
    cursor.execute(query)
    resultados = cursor.fetchall() 
    for r in resultados:
        r['fecha'] = str(r['fecha'])
        r['hora'] = str(r['hora'])
    cursor.close() 
    conexion.close()    
        
    return jsonify(resultados)

#POST: agregar turno

@turnos_bp.route("/turnos", methods=["POST"])
def agregar_turno():
    json_data = request.get_json()
    if not json_data:
        return jsonify({"error": "Faltan datos en la petición"}), 400
    
    try:
        # Marshmallow valida tipos de datos y presencia de campos obligatorios
        # También convierte los strings de fecha/hora a objetos Python
        datos = turno_schema.load(json_data)
    except ValidationError as err:
        return jsonify({"errores": err.messages}), 400
    
    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)
    
    # Validacion para evitar dobles turnos para medicos
    cursor.execute(
        "SELECT COUNT(*) AS cantidad FROM turnos WHERE medico_id = %s AND fecha = %s AND hora = %s",
        (datos['medico_id'], datos['fecha'], datos['hora'])
    )
    if cursor.fetchone()["cantidad"] > 0:
        cursor.close()
        conexion.close()
        return jsonify({"mensaje": "El médico ya tiene un turno en ese horario"}), 400
    
    # Validacion para evitar dobles turnos para pacientes
    
    cursor.execute(
        "SELECT COUNT(*) AS cantidad FROM turnos WHERE paciente_id = %s AND fecha = %s AND hora = %s",
        (datos['paciente_id'], datos['fecha'], datos['hora'])
    )
    
    if cursor.fetchone()["cantidad"] > 0:
        cursor.close()
        conexion.close()
        
        return jsonify({"mensaje": "El paciente ya tiene un turno en ese horario"}), 400
    
    # Si no tiene turnos agendados sigue con el proceso
    
    cursor.execute(
        "INSERT INTO turnos (paciente_id, medico_id, fecha, hora, motivo) VALUES (%s, %s, %s, %s, %s)",
        (datos['paciente_id'], datos['medico_id'], datos['fecha'], datos['hora'], datos['motivo'])
    )
    
    conexion.commit()
    cursor.close()
    conexion.close()
    
    return jsonify({"mensaje": "Turno agregado correctamente"}), 201

#Put: actualizar turno

@turnos_bp.route("/turnos/<int:id>", methods=["PUT"]) 
def actualizar_turno(id):
    datos = request.get_json()
    fecha = datos.get("fecha")
    hora = datos.get("hora")
    motivo = datos.get("motivo")
    
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute(
        "UPDATE turnos SET fecha = %s, hora = %s, motivo = %s WHERE id = %s",
        (fecha, hora, motivo, id)
    )
    filas_afectadas = cursor.rowcount
    conexion.commit()
    cursor.close()
    conexion.close()
    
    if filas_afectadas == 0:
        return jsonify({"mensaje": f"No existe turno con ID {id}"}), 404
    
    return jsonify({"mensaje": f"Turno con ID {id} actualizado correctamente"})

#DELETE: eliminar turno

@turnos_bp.route("/turnos/<int:id>", methods=["DELETE"]) 
def eliminar_turno(id):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute("DELETE FROM turnos WHERE id = %s", (id,))
    filas_afectadas = cursor.rowcount
    conexion.commit()
    cursor.close()
    conexion.close()
    
    if filas_afectadas == 0:
        return jsonify({"mensaje": f"No existe turno con ID {id}"}), 404
    
    return jsonify({"mensaje": f"Turno con ID {id} eliminado correctamente"})

# turnos que tiene el medico en la proxima semana

@turnos_bp.route("/reportes/medico/<int:medico_id>", methods=["GET"])
def turnos_medico_semana(medico_id):
    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True) #Crea un cursor que devuelve resultados
    cursor.execute("""
        SELECT t.id, p.nombre AS paciente, t.fecha, t.hora, t.motivo
        FROM turnos t
        JOIN pacientes p ON t.paciente_id = p.id
        WHERE t.medico_id = %s
            AND t.fecha BETWEEN CURDATE() AND DATE_ADD(CURDATE(), INTERVAL 7 DAY)
        ORDER BY t.fecha, t.hora
    """, (medico_id,))
    resultados = cursor.fetchall() 
    cursor.close()
    conexion.close()     
        
    return jsonify(resultados)

# turnos que tiene el paciente en la proxima semana

@turnos_bp.route("/reportes/paciente/<int:paciente_id>", methods=["GET"])
def turnos_paciente(paciente_id):
    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True) #Crea un cursor que devuelve resultados
    cursor.execute("""
        SELECT t.id, p.nombre AS medico, t.fecha, t.hora, t.motivo
        FROM turnos t
        JOIN medicos m ON t.medico_id = m.id
        WHERE t.paciente_id = %s
        ORDER BY t.fecha, t.hora
    """, (paciente_id,))
    resultados = cursor.fetchall() 
    cursor.close() 
    conexion.close()    
    
    return jsonify(resultados)