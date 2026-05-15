from flask import Blueprint, request, jsonify
from app.models import db, Appointment

# Blueprint solo con endpoints de prueba para citas medicas
main = Blueprint('test', __name__)

@main.route('/')
@main.route('/dashboard')
def index():
    return '<h1>Corriendo en Modo de Prueba.</h1>'

@main.route('/citas', methods=['GET'])
def listar_citas():
    """
    Retorna una lista de todas las citas (JSON).
    """
    citas = Appointment.query.all()
    data = [
        {
            'id': cita.id,
            'fecha': cita.fecha.strftime('%Y-%m-%d %H:%M'),
            'motivo': cita.motivo,
            'status': cita.status,
            'paciente_id': cita.paciente_id,
            'medico_id': cita.medico_id
        }
        for cita in citas
    ]
    return jsonify(data), 200

@main.route('/citas/<int:id>', methods=['GET'])
def listar_una_cita(id):
    """
    Retorna una sola cita por su ID (JSON).
    """
    cita = Appointment.query.get_or_404(id)
    data = {
        'id': cita.id,
        'fecha': cita.fecha.strftime('%Y-%m-%d %H:%M'),
        'motivo': cita.motivo,
        'status': cita.status,
        'paciente_id': cita.paciente_id,
        'medico_id': cita.medico_id
    }
    return jsonify(data), 200

@main.route('/citas', methods=['POST'])
def crear_cita():
    """
    Crea una cita sin validacion.
    Espera JSON con 'fecha', 'motivo', 'paciente_id', 'medico_id'.
    """
    data = request.get_json()

    if not data:
        return jsonify({'error': 'No input data provided'}), 400

    from datetime import datetime
    cita = Appointment(
        fecha=datetime.strptime(data.get('fecha'), '%Y-%m-%d %H:%M'),
        motivo=data.get('motivo'),
        status=data.get('status', 'pendiente'),
        paciente_id=data.get('paciente_id'),
        medico_id=data.get('medico_id')
    )

    db.session.add(cita)
    db.session.commit()

    return jsonify({'message': 'Cita creada', 'id': cita.id}), 201

@main.route('/citas/<int:id>', methods=['PUT'])
def actualizar_cita(id):
    """
    Actualiza una cita sin validacion de permisos.
    """
    cita = Appointment.query.get_or_404(id)
    data = request.get_json()

    from datetime import datetime
    if data.get('fecha'):
        cita.fecha = datetime.strptime(data.get('fecha'), '%Y-%m-%d %H:%M')

    cita.motivo = data.get('motivo', cita.motivo)
    cita.status = data.get('status', cita.status)
    cita.paciente_id = data.get('paciente_id', cita.paciente_id)
    cita.medico_id = data.get('medico_id', cita.medico_id)

    db.session.commit()

    return jsonify({'message': 'Cita actualizada', 'id': cita.id}), 200

@main.route('/citas/<int:id>', methods=['DELETE'])
def eliminar_cita(id):
    """
    Elimina una cita sin validacion de permisos.
    """
    cita = Appointment.query.get_or_404(id)

    db.session.delete(cita)
    db.session.commit()

    return jsonify({'message': 'Cita eliminada', 'id': cita.id}), 200