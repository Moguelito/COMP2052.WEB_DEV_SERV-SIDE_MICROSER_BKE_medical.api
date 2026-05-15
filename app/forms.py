from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, SelectField
from wtforms.validators import DataRequired, Email, EqualTo, Length

# Formulario para login
class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

# Formulario para registrar un nuevo usuario
class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm password', validators=[DataRequired(), EqualTo('password')])

    role = SelectField(
        'Role',
        choices=[('Paciente', 'Paciente'), ('Medico', 'Medico')],
        validators=[DataRequired()]
    )
    submit = SubmitField('Register')

# Formulario para cambiar contraseña
class ChangePasswordForm(FlaskForm):
    old_password = PasswordField('Current password', validators=[DataRequired()])
    new_password = PasswordField('New password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm new password', validators=[DataRequired(), EqualTo('new_password')])
    submit = SubmitField('Update Password')

# Formulario para crear o editar una cita medica
class AppointmentForm(FlaskForm):
    # Usar un campo de texto simple para que el usuario lo escriba manualmente
    # Formato esperado: YYYY-MM-DD HH:MM (por ejemplo: 2026-06-01 09:30)
    fecha = StringField('Fecha y Hora', validators=[DataRequired()])
    motivo = TextAreaField('Motivo de la consulta', validators=[DataRequired()])
    submit = SubmitField('Guardar')