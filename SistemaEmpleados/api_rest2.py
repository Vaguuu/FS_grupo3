import sqlite3

DATABASE = 'prueba.db'

def get_db_connection():
    print("Obteniendo conexión...")
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def create_table():
    print("Creando tabla de staff...")
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
    print("Creando la base de datos...")
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
            print("Ya existe un profesional con esa matrícula.")
            return False
        nuevo_profesional = Profesional (mn, nombre, especialidad, correo, horarios, foto)
        sql = f'INSERT INTO tablaprueba VALUES ("{mn}", "{nombre}", "{especialidad}", "{correo}", "{horarios}", "{foto}");'
        self.cursor.execute(sql)
        self.conexion.commit()
        return True    
    
    def consultar_profesional(self, nombre):
        sql = f'SELECT * FROM tablaprueba WHERE nombre = {nombre} OR mn = {nombre};'
        self.cursor.execute(sql)
        row = self.cursor.fetchone()
        if row:
            mn, nombre, especialidad, correo, horarios, foto = row
            return Profesional(mn, nombre, especialidad, correo, horarios, foto)
        return False
    
    def modificar_profesional(self, nombre, nueva_especialidad, nuevo_correo, nuevos_horarios, nueva_foto):
        profesional =  self.consultar_profesional(nombre)
        if profesional:
            profesional.modificar(nueva_especialidad, nuevo_correo, nuevos_horarios, nueva_foto)
            sql = f'UPDATE tablaprueba SET especialidad = "{nueva_especialidad}", correo = "{nuevo_correo}", horarios = "{nuevos_horarios}", foto = "{nueva_foto}" WHERE nombre = {nombre} OR mn = {nombre};'
            self.cursor.execute(sql)
            self.conexion.commit()

    def eliminar_profesional(self, nombre):
        sql = f'DELETE from tablaprueba WHERE nombre = {nombre} OR mn = {nombre};'
        self.cursor.execute(sql)
        if self.cursor.rowcount > 0:
            print(f'El profesional {nombre} ha sido removido del staff.')
            self.conexion.commit()
        else:
            print(f'El profesional {nombre} no se encuentra en el staff.')

    def listar_profesionales(self):
        print("-"*30)
        print("Listado del Staff:")
        print("MN\tNOMBRE\t\tESPECIALIDAD\t\tCORREO\t\tHORARIOS\t\tFOTO")
        self.cursor.execute("SELECT * FROM tablaprueba")
        rows = self.cursor.fetchall()
        for row in rows:
            mn, nombre, especialidad, correo, horarios, foto = row
            print(f'{mn}\t{nombre}\t\t{especialidad}\t\t{correo}\t\t{horarios}\t\t{foto}')
        print("-"*30)

create_database()
mi_staff = Staff()

# mi_staff.agregar_profesional("444444","Juan Carlos Perez","Obstetra","jcperez@gmail.com","Lunes 10.00 a 20.00 horas.", "444444User.png")
# mi_staff.agregar_profesional("222222","Ana Laura Gomez","Fertilidad","algomez@gmail.com","Martes 10.00 a 20.00 horas.", "222222User.png")
# mi_staff.agregar_profesional("333333","Nicolás Díaz","Enfermedades cuello de útero","ndiaz@gmail.com","Miércoles 10.00 a 20.00 horas.", "333333User.png")

print(mi_staff.consultar_profesional("222222"))
print(mi_staff.consultar_profesional("444444"))

mi_staff.listar_profesionales()