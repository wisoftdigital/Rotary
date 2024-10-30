from flask import Flask, render_template, send_from_directory, request, redirect, url_for, jsonify, g, session
import sqlite3
import os

app = Flask(__name__)
app.secret_key = 'tu_clave_secreta'  # Clave secreta para manejar sesiones

# Configura la conexión a la base de datos SQLite
DATABASE = 'databaseRotary.db'

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
        # Verificar si ya existe un usuario con el mismo correo electrónico
        cursor.execute('SELECT club_id FROM Usuarios WHERE correo = ?', (email,))
        existing_user = cursor.fetchone()
        
        if existing_user:
            return False, 'Ya existe un usuario registrado con este correo electrónico.'
        
        # Insertar el nuevo usuario en la base de datos
        cursor.execute('INSERT INTO Usuarios (correo, password) VALUES (?, ?)', (email, password))
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
        cursor.execute('SELECT club_id FROM Usuarios WHERE correo = ? AND password = ?', (email, password))
        user = cursor.fetchone()

        if user:
            # Extraer el club_id de la tupla y retornar solo el valor
            club_id = user[0]
            return club_id
        else:
            return None
    
    except sqlite3.Error as e:
        print(f'Error al verificar credenciales: {e}')
        return None
    
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
                return redirect('/login')  # Redirigir a la página de inicio después del registro
            else:
                registro_error = error_message

        else:
            # Inicio de sesión
            email = request.form['email']
            password = request.form['password']
            club_id = check_credentials(email, password)
            if club_id is not None:
                session['email'] = email
                session['club_id'] = club_id  # Asegúrate de que club_id sea un valor entero
                return redirect('/Dashboard')  # Redirigir a la página de inicio después de iniciar sesión
            else:
                login_error = 'Correo electrónico o contraseña incorrectos'
    
    return render_template('login.html', login_error=login_error, registro_error=registro_error)

def obtener_socios(club_id):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    try:
        cursor.execute('''
            SELECT 
                usuario_id, 
                club_id, 
                usuarioIDRotary, 
                nombres, 
                apellidos, 
                correo, 
                celular, 
                celular_emergencia, 
                direccion, 
                fecha_nacimiento, 
                informacion_adicional, 
                estado  
            FROM Socios 
            WHERE club_id = ?
        ''', (club_id,))
        columnas = [desc[0] for desc in cursor.description]
        socios = [dict(zip(columnas, fila)) for fila in cursor.fetchall()]
        return socios
    
    except sqlite3.Error as e:
        print(f'Error al recuperar socios: {e}')
        return []
    
    finally:
        cursor.close()
        conn.close()

def obtener_junta(club_id):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    try:
        cursor.execute('''
            SELECT 
                Junta.cargo_id, 
                Cargos_Junta.nombre_cargo, 
                Socios.nombres, 
                Socios.apellidos, 
                Junta.fecha_inicio, 
                Junta.fecha_fin
            FROM Junta
            JOIN Cargos_Junta ON Junta.cargo_id = Cargos_Junta.cargo_id
            JOIN Socios ON Junta.usuario_id = Socios.usuario_id
            WHERE Junta.club_id = ?
        ''', (club_id,))
        columnas = [desc[0] for desc in cursor.description]
        junta = [dict(zip(columnas, fila)) for fila in cursor.fetchall()]
        return junta
    
    except sqlite3.Error as e:
        print(f'Error al recuperar la junta: {e}')
        return []
    
    finally:
        cursor.close()
        conn.close()

def obtener_comites(club_id):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    try:
        cursor.execute('''
            SELECT 
                Comite.comite_id, 
                Cargos_Comite.nombre_comite, 
                Socios.nombres, 
                Socios.apellidos, 
                Comite.fecha_inicio, 
                Comite.fecha_fin, 
                Comite.cargo
            FROM Comite
            JOIN Cargos_Comite ON Comite.comite_id = Cargos_Comite.comite_id
            JOIN Socios ON Comite.usuario_id = Socios.usuario_id
            WHERE Comite.club_id = ?
        ''', (club_id,))
        
        columnas = [desc[0] for desc in cursor.description]
        filas = cursor.fetchall()
        
        comites = {}
        for fila in filas:
            comite_id = fila[0]
            if comite_id not in comites:
                comites[comite_id] = {
                    'comite_id': comite_id,
                    'nombre_comite': fila[1],
                    'fecha_inicio': fila[4],
                    'fecha_fin': fila[5],
                    'cargo': fila[6],
                    'miembros': []
                }
            comites[comite_id]['miembros'].append({
                'nombres': fila[2],
                'apellidos': fila[3]
            })
        
        return list(comites.values())
    
    except sqlite3.Error as e:
        print(f'Error al recuperar comités: {e}')
        return []
    
    finally:
        cursor.close()
        conn.close()


@app.route('/Dashboard')
def DashboardPH():
    if 'email' in session:
        email = session['email']
        club_id = session.get('club_id')  # Obtener club_id de la sesión
        
        print(f'Tipo de club_id: {type(club_id)}, Valor de club_id: {club_id}')  # Para depuración

        if isinstance(club_id, tuple):
            # Si club_id es una tupla, extrae el primer elemento
            club_id = club_id[0]

        try:
            club_id = int(club_id)  # Asegúrate de convertir club_id a entero si es necesario
        except (ValueError, TypeError):
            return redirect('/login')

        # Obtener la lista de socios del club utilizando la función
        socios = obtener_socios(club_id)
        junta = obtener_junta(club_id)
        comites = obtener_comites(club_id)
        return render_template('Dashboard.html', email=email, club_id=club_id, socios=socios, junta=junta, comites=comites)
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





@app.route('/Ejemplo')
def ejemplo():
    return render_template('Ejemplo.html')  # Asegúrate de que este archivo exista

if __name__ == '__main__':
    # Iniciar la aplicación Flask
    #app.run(debug=True, port=5001)
    app.run(debug=True, host='0.0.0.0', port=5001)
