from flask import Flask, jsonify # Llamamos a flask
from flask_cors import CORS 
from routes.routes_pacientes import pacientes_bp
from routes.routes_turnos import turnos_bp
from routes.routes_medicos import medicos_bp

app = Flask(__name__) # crea la aplicacion flask

CORS(app, resources={r"/*": {"origins": [
    "https://aiturnos.up.railway.app",
    "https://sistema-turnos-frontend-production.up.railway.app"
    ]}})

# Manejo de errores 
@app.errorhandler(404)
def recurso_no_encontrado(e):
    """Maneja errores cuando la ruta no existe."""
    return jsonify({
        "error": "Recurso no encontrado",
        "mensaje": "La direccion que buscas no existe en el servidor del hospital."
    }), 404
    
@app.errorhandler(500)
def error_interno(e):
    """Maneja errores inesperados (ej. base de datos caída)."""
    return jsonify({
        "error": "Error interno del servidor",
        "mensaje": "Ocurrió un problema inesperado. Por favor, intente más tarde."
    }), 500

@app.errorhandler(Exception)
def manejar_excepcion_generica(e):
    """Atrapa cualquier otro error que no hayamos previsto."""
    return jsonify({
        "error": "Error desconocido",
        "detalle": str(e)
    }), 500
    
# Regitrando los Blueprints
app.register_blueprint(pacientes_bp)
app.register_blueprint(medicos_bp)
app.register_blueprint(turnos_bp)


@app.route("/") # define una ruta o direccion del servidor
def home(): # esto se ejecuta cuando alguien ingresa a la ruta
    return "Hola, servidor funcionando!" # esto responde el servidor


if __name__ == "__main__":
    # El host '0.0.0.0' permite conexiones externas
    # El port lo da el servidor de internet automáticamente
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
    