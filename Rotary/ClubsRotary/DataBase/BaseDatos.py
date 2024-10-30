import sqlite3
from datetime import date

# Conectarse a la base de datos
conn = sqlite3.connect('databaseRotary.db')

# Crear un cursor para ejecutar comandos SQL
cursor = conn.cursor()

# Definir los comandos SQL para crear cada tabla, incluyendo la nueva tabla para el club
sql_commands = [
    '''
    CREATE TABLE IF NOT EXISTS Usuarios (
        club_id INTEGER PRIMARY KEY AUTOINCREMENT,
        correo TEXT UNIQUE,
        password TEXT
    );
    ''',
    '''
    CREATE TABLE IF NOT EXISTS Club (
        club_id INTEGER,
        nombre_club TEXT NOT NULL,
        direccion_club TEXT,
        reunion TEXT,
        ciudad_club TEXT,
        pais_club TEXT,
        fecha_fundacion DATE,
        distrito TEXT,
        zona TEXT,
        informacion_adicional TEXT
    );
    ''',
    '''
    CREATE TABLE IF NOT EXISTS Socios (
        usuario_id INTEGER PRIMARY KEY AUTOINCREMENT,
        club_id INTEGER,
        usuarioIDRotary TEXT,
        nombres TEXT NOT NULL,
        apellidos TEXT NOT NULL,
        correo TEXT UNIQUE,
        celular TEXT NOT NULL,
        celular_emergencia TEXT,
        direccion TEXT,
        fecha_nacimiento DATE,
        informacion_adicional TEXT,
        estado INTEGER,
        FOREIGN KEY (usuario_id) REFERENCES Usuarios(usuario_id),
        FOREIGN KEY (club_id) REFERENCES Club(club_id)
    );
    ''',
    '''
    CREATE TABLE IF NOT EXISTS Cargos_Junta (
        cargo_id INTEGER PRIMARY KEY AUTOINCREMENT,
        club_id INTEGER,
        nombre_cargo TEXT NOT NULL,
        descripcion TEXT,
        FOREIGN KEY (club_id) REFERENCES Club(club_id)
    );
    ''',
    '''
    CREATE TABLE IF NOT EXISTS Junta (
        club_id INTEGER,
        cargo_id INTEGER,
        usuario_id INTEGER NOT NULL,
        fecha_inicio DATE NOT NULL,
        fecha_fin DATE,
        FOREIGN KEY (usuario_id) REFERENCES Usuarios(usuario_id),
        FOREIGN KEY (cargo_id) REFERENCES Cargos_Junta(cargo_id),
        FOREIGN KEY (club_id) REFERENCES Club(club_id)
    );
    ''',
    '''
    CREATE TABLE IF NOT EXISTS Cargos_Comite (
        comite_id INTEGER PRIMARY KEY AUTOINCREMENT,
        club_id INTEGER,
        nombre_comite TEXT NOT NULL,
        descripcion TEXT,
        FOREIGN KEY (club_id) REFERENCES Club(club_id)
    );
    ''',
    '''
    CREATE TABLE IF NOT EXISTS Comite (
        comite_id INTEGER,
        club_id INTEGER,
        usuario_id INTEGER NOT NULL,
        fecha_inicio DATE NOT NULL,
        fecha_fin DATE,
        cargo INTEGER,
        FOREIGN KEY (comite_id) REFERENCES Cargos_Comite(comite_id),
        FOREIGN KEY (usuario_id) REFERENCES Usuarios(usuario_id),
        FOREIGN KEY (club_id) REFERENCES Club(club_id)
    );
    ''',
    '''
    CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        club_id INTEGER,
        title TEXT NOT NULL,
        start TEXT NOT NULL,
        end TEXT NOT NULL,
        FOREIGN KEY (club_id) REFERENCES Club(club_id)
    );
    '''
]

# Ejecutar cada comando SQL individualmente
for command in sql_commands:
    cursor.execute(command)

# Guardar los cambios en la base de datos
conn.commit()

# Cerrar la conexión
conn.close()

print("BDatos subidos correctamente.")
