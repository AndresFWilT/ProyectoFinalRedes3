from flask import Flask, render_template, request
from flask_mail import Mail, Message
from config import DevelopmentConfig
import cx_Oracle
import json

import smtplib

# Global
app = Flask(__name__)
app.config.from_object(DevelopmentConfig)
mail = Mail()

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
  #PRUEBA DE ENVIO SMTP CON SERVIDOR GMAIL
  #correo de destino
  correo_d = 'Destino_prueba@yopmail.com'

  #correo de origen
  correo_o = 'correo.base.de.datos.uno@gmail.com'

  #definimos parametros del mensaje 
  mensaje = ('Buen dia, correo enviado usando SMTP ')
  server = smtplib.SMTP('smtp.gmail.com', 587)
  server.ehlo()
  server.starttls()

  msg = 'Subject: {}\n\n{}'.format("Prueba Redes 3", mensaje)  

  #ingreso al correo de gmail
  server.login('correo.base.de.datos.uno@gmail.com', 'basededatosunoprueba123')  
  
  #se envia el correo
  server.sendmail(correo_o, correo_d, msg) 
  server.quit()
 
  '''
  #PRUEBA DE ENVIO SMTP CON SERVIDOR LOCAL
  #definimos las variables necesarias para el envío del mensaje (remitente, destinatario, asunto y mensaje -en formato HTML-):
  remitente = "Desde prueba <correo.base.de.datos.uno@gmail.com>" 
  destinatario = "Hacia prueba <luisocampo.o.g@gmail.com>" 
  asunto = "E-mal HTML enviado desde Python" 
  mensaje = """Hola!<br/> <br/> 
  Este es un <b>e-mail</b> enviando desde <b>Python</b> 
  """
  
  #generamos el e-mail con todos los datos definidos anteriormente:
  email = """From: %s 
  To: %s 
  MIME-Version: 1.0 
  Content-type: text/html 
  Subject: %s 
  %s
  """ % (remitente, destinatario, asunto, mensaje)
  
  # creamos un objeto smtp y realizamos el envío:
  smtp = smtplib.SMTP('localhost')
  smtp.sendmail(remitente, destinatario, email)
  '''

  mail.init_app(app)
  return index()

# Path for login view
@app.route('/login')
def index():
  message = ""
  return render_template('login.html',message=message)

# Path for login into a user
@app.route('/loginUser',methods=['POST'])
def logging_user():
  if request.method == 'POST':
    # From POST method, we request the inputs from the view
    _email = request.form['emailAddress']
    _password = request.form['password']
    try:
      # Query for the password for the DB
      sqlGetPass = f"""SELECT u.password FROM USUARIO u WHERE u.email like '%{_email}%'"""
      # Query for bring the data of the user
      sqlGetUser = f"""SELECT * FROM USUARIO u WHERE u.email like '%{_email}%'"""
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
        # executing Query for user
        cur.execute(sqlGetUser)
        user = cur.fetchall()
        # closing cursor
        cur.close()
        # closing connection
        connection.close()
        if password == _password:
          # succesfull message
          message = "Ingresando"
          return render_template('mail.html',user = user)
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
      message = "No encontramos tu cuenta"
      return render_template('register.html',message = message)  
    return render_template('login.html',message = message)  

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

# Path for view mail user
@app.route('/mail',methods=['POST'])
def view_mail_main():
  # From POST method, we request the inputs from the view
  if request.method == 'POST':
    _email = request.form["email"]
    try:
      # Query for bring the data of the user
      sqlGetUser = f"""SELECT * FROM USUARIO u WHERE u.email like '%{_email}%'"""
      # Bring the credentials from JSON to use in DB
      cdtls = get_credentials_db()
      try:
        print("Entra a la conexion")
        # Connection
        connection = cx_Oracle.connect(
          f'{cdtls["user"]}/{cdtls["psswrd"]}@{cdtls["host"]}:{cdtls["port"]}/{cdtls["db"]}')
        cur = connection.cursor()
        # executing Query for user
        cur.execute(sqlGetUser)
        user = cur.fetchall()
        # closing cursor
        cur.close()
        # closing connection
        connection.close()
        return render_template('mail.html',user = user)  
      except cx_Oracle.Error as error:
        print('Error occurred:')
        print(error)
        #   error message for view
        message = "No pudimos hacer su solicitud"
    except:
      message = "algo salio mal"
    return render_template('login.html')

# Path for view send mail
@app.route('/viewSendMail',methods=['POST'])
def view_send_mail():
  # From POST method, we request the inputs from the view
  if request.method == 'POST':
    _email = request.form["email"]
    try:
      # Query for bring the data of the user
      sqlGetUser = f"""SELECT * FROM USUARIO u WHERE u.email like '%{_email}%'"""
      # Bring the credentials from JSON to use in DB
      cdtls = get_credentials_db()
      try:
        print("Entra a la conexion")
        # Connection
        connection = cx_Oracle.connect(
          f'{cdtls["user"]}/{cdtls["psswrd"]}@{cdtls["host"]}:{cdtls["port"]}/{cdtls["db"]}')
        cur = connection.cursor()
        # executing Query for user
        cur.execute(sqlGetUser)
        user = cur.fetchall()
        # closing cursor
        cur.close()
        # closing connection
        connection.close()
        return render_template('sendMail.html',user = user)  
      except cx_Oracle.Error as error:
        print('Error occurred:')
        print(error)
        #   error message for view
        message = "No pudimos hacer su solicitud"
    except:
      message = "algo salio mal"
    return render_template('sendMail.html', email = _email)

# Path for sending an email
@app.route('/sendMail',methods=['POST'])
def send_mail():
  # From POST method, we request the inputs from the view
  if request.method == 'POST':
    _email = request.form["emailAddress"]
    _emailDes = request.form["emailDes"]
    _message = request.form["texto"]
    try:
      # Query for bring the data of the user
      sqlGetUser = f"""SELECT * FROM USUARIO u WHERE u.email like '%{_email}%'"""
      # Bring the credentials from JSON to use in DB
      cdtls = get_credentials_db()
      try:
        print("Entra a la conexion")
        # Connection
        connection = cx_Oracle.connect(
          f'{cdtls["user"]}/{cdtls["psswrd"]}@{cdtls["host"]}:{cdtls["port"]}/{cdtls["db"]}')
        cur = connection.cursor()
        # executing Query for user
        cur.execute(sqlGetUser)
        user = cur.fetchall()
        # closing cursor
        cur.close()
        # closing connection
        connection.close()
        ## Logic to send mail

        return render_template('mail.html', user = user)
      except cx_Oracle.Error as error:
        print('Error occurred:')
        print(error)
        #   error message for view
        message = "No pudimos hacer su solicitud"
    except:
      message = "algo salio mal"
    return render_template('login.html')

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