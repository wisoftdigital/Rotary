import sqlite3

# Conectar a la base de datos
conn = sqlite3.connect('becados.db')
cursor = conn.cursor()

# Comandos SQL para insertar datos
sql_commands = [
    '''
    INSERT INTO Usuarios (BCR_id, correo, password) VALUES
    (1, 'juan.perez@example.com', 'password123'),
    (2, 'maria.gomez@example.com', 'securepass456'),
    (3, 'pedro.fernandez@example.com', 'mypassword789');
    ''',
    '''
    INSERT INTO tasks (title, BCR_id, start, end) VALUES
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
