from flask import Flask, redirect, url_for, render_template, session, request, send_from_directory, jsonify
import sqlite3
import os
from werkzeug.utils import secure_filename

from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'tu_clave_secreta'  # Cambia esto por una clave secreta

DATABASE = 'becados.db'  # Nombre de tu base de datos


app.config['UPLOAD_TITULO_FOLDER'] = 'uploads/titulos'
app.config['UPLOAD_PRUEBAS_FOLDER'] = 'uploads/pruebas'
app.config['UPLOAD_ESTRATO_FOLDER'] = 'uploads/estratos'


# Redirigir la ruta base '/' a la página de inicio de sesión '/login'
@app.route('/')
def home():
    return redirect(url_for('login'))

# Ruta para servir archivos de node_modules
@app.route('/node_modules/<path:filename>')
def send_node_module(filename):
    return send_from_directory(os.path.join(app.root_path, 'node_modules'), filename)

@app.route('/logout')
def logout():
    session.pop('email', None)
    return redirect('/login')

# Función para agregar un nuevo usuario a la base de datos
def agregar_usuario(email, password):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    try:
        # Consulta corregida: agregar SELECT
        cursor.execute('SELECT * FROM Usuarios WHERE correo = ?', (email,))
        existing_user = cursor.fetchone()
        
        if existing_user:
            return False, 'Ya existe un usuario registrado con este correo electrónico.'
        
        # Encriptar la contraseña
        hashed_password = generate_password_hash(password)
        
        # Insertar el nuevo usuario en la base de datos
        cursor.execute('INSERT INTO Usuarios (correo, password) VALUES (?, ?)', (email, hashed_password))
        conn.commit()
        return True, None
    
    except sqlite3.Error as e:
        print(f'Error al agregar usuario: {e}')
        return False, 'Error interno al intentar registrar el usuario.'
    
    finally:
        cursor.close()
        conn.close()


def check_credentials(email, password):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    try:
        cursor.execute('SELECT password FROM Usuarios WHERE correo = ?', (email,))
        user = cursor.fetchone()

        if user and check_password_hash(user[0], password):
            return True  # La contraseña es correcta
        else:
            return False
    
    except sqlite3.Error as e:
        print(f'Error al verificar credenciales: {e}')
        return False
    
    finally:
        cursor.close()
        conn.close()


@app.route('/login', methods=['GET', 'POST'])
def login():
    login_error = None
    registro_error = None

    if request.method == 'POST':
        if request.form.get('registro') == 'registro':
            # Registro de nuevos usuarios
            email = request.form['email']
            password = request.form['password']
            success, error_message = agregar_usuario(email, password)
            if success:
                session['email'] = email
                return redirect('/Dashboard')  # Redirigir a la página de inicio después del registro
            else:
                registro_error = error_message

        else:
            # Inicio de sesión
            email = request.form['email']
            password = request.form['password']
            if check_credentials(email, password):
                session['email'] = email
                return redirect('/Dashboard')  # Redirigir a la página de inicio después de iniciar sesión
            else:
                login_error = 'Correo electrónico o contraseña incorrectos'
    
    return render_template('login.html', login_error=login_error, registro_error=registro_error)

# Endpoint para verificar si la postulación existe
@app.route('/verificar_postulacion', methods=['GET'])
def verificar_postulacion():
    numero_documento = request.args.get('numero_documento')
    
    # Lógica para buscar en la base de datos
    postulante = buscar_postulante(numero_documento)  # Reemplaza esto con tu lógica de consulta

    if postulante:
        return jsonify({
            "existe": True,
            "nombres": postulante['nombres'],
            "apellidos": postulante['apellidos'],
            "fecha_nacimiento": postulante['fecha_nacimiento'],
            "tipo_documento": postulante['tipo_documento'],
            "numero_documento": postulante['numero_documento'],
            "direccion": postulante['direccion'],
            "municipio": postulante['municipio'],
            "celular1": postulante['celular1'],
            "celular2": postulante['celular2'],
            "correo": postulante['correo']
        })
    else:
        return jsonify({"existe": False})

# Método de ejemplo para búsqueda (debes implementar la lógica real)
def buscar_postulante(numero_documento):
    # Aquí iría la lógica real, posiblemente una consulta SQL
    # Esto es un ejemplo de un postulante
    return {
        "nombres": "Juan",
        "apellidos": "Pérez",
        "fecha_nacimiento": "2000-01-01",
        "tipo_documento": "cc",
        "numero_documento": numero_documento,
        "direccion": "Calle 123",
        "municipio": "Medellín",
        "celular1": "3001234567",
        "celular2": "3107654321",
        "correo": "juan.perez@example.com"
    }


