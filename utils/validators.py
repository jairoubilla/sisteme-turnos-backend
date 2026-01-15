from datetime import datetime

def validar_dni_argentino(dni):
    """Verifica que el DNI sea numérico y tenga una longitud razonable."""
    if not dni.isdigit():
        return False
    if len(dni) < 7 or len(dni) > 8:
        return False
    return True

def validar_fecha_futura(fecha_obj):
    """Verifica que la fecha del turno no sea anterior a hoy."""
    if fecha_obj < datetime.now().date():
        return False
    return True

def validar_horario_laboral(hora_obj):
    """Verifica que el turno esté dentro del horario del hospital (ej. 08:00 a 20:00)."""
    inicio = datetime.strptime("08:00", "%H:%M").time()
    fin = datetime.strptime("20:00", "%H:%M").time()
    return inicio <= hora_obj <= fin