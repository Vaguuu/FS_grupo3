# coding=utf-8
import sqlite3

DATABASE = "staff.db"

def get_db_connection():
    print("Obteniendo conexion...")
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def create_database():
    print("Creando base de datos...")
    conn = sqlite3.connect(DATABASE)
    conn.close()
    create_table()

def create_table():
    print("Creando tabla de profesionales...")
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS staff (
            nombre TEXT NOT NULL,
            especialidad TEXT NOT NULL,
            mn INTEGER NOT NULL,
            horarios TEXT NOT NULL
        ) ''')
    conn.commit()
    cursor.close()
    conn.close()

create_database()

class Medico:
    def __init__(self, nombre, especialidad, mn, horarios):
        self.nombre = nombre
        self.especialidad = especialidad
        self.mn = mn # matricula nacional
        self.horarios = horarios
    
    def update(self, nuevos_horarios):
        self.horarios = nuevos_horarios

medico = Medico('Juan Perez', 'Obstetricia', 123456, 'Lunes a viernes de 10.00 a 14.00 horas.')

class Staff:
    def __init__(self):
        self.conexion = get_db_connection()
        self.cursor = self.conexion.cursor()
    
    def create_medico(self, nombre, especialidad, mn, horarios):
        medico_existente = self.consultar_medico(nombre)
        if medico_existente:
            print("Ya está cargado dicho profesional.")
            return False
        nuevo_medico = Medico(nombre, especialidad, mn, horarios)
        sql = f'INSERT INTO staff VALUES ("{nombre}", "{especialidad}", {mn}, "{horarios}");'
        self.cursor.execute(sql)
        self.conexion.commit()
        return True

    def consultar_medico(self, nombre):
        sql = f'SELECT * FROM staff WHERE nombre = {nombre};'
        self.cursor.execute(sql)
        row = self.cursor.fetchone()
        if row:
            nombre, especialidad, mn, horarios = row
            return Medico(nombre, especialidad, mn, horarios)
        return False
    
    def update_medico(self, nombre, nuevos_horarios):
        medico = self.consultar_medico(nombre)
        if medico:
            medico.update(nuevos_horarios)
            sql = f'UPDATE staff SET horarios = {nuevos_horarios} WHERE nombre = {nombre};'
            self.cursor.execute(sql)
            self.conexion.commit()
            
    def delete_medico(self, nombre):
        sql = f'DELETE FROM staff WHERE nombre = {nombre};'
        self.cursor.execute(sql)
        if self.cursor.rowcount > 0:
            print(f'El profesional {nombre} ha sido eliminado del staff.')
            self.conexion.commit()
        else:
            print(f'{nombre} no se encuentra en el staff.')

    def read_medicos(self):
        print("Listado de médicos en el Staff:")
        print("Nombre\t\tEspecialidad\tM.N.\tHorarios")
        self.cursor.execute("SELECT * FROM staff")
        rows = self.cursor.fetchall()
        for row in rows:
            nombre, especialidad, mn, horarios = row
            print('{nombre}\t{especialidad}\t{mn}\t{horarios}')

mi_staff = Staff()

mi_staff.create_medico('Juan Perez', 'Obstetricia', 123456, 'Lunes a viernes de 10.00 a 14.00 horas.')
mi_staff.create_medico('María Gomez', 'Cuello uterino', 111111, 'Martes y jueves de 10.00 a 20.00 horas.')
mi_staff.create_medico('Paola Lopez', 'Mastologia', 555555, 'Miércoles y viernes de 15.00 a 20.00 horas.')
