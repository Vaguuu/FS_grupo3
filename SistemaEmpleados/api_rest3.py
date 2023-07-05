import sqlite3
from flask import Flask, jsonify, request

DATABASE = 'prueba.db'

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def create_table():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tablaprueba (
            mn VARCHAR PRIMARY KEY, 
            nombre VARCHAR NOT NULL, 
            especialidad VARCHAR NOT NULL,
            correo VARCHAR NOT NULL,
            horarios VARCHAR NOT NULL,
            foto VARCHAR NOT NULL
        )''')
    conn.commit()
    cursor.close()
    conn.close()

def create_database():
    conn = sqlite3.connect(DATABASE)
    conn.close()
    create_table()

create_database()

class Profesional:
    def __init__(self, mn, nombre, especialidad, correo, horarios, foto):
        self.mn = mn
        self.nombre = nombre
        self.especialidad = especialidad
        self.correo = correo
        self.horarios = horarios
        self.foto = foto
    
    def modificar(self, nueva_especialidad, nuevo_correo, nuevos_horarios, nueva_foto):
        self.especialidad = nueva_especialidad
        self.correo = nuevo_correo
        self.horarios = nuevos_horarios
        self.foto = nueva_foto

class Staff:
    def __init__(self):
        self.conexion = get_db_connection()
        self.cursor = self.conexion.cursor()

    def agregar_profesional(self, mn, nombre, especialidad, correo, horarios, foto):
        profesional_existente = self.consultar_profesional(mn)
        if profesional_existente:
            return jsonify({'message': 'Ya existe un profesional con esa matrícula.'}), 404
        nuevo_profesional = Profesional(mn, nombre, especialidad, correo, horarios, foto)
        sql = f'INSERT INTO tablaprueba VALUES ("{mn}", "{nombre}", "{especialidad}", "{correo}", "{horarios}", "{foto}");'
        self.cursor.execute(sql)
        self.conexion.commit()
        return jsonify({'message': 'Profesional agregado correctamente al staff.'}), 200
    
    def consultar_profesional(self, mn):
        sql = f'SELECT * FROM tablaprueba WHERE nombre = {mn} OR mn = {mn};'
        self.cursor.execute(sql)
        row = self.cursor.fetchone()
        if row:
            mn, nombre, especialidad, correo, horarios, foto = row
            return Profesional(mn, nombre, especialidad, correo, horarios, foto)
        return None
    
    def modificar_profesional(self, mn, nueva_especialidad, nuevo_correo, nuevos_horarios, nueva_foto):
        profesional =  self.consultar_profesional(mn)
        if profesional:
            profesional.modificar(nueva_especialidad, nuevo_correo, nuevos_horarios, nueva_foto)
            sql = f'UPDATE tablaprueba SET especialidad = "{nueva_especialidad}", correo = "{nuevo_correo}", horarios = "{nuevos_horarios}", foto = "{nueva_foto}" WHERE nombre = {mn} OR mn = {mn};'
            self.cursor.execute(sql)
            self.conexion.commit()
            return jsonify({'message': 'Profesional modificado correctamente.'}), 200
        return jsonify({'message': 'El profesional no se encuentra en el staff.'}), 404

    def eliminar_profesional(self, mn):
        sql = f'DELETE from tablaprueba WHERE nombre = {mn} OR mn = {mn};'
        self.cursor.execute(sql)
        if self.cursor.rowcount > 0:
            self.conexion.commit()
            return jsonify({'message': 'Profesional removido del staff correctamente.'}), 200
        return jsonify({'message': 'El profesional no se encuentra en el staff.'}), 404

    def listar_profesionales(self):
        self.cursor.execute("SELECT * FROM tablaprueba")
        rows = self.cursor.fetchall()
        for row in rows:
            mn, nombre, especialidad, correo, horarios, foto = row
            profesional = {'mn': mn, 'nombre': nombre, 'especialidad': especialidad, 'correo': correo, 'horarios': horarios, 'foto': foto}
            staff.append(profesional)
        return jsonify(staff), 200
        

app = Flask(__name__)

staff = Staff()

@app.route('/staff/<path:mn>', methods=['GET'])
def obtener_profesional(mn):
    profesional = staff.consultar_profesional(mn)
    if profesional:
        return jsonify({
            'mn' : profesional.mn,
            'nombre' : profesional.nombre,
            'especialidad' : profesional.especialidad,
            'correo' : profesional.correo,
            'horarios' : profesional.horarios,
            'foto' : profesional.foto
        }), 200
    return jsonify({'message': 'El profesional no se encuentra en el staff.'}), 404

@app.route('/')
def index():
    return 'API de Staff'

@app.route('/staff', methods=['GET'])
def obtener_staff():
    return staff.listar_profesionales()

@app.route('/staff', methods=['POST'])
def agregar_profesional():
    mn = request.json.get('mn')
    nombre = request.json.get('nombre')
    especialidad = request.json.get('especialidad')
    correo = request.json.get('correo')
    horarios = request.json.get('horarios')
    foto = request.json.get('foto')
    return staff.agregar_profesional(mn,nombre,especialidad,correo,horarios,foto)

@app.route('/staff/<path:mn>', methods=['PUT'])
def modificar_profesional(mn):
    nueva_especialidad = request.json.get('especialidad')
    nuevo_correo = request.json.get('correo')
    nuevos_horarios = request.json.get('horarios')
    nueva_foto = request.json.get('foto')
    return staff.modificar_profesional(mn,nueva_especialidad,nuevo_correo,nuevos_horarios,nueva_foto)

@app.route('/staff/<path:mn>', methods=['DELETE'])
def eliminar_profesional(mn):
    return staff.eliminar_profesional(mn)

