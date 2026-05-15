from app import create_app, db
from app.models import Role, User

app = create_app()

with app.app_context():

    # Crear las tablas si no existen
    db.create_all()

    # Asegurarse de que los roles existen
    roles = ['Admin', 'Medico', 'Paciente']
    for role_name in roles:
        existing_role = Role.query.filter_by(name=role_name).first()
        if not existing_role:
            new_role = Role(name=role_name)
            db.session.add(new_role)
            print(f'Rol "{role_name}" creado.')
    db.session.commit()

    # Diccionario con usuarios a insertar
    users_data = [
        {
            "username": "Administrator",
            "email": "admin@example.com",
            "password": "admin123",
            "role_name": "Admin"
        },
        {
            "username": "Dr. Juan Perez",
            "email": "medico@example.com",
            "password": "medico123",
            "role_name": "Medico"
        },
        {
            "username": "Carlos Rivera",
            "email": "paciente@example.com",
            "password": "paciente123",
            "role_name": "Paciente"
        }
    ]

    for user_info in users_data:
        existing_user = User.query.filter_by(email=user_info['email']).first()
        if not existing_user:
            role = Role.query.filter_by(name=user_info['role_name']).first()
            user = User(
                username=user_info['username'],
                email=user_info['email'],
                role=role
            )
            user.set_password(user_info['password'])
            db.session.add(user)
            print(f'Usuario "{user.username}" creado con rol "{role.name}".')
        else:
            print(f'El usuario con email {user_info["email"]} ya existe.')

    db.session.commit()
    print("Todos los usuarios fueron procesados correctamente.")