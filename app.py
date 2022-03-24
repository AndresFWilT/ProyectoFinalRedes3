
import email
from flask import Flask, render_template
from config import DevelopmentConfig
import json
import os
import smtplib
import getpass
import poplib


# Global
app = Flask(__name__)
app.config.from_object(DevelopmentConfig)


# Default server path
@app.route('/')
def init():
    return 'Running'


# Path for login
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

if __name__ == '__main__':
    app.run(debug=True)
