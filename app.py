
from flask import Flask, render_template
from flask_mail import Mail, Message
from config import DevelopmentConfig
import cx_Oracle
import json
import os

import smtplib


# Global
app = Flask(__name__)
app.config.from_object(DevelopmentConfig)
mail = Mail()

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

# Path for login
@app.route('/login')
def index():
  return 'test'

if __name__ == '__main__':
    app.run(debug=True)

