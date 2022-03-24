
from flask import Flask, render_template, request
from config import DevelopmentConfig
import json
import os
import smtplib
import getpass
import poplib
import cx_Oracle


# Global
app = Flask(__name__)
app.config.from_object(DevelopmentConfig)


# Path for dataBase connection Oracle
@app.route('/con')
def connection():
    #   getting credentials from the method get_credentials_db   
    cdtls = get_credentials_db()
    print(f"Credentials: {cdtls}")
    #   making connection from impor cx_oracle, and passing the parameters into the dicctionary for conecction
    connection = cx_Oracle.connect(
        f'{cdtls["user"]}/{cdtls["psswrd"]}@{cdtls["host"]}:{cdtls["port"]}/{cdtls["db"]}')
    # making the cursor
    cur = connection.cursor()
    #   probing connection
    cur.execute("SELECT 'Hello, World from Oracle DB!' FROM DUAL")
    col = cur.fetchone()[0]
    cur.close()
    connection.close()
    return col

# Default server path
@app.route('/')
def init():
    return 'Running'


# Path for login view
@app.route('/login')
def index():
    return 'test'


# Send an email
@app.route('/send')
def send():
    # PRUEBA DE ENVIO SMTP CON SERVIDOR LOCAL
    # definimos las variables necesarias para el envío del mensaje (remitente, destinatario, asunto y mensaje -en formato HTML-):
    from_addr = "Desde prueba <correox@redestres.udistrital.edu.co>"
    to_addr = "Hacia prueba <usuario01@redestres.udistrital.edu.co>"

    message = "Hola! Este es un e-mail enviando desde Python"

    # creamos un objeto smtp y realizamos el envío:
    smtp = smtplib.SMTP('localhost', 25)
    smtp.sendmail(from_addr=from_addr, to_addrs=to_addr, msg=message)
    return 'test'

# Path for login into a user
@app.route('/loginUser',methods=['POST'])
def logging_user():
  if request.method == 'POST':
    # From POST method, we request the inputs from the view
    _email = request.form['emailAddress']
    _password = request.form['password']
    try:
      # Query para extrar la contraseña de la BD
      sqlGetPass = f"""SELECT u.password FROM USUARIO u WHERE u.email like '%{_email}%'"""
      # Bring the credentials from JSON to use in DB
      cdtls = get_credentials_db()
      try:
        print("Entra a la conexion")
        # Connection
        connection = cx_Oracle.connect(
          f'{cdtls["user"]}/{cdtls["psswrd"]}@{cdtls["host"]}:{cdtls["port"]}/{cdtls["db"]}')
        cur = connection.cursor()
        # Execute Querys
        cur.execute(sqlGetPass)
        # making commit for connection
        connection.commit()
        # fetch to get password
        fetch = cur.fetchall()[0]
        password = fetch[0]
        # closing cursor
        cur.close()
        # closing connection
        connection.close()
        if password == _password:
          # succesfull message
          message = "Ingresando"
          return render_template('login.html',message = message)
        else:
          # succesfull message
          message = "Datos no coinciden"
          return render_template('login.html',message = message)  
      except cx_Oracle.Error as error:
        print('Error occurred:')
        print(error)
        #   error message for view
        message = "No pudimos hacer su solicitud"
    except:
      message = "Algo salio mal"
      return render_template('register.html',message = message)  
    return render_template('bandeja.html',message = message)  

# Path for register template
@app.route('/register')
def view_register():
  message = ""
  return render_template('register.html', message = message)

# Path to register a user
@app.route('/saveUser',methods=['POST'])
def register_user():
  if request.method == 'POST':
    # From POST method, we request the inputs from the view
    _names = request.form['names']
    _surnames = request.form['surnames']
    _email = request.form['emailAddress']
    _password = request.form['password']
    _rpassword = request.form['RepeatPassword']
    try:
      if (comprobePasswords(_password,_rpassword) == True):
        # Query for insert into usuario, format variable
        sqlInsUser = f"""INSERT INTO USUARIO (names,surnames,email,password)
                          VALUES ('{_names}','{_surnames}','{_email}','{_password}')"""
        # Bring the credentials from JSON to use in DB
        cdtls = get_credentials_db()
        try:
          # Connection
          connection = cx_Oracle.connect(
            f'{cdtls["user"]}/{cdtls["psswrd"]}@{cdtls["host"]}:{cdtls["port"]}/{cdtls["db"]}')
          cur = connection.cursor()
          # Execute Querys
          cur.execute(sqlInsUser)
          # making commit for connection
          connection.commit()
          # closing cursor
          cur.close()
          # closing connection
          connection.close()
          # succesfull message
          message = "Registro completado exitosamente"
          return render_template('login.html',message = message)  
        except cx_Oracle.Error as error:
          print('Error occurred:')
          print(error)
            #   error message for view
          message = "Lo sentimos no pudimos agregar al usuario al sistema"
      else:
        message = "contraseñas no coinciden"
    except:
      message = "Algo salio mal"
      return render_template('register.html',message = message)  
    return render_template('register.html',message = message) 

#  Method that comprobe the passwords
def comprobePasswords(p1,p2):
  if p1 == p2:
    return True
  else:
    return False

# Get credentials
def get_credentials_db():
    # Opening JSON file
    f = open('credentials.json')
    # returns JSON object as a dictionary
    db = json.load(f)
    f.close
    return db

if __name__ == '__main__':
    app.run(debug=True)
