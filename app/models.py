from app import db, login_manager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

# Necesario para Flask-Login
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Roles: Paciente, Medico, Admin
class Role(db.Model):
    __tablename__ = 'role'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, nullable=False)

    users = db.relationship('User', backref='role', lazy=True)

# Usuarios del sistema
class User(UserMixin, db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'), nullable=False)

    # Relaciones con citas
    citas_paciente = db.relationship('Appointment', foreign_keys='Appointment.paciente_id', backref='paciente', lazy=True)
    citas_medico = db.relationship('Appointment', foreign_keys='Appointment.medico_id', backref='medico', lazy=True)

    def set_password(self, password: str):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)

# Citas medicas
class Appointment(db.Model):
    __tablename__ = 'appointment'

    id = db.Column(db.Integer, primary_key=True)
    fecha = db.Column(db.DateTime, nullable=False)
    motivo = db.Column(db.String(200), nullable=False)
    status = db.Column(db.String(50), default='pendiente')

    paciente_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    medico_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)