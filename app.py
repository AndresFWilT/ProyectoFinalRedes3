from re import I
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
  return index()

# Path for login view
@app.route('/login')
def index():
  message = ""
  return render_template('login.html', message=message)


# Path for login into a user
@app.route('/loginUser', methods=['POST'])
def logging_user():
  if request.method == 'POST':
    # From POST method, we request the inputs from the view
    _user = request.form['user']
    _password = request.form['password']
    try:
      user = {
        "usuario":"usuario01",
        "email":"correox@redes3.udistrital.edu.co",
        "contra":"clave01"
      }
      if user["usuario"] == _user and user["contra"] == _password:
        print("datos correctos")
        # succesfull message
        message = "Ingresando"
        return render_template('mail.html', user=user)
      else:
        # succesfull message
        message = "Datos no coinciden"
        return render_template('login.html', message=message)
    except Exception as message:
      return render_template('login.html', message=message)

# Path for register template
@app.route('/register')
def view_register():
  message = ""
  return render_template('register.html', message=message)

# Path to register a user
@app.route('/saveUser', methods=['POST'])
def register_user():
  if request.method == 'POST':
    # From POST method, we request the inputs from the view
    _names = request.form['names']
    _surnames = request.form['surnames']
    _email = request.form['emailAddress']
    _password = request.form['password']
    _rpassword = request.form['RepeatPassword']
    try:
      if (comprobePasswords(_password, _rpassword) == True):
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
          return render_template('login.html', message=message)
        except cx_Oracle.Error as error:
          print('Error occurred:')
          print(error)
            #   error message for view
          message = "Lo sentimos no pudimos agregar al usuario al sistema"
      else:
        message = "contraseñas no coinciden"
    except Exception as message:
      return render_template('register.html', message=message)
    return render_template('register.html', message=message)

# Path for view mail user
@app.route('/mail', methods=['POST'])
def view_mail_main():
  # From POST method, we request the inputs from the view
  if request.method == 'POST':
    user = {
      "email":request.form["email"],
      "usuario":request.form["usuario"]
    }
    
    try:
      print(show_emails())
      return render_template('mail.html', user=user)
    except:
      message = "algo salio mal"
    return render_template('login.html')

# Path for view visualize reciebed mails
@app.route('/viewReciebedMail', methods=['POST'])
def view_reciebed_mail():
  # From POST method, we request the inputs from the view
  if request.method == 'POST':
    user = {
      "email":request.form["email"],
      "usuario":request.form["usuario"]
    }
    try:
      return render_template('reciebedMail.html', user=user)
    except:
      message = "algo salio mal"
    return render_template('login.html')

# Path for view visualize sent mails
@app.route('/viewSentMail', methods=['POST'])
def view_sent_mail():
  # From POST method, we request the inputs from the view
  if request.method == 'POST':
    user = {
      "email":request.form["email"],
      "usuario":request.form["usuario"]
    }
    try:
      return render_template('sentMail.html', user=user)
    except:
      message = "algo salio mal"
    return render_template('login.html')

# Path for view send mail
@app.route('/viewSendMail', methods=['POST'])
def view_send_mail():
  # From POST method, we request the inputs from the view
  if request.method == 'POST':
    user = {
      "email":request.form["email"],
      "usuario":request.form["usuario"]
    }
    try:
      print(user)
      return render_template('sendMail.html', user=user)
    except Exception as message:
      return render_template('login.html',message=message)

# Path for sending an email
@app.route('/sendMail', methods=['POST'])
def send_mail():
  # From POST method, we request the inputs from the view
  if request.method == 'POST':
    _Or = request.form["emailOrigin"]
    _Des = request.form["emailDestination"]
    _message = request.form["message"]
    user = {
      "email":request.form["emailOrigin"],
      "usuario":request.form["usuario"]
    }
    try:
      # PRUEBA DE ENVIO SMTP CON SERVIDOR LOCAL
      # definimos las variables necesarias para el envío del mensaje (remitente, destinatario, asunto y mensaje -en formato HTML-):
        
      print("Impresion de valores")
      print(_Or)
      print(_Des)
      print(_message)

      from_addr = f"""Desde prueba <{_Or}>"""
      to_addr = f"""Hacia prueba <{_Des}>"""
      _message = _message + "|||||"

      print(from_addr)
      print(user)

      # creamos un objeto smtp y realizamos el envío:
      smtp = smtplib.SMTP('localhost', 25)
      smtp.sendmail(from_addr=from_addr, to_addrs=to_addr, msg=_message)
      message = "Correo enviado"
      return render_template('mail.html', user=user,message=message)
    except Exception as message:
        print('Error occurred:')
        print(message)
  return render_template('login.html',message=message,user=user)

# Get credentials
def get_credentials_db():
    # Opening JSON file
    f = open('credentials.json')
    # returns JSON object as a dictionary
    db = json.load(f)
    f.close
    return db


def show_emails():   
    print("Mostrando correos") 
    mails = open('/var/spool/mail/usuario01', 'r').read()
    ind_mails = mails.split("|||||")
    return ind_mails
  
if __name__ == '__main__':
    app.run(debug=True)