@app.route('/inscripcion', methods=['POST'])
def inscripcion():
    print(request.form)  # Para ver qué datos se están recibiendo
    # Obtener datos del formulario
    nombres = request.form['nombres']
    apellidos = request.form['apellidos']
    tipo_documento = request.form['tipo-documento']
    numero_documento = request.form['numero-documento']
    direccion = request.form['direccion']
    municipio = request.form['municipio']
    fecha_nacimiento = request.form['fecha-nacimiento']
    celular1 = request.form['celular1']
    celular2 = request.form.get('celular2', '')  # Puede ser opcional
    correo = request.form['correo']
    club = request.form['club']
    rotario_padrino = request.form['rotario']
    
    # Captura de matrícula o PIN
    tipo_mat_pin = request.form['tipo_mat_pin']
    numero_mat_pin = request.form['numero_mat_pin']

    
    estado = request.form.get('estado', 'aspirante')  # 'aspirante' como valor por defecto

    # Captura del estado (por defecto "aspirante")
    estado = request.form['estado']

    # Guardar archivos
    titulo_file = request.files['titulo_grado']
    pruebas_saber_file = request.files['pruebas_saber']
    estrato_file = request.files['estrato_social']

    # Cambiar nombre de archivo usando el número de documento
    titulo_filename = f"{numero_documento}_titulo.{secure_filename(titulo_file.filename).split('.')[-1]}"
    pruebas_saber_filename = f"{numero_documento}_pruebas.{secure_filename(pruebas_saber_file.filename).split('.')[-1]}"
    estrato_filename = f"{numero_documento}_estrato.{secure_filename(estrato_file.filename).split('.')[-1]}"

    # Crear las carpetas si no existen
    os.makedirs(app.config['UPLOAD_TITULO_FOLDER'], exist_ok=True)
    os.makedirs(app.config['UPLOAD_PRUEBAS_FOLDER'], exist_ok=True)
    os.makedirs(app.config['UPLOAD_ESTRATO_FOLDER'], exist_ok=True)

    # Guardar los archivos en las carpetas correspondientes
    titulo_file.save(os.path.join(app.config['UPLOAD_TITULO_FOLDER'], titulo_filename))
    pruebas_saber_file.save(os.path.join(app.config['UPLOAD_PRUEBAS_FOLDER'], pruebas_saber_filename))
    estrato_file.save(os.path.join(app.config['UPLOAD_ESTRATO_FOLDER'], estrato_filename))

    # Guardar la ruta de los archivos en la base de datos
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO Becados (nombres, apellidos, tipo_documento, numero_documento, direccion, municipio, fecha_nacimiento, celular1, celular2, correo, titulo_grado, pruebas_saber, estrato_social, club, rotario_padrino, tipo_matricula_pin, numero_matricula_pin, estado)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (nombres, apellidos, tipo_documento, numero_documento, direccion, municipio, fecha_nacimiento, celular1, celular2, correo, 
          os.path.join(app.config['UPLOAD_TITULO_FOLDER'], titulo_filename),
          os.path.join(app.config['UPLOAD_PRUEBAS_FOLDER'], pruebas_saber_filename),
          os.path.join(app.config['UPLOAD_ESTRATO_FOLDER'], estrato_filename),
          club, rotario_padrino, tipo_mat_pin, numero_mat_pin, estado))  # Agregar estado

    conn.commit()
    conn.close()

    return 'Inscripción exitosa'



def obtener_becados():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    try:
        cursor.execute('SELECT * FROM Becados')
        # Obtiene todos los becados
        becados = cursor.fetchall()
        
        # Opcional: Convertir a diccionarios para una mejor legibilidad
        column_names = [description[0] for description in cursor.description]
        return [dict(zip(column_names, becado)) for becado in becados]
    
    except sqlite3.Error as e:
        print(f'Error al obtener becados: {e}')
        return []  # Retorna una lista vacía en caso de error
    
    finally:
        cursor.close()  # Asegúrate de cerrar el cursor
        conn.close()    # Asegúrate de cerrar la conexión


@app.route('/Dashboard')
def DashboardPH():
    if 'email' in session:
        email = session['email']
        
        try:
            # Obtener la lista de becados utilizando la función
            becados = obtener_becados()
            return render_template('Dashboard.html', email=email, becados=becados)
        except Exception as e:
            print(f'Error en el dashboard: {e}')
            return redirect('/login')
    else:
        return redirect('/login')



# Ruta para agregar una nueva tarea
@app.route('/add_task', methods=['POST'])
def add_task():
    conn = sqlite3.connect(DATABASE)  
    cursor = conn.cursor()
    
    title = request.json['title']
    start = request.json['start']
    end = request.json['end']
    
    cursor.execute('INSERT INTO tasks (title, start, end) VALUES (?, ?, ?)', (title, start, end))
    conn.commit()
    
    task_id = cursor.lastrowid
    
    cursor.close()
    conn.close()
    
    return jsonify({"id": task_id})

# Ruta para actualizar una tarea existente
@app.route('/update_task/<int:id>', methods=['POST'])
def update_task(id):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    start = request.json['start']
    end = request.json['end']
    
    cursor.execute('UPDATE tasks SET start = ?, end = ? WHERE id = ?', (start, end, id))
    conn.commit()
    
    cursor.close()
    conn.close()
    
    return jsonify({"status": "Task updated!"})

# Ruta para eliminar una tarea existente
@app.route('/delete_task/<int:id>', methods=['DELETE'])
def delete_task(id):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    cursor.execute('DELETE FROM tasks WHERE id = ?', (id,))
    conn.commit()
    
    cursor.close()
    conn.close()
    
    return jsonify({"status": "Task deleted!"})

# Ruta para obtener todas las tareas
@app.route('/get_tasks')
def get_tasks():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('SELECT id, title, start, end FROM tasks')
    tasks = cursor.fetchall()

    cursor.close()
    conn.close()
    
    tasks_data = [{"id": t[0], "title": t[1], "start": t[2], "end": t[3]} for t in tasks]
    
    return jsonify(tasks_data)



@app.route('/Formulario')
def ejemplo():
    return render_template('formulario.html')  # Asegúrate de que este archivo exista

if __name__ == '__main__':
    # Iniciar la aplicación Flask
    #app.run(debug=True, port=5001)
    app.run(debug=True, host='0.0.0.0', port=5001)
