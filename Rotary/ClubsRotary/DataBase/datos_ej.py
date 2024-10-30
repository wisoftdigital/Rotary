import sqlite3

# Conectar a la base de datos
conn = sqlite3.connect('databaseRotary.db')
cursor = conn.cursor()

# Comandos SQL para insertar datos
sql_commands = [
    '''
    INSERT INTO Usuarios (club_id, correo, password) VALUES
    (1, 'juan.perez@example.com', 'password123'),
    (2, 'maria.gomez@example.com', 'securepass456'),
    (3, 'pedro.fernandez@example.com', 'mypassword789');
    ''',
    '''
    INSERT INTO Club (club_id, nombre_club, direccion_club, reunion, ciudad_club, pais_club, fecha_fundacion, distrito, zona, informacion_adicional) VALUES
    (1, 'Club Rotaract Medellín', 'Calle 70 #5-30', 'Primer lunes de cada mes', 'Medellín', 'Colombia', '2000-01-15', 'Distrito 4281', 'Zona 1', 'Club dedicado a la juventud'),
    (2, 'Club Rotaract Higüey', 'Avenida 3 #10-5', 'Segundo martes de cada mes', 'Higüey', 'República Dominicana', '2005-05-20', 'Distrito 4200', 'Zona 3', 'Club con enfoque en el desarrollo comunitario');
    ''',
    '''
    INSERT INTO Socios (usuario_id, club_id, usuarioIDRotary, nombres, apellidos, correo, celular, celular_emergencia, direccion, fecha_nacimiento, informacion_adicional, estado) VALUES
    (1, 1, 'ROT1234', 'Juan', 'Pérez', 'juan.perez@example.com', '300-123-4567', '310-765-4321', 'Calle 50 #45-67', '1990-08-15', 'Presidente del Club', 1),
    (2, 1, 'ROT5678', 'María', 'Gómez', 'maria.gomez@example.com', '300-234-5678', '310-876-5432', 'Calle 60 #78-90', '1992-11-22', 'Secretaria', 1),
    (3, 1, 'ROT9101', 'Pedro', 'Fernández', 'pedro.fernandez@example.com', '300-345-6789', '310-987-6543', 'Calle 70 #12-34', '1991-05-10', 'Tesorero', 1);
    ''',
    '''
    INSERT INTO Cargos_Junta (club_id, nombre_cargo, descripcion) VALUES
    (1, 'Presidente', 'Responsable del club y sus actividades'),
    (1, 'Secretaria', 'Encargada de la documentación y correspondencia'),
    (1, 'Tesorero', 'Manejo de las finanzas del club'),
    (2, 'Presidente', 'Líder del club Rotaract Higüey'),
    (2, 'Secretaria', 'Administración de los registros del club');
    ''',
    '''
    INSERT INTO Junta (club_id, cargo_id, usuario_id, fecha_inicio, fecha_fin) VALUES
    (1, 1, 1, '2024-01-01', NULL),
    (1, 2, 2, '2024-01-01', NULL),
    (1, 3, 2, '2024-01-01', NULL),
    (2, 1, 3, '2024-01-01', NULL),
    (2, 2, 2, '2024-01-01', NULL);
    ''',
    '''
    INSERT INTO Cargos_Comite (club_id, nombre_comite, descripcion) VALUES
    (1, 'Comité de Proyectos', 'Encargado de coordinar y ejecutar proyectos del club'),
    (1, 'Comité de Eventos', 'Organización de eventos y actividades sociales'),
    (2, 'Comité de Educación', 'Proyectos relacionados con la educación'),
    (2, 'Comité de Salud', 'Iniciativas y programas de salud para la comunidad');
    ''',
    '''
    INSERT INTO Comite (club_id, comite_id, usuario_id, fecha_inicio, fecha_fin) VALUES
    (1, 1, 1, '2024-01-01', NULL),
    (1, 2, 2, '2024-01-01', NULL),
    (2, 1, 3, '2024-01-01', NULL),
    (2, 2, 2, '2024-01-01', NULL);
    ''',
    '''
    INSERT INTO tasks (title, club_id, start, end) VALUES
    ("Evento 1", 1, "2024-09-12T10:00:00","2024-09-12T12:00:00"),
    ("Evento 2", 1, "2024-09-12T13:00:00","2024-09-12T14:30:00");
    '''
]

# Ejecutar los comandos SQL
for command in sql_commands:
    cursor.executescript(command)

# Confirmar los cambios y cerrar la conexión
conn.commit()
conn.close()

print("BDatos subidos correctamente.")
