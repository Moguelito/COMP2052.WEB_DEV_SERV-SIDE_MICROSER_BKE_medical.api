from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from app.forms import AppointmentForm, ChangePasswordForm
from app.models import db, Appointment, User
from datetime import datetime

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/dashboard')
@login_required
def dashboard():
    if current_user.role.name == 'Paciente':
        citas = Appointment.query.filter_by(paciente_id=current_user.id).all()
    elif current_user.role.name == 'Medico':
        citas = Appointment.query.filter_by(medico_id=current_user.id).all()
    else:
        # Admin ve todas las citas
        citas = Appointment.query.all()

    return render_template('dashboard.html', citas=citas)

@main.route('/citas/crear', methods=['GET', 'POST'])
@login_required
def crear_cita():
    # Solo pacientes pueden crear citas
    if current_user.role.name != 'Paciente':
        flash('No tienes permiso para crear citas.')
        return redirect(url_for('main.dashboard'))

    form = AppointmentForm()

    if form.validate_on_submit():
        # Parsear la fecha introducida manualmente por el usuario
        try:
            fecha_dt = datetime.strptime(form.fecha.data.strip(), '%Y-%m-%d %H:%M')
        except Exception:
            flash('Formato de fecha inválido. Usa YYYY-MM-DD HH:MM (p.ej. 2026-06-01 09:30).')
            return render_template('cita_form.html', form=form)

        cita = Appointment(
            fecha=fecha_dt,
            motivo=form.motivo.data,
            paciente_id=current_user.id,
            medico_id=1  # esto lo mejoraremos despues
        )
        db.session.add(cita)
        db.session.commit()
        flash('Cita creada exitosamente.')
        return redirect(url_for('main.dashboard'))

    return render_template('cita_form.html', form=form)

@main.route('/citas/<int:id>/editar', methods=['GET', 'POST'])
@login_required
def editar_cita(id):
    cita = Appointment.query.get_or_404(id)

    # Solo el paciente dueño o admin puede editar
    if current_user.role.name not in ['Admin', 'Paciente'] or (
        cita.paciente_id != current_user.id and current_user.role.name != 'Admin'):
        flash('No tienes permiso para editar esta cita.')
        return redirect(url_for('main.dashboard'))

    # Inicializar el formulario con los valores existentes
    # Convertir la fecha a string con el formato esperado
    form = AppointmentForm(obj=cita)
    # Si WTForms puso un objeto datetime en form.fecha.data, convertirlo
    if isinstance(form.fecha.data, datetime):
        form.fecha.data = form.fecha.data.strftime('%Y-%m-%d %H:%M')
    elif not form.fecha.data:
        form.fecha.data = cita.fecha.strftime('%Y-%m-%d %H:%M')

    if form.validate_on_submit():
        # Parsear la fecha manual
        try:
            fecha_dt = datetime.strptime(form.fecha.data.strip(), '%Y-%m-%d %H:%M')
        except Exception:
            flash('Formato de fecha inválido. Usa YYYY-MM-DD HH:MM (p.ej. 2026-06-01 09:30).')
            return render_template('cita_form.html', form=form, editar=True)

        cita.fecha = fecha_dt
        cita.motivo = form.motivo.data
        db.session.commit()
        flash('Cita actualizada exitosamente.')
        return redirect(url_for('main.dashboard'))

    return render_template('cita_form.html', form=form, editar=True)

@main.route('/citas/<int:id>/eliminar', methods=['POST'])
@login_required
def eliminar_cita(id):
    cita = Appointment.query.get_or_404(id)

    if current_user.role.name not in ['Admin', 'Paciente'] or (
        cita.paciente_id != current_user.id and current_user.role.name != 'Admin'):
        flash('No tienes permiso para eliminar esta cita.')
        return redirect(url_for('main.dashboard'))

    db.session.delete(cita)
    db.session.commit()
    flash('Cita eliminada exitosamente.')
    return redirect(url_for('main.dashboard'))

@main.route('/cambiar-password', methods=['GET', 'POST'])
@login_required
def cambiar_password():
    form = ChangePasswordForm()

    if form.validate_on_submit():
        if not current_user.check_password(form.old_password.data):
            flash('La contraseña actual es incorrecta.')
            return render_template('cambiar_password.html', form=form)

        current_user.set_password(form.new_password.data)
        db.session.commit()
        flash('Contraseña actualizada exitosamente.')
        return redirect(url_for('main.dashboard'))

    return render_template('cambiar_password.html', form=form)

@main.route('/usuarios')
@login_required
def listar_usuarios():
    if current_user.role.name != 'Admin':
        flash('No tienes permiso para ver esta página.')
        return redirect(url_for('main.dashboard'))

    usuarios = User.query.join(User.role).all()

    return render_template('usuarios.html', usuarios=usuarios)


@main.route('/usuarios/<int:id>/eliminar', methods=['POST'])
@login_required
def eliminar_usuario(id):
    # Solo Admin puede eliminar usuarios
    if current_user.role.name != 'Admin':
        flash('No tienes permiso para realizar esta acción.')
        return redirect(url_for('main.dashboard'))

    # Evitar que un admin se elimine a sí mismo
    if current_user.id == id:
        flash('No puedes eliminar tu propia cuenta.')
        return redirect(url_for('main.listar_usuarios'))

    usuario = User.query.get_or_404(id)

    # Eliminar citas relacionadas (como paciente o médico) para evitar errores de FK
    try:
        Appointment.query.filter_by(paciente_id=id).delete()
        Appointment.query.filter_by(medico_id=id).delete()
        db.session.delete(usuario)
        db.session.commit()
        flash(f'Usuario {usuario.username} eliminado correctamente.')
    except Exception as e:
        db.session.rollback()
        flash('Ocurrió un error al intentar eliminar el usuario.')

    return redirect(url_for('main.listar_usuarios'))