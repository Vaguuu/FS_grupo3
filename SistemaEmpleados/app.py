from flask import Flask
from flask import render_template,request,redirect,send_from_directory,url_for,flash 
from flaskext.mysql import MySQL
from datetime import datetime
import os

app = Flask(__name__)
app.secret_key="ClaveSecreta"
mysql = MySQL()
app.config['MYSQL_DATABASE_HOST']='localhost'
app.config['MYSQL_DATABASE_USER']='root'
app.config['MYSQL_DATABASE_PASSWORD']=''
app.config['MYSQL_DATABASE_BD']='sistema'
mysql.init_app(app)
CARPETA= os.path.join('uploads')
app.config['CARPETA']=CARPETA

@app.route('/fotoperfil/<nombreFoto>')
def fotoperfil(nombreFoto):
    return send_from_directory(app.config['CARPETA'], nombreFoto)

@app.route('/')
def index():
    conn = mysql.connect()
    cursor = conn.cursor()
    sql = "SELECT * FROM `sistema`.`empleados`;"
    cursor.execute(sql)
    empleados = cursor.fetchall()
    conn.commit()
    return render_template('empleados/index.html',empleados=empleados)

@app.route('/create')
def create():
    return render_template('empleados/create.html')

@app.route('/store', methods=['POST'])
def storage():
    _mn=request.form['txtMN']
    _nombre=request.form['txtNombre']
    _especialidad=request.form['txtEspecialidad']
    _correo=request.form['txtCorreo']
    _horarios=request.form['txtHorarios']
    _foto=request.files['txtFoto']
    if _mn == '' or _nombre == '' or _especialidad == '' or _correo == '' or _foto.filename == '' or _horarios =='':
        flash('Por favor, complete los datos de todos los campos.')
        return redirect(url_for('create'))
    if _foto.filename != '':
        nuevoNombreFoto = _mn + _foto.filename
        _foto.save("uploads/"+nuevoNombreFoto)
    sql = "INSERT INTO `sistema`.`empleados` (`mn`, `nombre`, `especialidad`, `correo`, `horarios`, `foto`) VALUES (%s, %s, %s, %s, %s, %s);"
    datos=(_mn,_nombre,_especialidad,_correo,_horarios,nuevoNombreFoto)
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute(sql,datos)
    conn.commit()
    return redirect('/')

@app.route('/delete/<path:mn>')
def delete(mn):
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("SELECT foto FROM `sistema`.`empleados` WHERE mn=%s",mn)
    fila= cursor.fetchall()
    os.remove(os.path.join(app.config['CARPETA'], fila[0][0]))
    cursor.execute("DELETE FROM `sistema`.`empleados` WHERE mn=%s", (mn))
    conn.commit()
    return redirect('/')

@app.route('/edit/<path:mn>')
def edit(mn):
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM `sistema`.`empleados` WHERE mn=%s", (mn))
    empleados=cursor.fetchall()
    conn.commit()
    return render_template('empleados/edit.html', empleados=empleados)

@app.route('/update', methods=['POST'])
def update():
    mn = "SELECT mn FROM `sistema`.`empleados` WHERE mn=%s, ({{empleados[0]}})"
    _especialidad=request.form['txtEspecialidad']
    _correo=request.form['txtCorreo']
    _horarios=request.form['txtHorarios']
    _foto=request.files['txtFoto']
    sql = "UPDATE `sistema`.`empleados` SET `especialidad`=%s, `correo`=%s, `horarios`=%s WHERE mn=%s;"
    datos=(_especialidad,_correo,_horarios,mn)
    conn = mysql.connect()
    cursor = conn.cursor()
    if _foto.filename!='':
        nuevoNombreFoto=mn+_foto.filename
        _foto.save("SistemaEmpleados/uploads/"+nuevoNombreFoto)
        cursor.execute("SELECT foto FROM `sistema`.`empleados` WHERE mn=%s", mn)
        fila= cursor.fetchall()
        os.remove(os.path.join(app.config['CARPETA'], fila[0][0]))
        cursor.execute("UPDATE `sistema`.`empleados` SET foto=%s WHERE mn=%s;", (nuevoNombreFoto, mn))
        conn.commit()
    cursor.execute(sql,datos)
    conn.commit()
    return redirect('/')

if __name__=='__main__':
    app.run(debug=True)