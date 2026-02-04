from marshmallow import Schema, fields, validate, ValidationError
from utils.validators import validar_dni_argentino, validar_fecha_futura

class PacienteSchema(Schema):
    id = fields.Int(dump_only=True) # Solo para lectura
    nombre = fields.Str(required=True, validate=validate.Length(min=3))
    dni = fields.Str(required=True, validate=lambda x: validar_dni_argentino(x))
    telefono = fields.Str(required=False)
    
    
class MedicoSchema(Schema):
    id = fields.Int(dump_only=True)
    nombre = fields.Str(required=True)
    especialidad = fields.Str(required=True)
    matricula = fields.Str(required=True)
    telefono = fields.Str(required=False, allow_none=True)
    consultorio = fields.Str()
    
class TurnoSchema(Schema):
    id = fields.Int(dump_only=True)
    paciente_id = fields.Int(required=True)
    medico_id = fields.Int(required=True)
    fecha = fields.Date(required=True, validate=validar_fecha_futura) # Valida formato AAAA-MM-DD
    hora = fields.Time(required=True) # Valida formato HH:MM:SS
    motivo = fields.Str(required=True)
    estado = fields.Str(dump_default="Pendiente")
    
paciente_schema = PacienteSchema()
pacientes_schema = PacienteSchema(many=True)

medico_schema = MedicoSchema()
medicos_schema = MedicoSchema(many=True)

turno_schema = TurnoSchema()
turnos_schema = TurnoSchema(many=True)