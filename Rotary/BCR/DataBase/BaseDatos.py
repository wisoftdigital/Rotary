import sqlite3
from datetime import date

# Conectarse a la base de datos
conn = sqlite3.connect('becados.db')

# Crear un cursor para ejecutar comandos SQL
cursor = conn.cursor()

# Definir los comandos SQL para crear cada tabla, incluyendo la nueva tabla para el club
sql_commands = [
    '''
    CREATE TABLE IF NOT EXISTS Usuarios (
        BCR_id INTEGER PRIMARY KEY AUTOINCREMENT,
        correo TEXT UNIQUE,
        password TEXT
    );
    ''',
    '''
    CREATE TABLE IF NOT EXISTS BCR (
        BCR_id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        pais TEXT NOT NULL,
        direccion_oficina TEXT,
        correo TEXT NOT NULL,
        celular TEXT,
        celular2 TEXT,
        sitio_web TEXT,
        instagram_url TEXT,
        facebook_url TEXT,
        linkedin_url TEXT,
        informacion_adicional TEXT
    );
    ''',
    '''
    CREATE TABLE IF NOT EXISTS Becados (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombres TEXT NOT NULL,
        apellidos TEXT NOT NULL,
        tipo_documento TEXT NOT NULL,
        numero_documento TEXT NOT NULL UNIQUE,
        direccion TEXT NOT NULL,
        municipio TEXT NOT NULL,
        fecha_nacimiento TEXT NOT NULL,
        celular1 TEXT NOT NULL,
        celular2 TEXT,
        correo TEXT NOT NULL,
        edad INTEGER,
        titulo_grado TEXT,
        pruebas_saber TEXT,
        estrato_social TEXT,
        club TEXT NOT NULL,
        universidad_postuladora TEXT,
        tipo_matricula_pin TEXR,
        numero_matricula_pin TEXT,
        porcentaje_u_completada INTEGER CHECK (porcentaje_u_completada >= 0 AND porcentaje_u_completada <= 100),
        rotario_padrino TEXT NOT NULL,
        estado TEXT NOT NULL CHECK (estado IN ('aspirante', 'becado'))
    );
    ''',
    '''
    CREATE TABLE IF NOT EXISTS AyudasBecados (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        becado_id INTEGER NOT NULL,
        porcentaje_estudiante INTEGER NOT NULL CHECK (porcentaje_estudiante >= 0 AND porcentaje_estudiante <= 100),
        porcentaje_institucion INTEGER NOT NULL CHECK (porcentaje_institucion >= 0 AND porcentaje_institucion <= 100),
        porcentaje_adicional INTEGER DEFAULT 0 CHECK (porcentaje_adicional >= 0 AND porcentaje_adicional <= 100),
        tipo_sostenimiento TEXT NOT NULL CHECK (tipo_sostenimiento IN ('alojamiento', 'alimentación', 'transporte', 'otro')),
        monto_sostenimiento DECIMAL(10, 2) NOT NULL DEFAULT 0,
        FOREIGN KEY (becado_id) REFERENCES Becados(id) ON DELETE CASCADE
    );
    ''',
    '''
    CREATE TABLE IF NOT EXISTS Calificaciones (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        becado_id INTEGER NOT NULL,
        materia TEXT NOT NULL,
        fecha DATE NOT NULL,
        semestre TEXT NOT NULL,
        calificacion DECIMAL(5, 2) NOT NULL CHECK (calificacion >= 0 AND calificacion <= 5),
        observaciones TEXT,
        FOREIGN KEY (becado_id) REFERENCES Becados(id) ON DELETE CASCADE
    );
    ''',
    '''
    CREATE TABLE IF NOT EXISTS EstadisticasBecados (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        total_becados INTEGER NOT NULL,
        total_aspirantes INTEGER NOT NULL,
        promedio_calificaciones DECIMAL(5, 2),
        promedio_ayuda DECIMAL(10, 2),
        porcentaje_asistencia DECIMAL(5, 2),
        distribucion_clubes TEXT,
        porcentaje_reciben_ayuda DECIMAL(5, 2),
        rendimiento_por_semestre TEXT
    );
    ''',
    '''
    CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        BCR_id INTEGER,
        title TEXT NOT NULL,
        start TEXT NOT NULL,
        end TEXT NOT NULL,
        FOREIGN KEY (BCR_id) REFERENCES BCR(BCR_id)
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

print("Datos subidos correctamente.")
