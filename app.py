from flask import Flask, render_template, request
from config import DevelopmentConfig
import json
import os
import smtplib
import getpass
import poplib
import cx_Oracle
import os
from subprocess import call
import getpass
import poplib


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
                "usuario": "usuario01",
                "email": "correox@redes3.udistrital.edu.co",
                "contra": "clave01"
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


# Path for view mail user
@app.route('/mail', methods=['POST'])
def view_mail_main():
    # From POST method, we request the inputs from the view
    if request.method == 'POST':
        user = {
            "email": request.form["email"],
            "usuario": request.form["usuario"]
        }

        try:
            return render_template('mail.html', user=user)
        except:
            message = "algo salio mal"
        return render_template('login.html')



# Path for view visualize sent mails
@app.route('/viewSentMail', methods=['POST'])
def view_sent_mail():
    # From POST method, we request the inputs from the view
    if request.method == 'POST':
        user = {
            "email": request.form["email"],
            "usuario": request.form["usuario"]
        }
        emails = get_emails_with_pop3()
        return render_template('sentMail.html', user=user, emails=emails)
        


# Path for view send mail
@app.route('/viewSendMail', methods=['POST'])
def view_send_mail():
    # From POST method, we request the inputs from the view
    if request.method == 'POST':
        user = {
            "email": request.form["email"],
            "usuario": request.form["usuario"]
        }
        try:
            return render_template('sendMail.html', user=user)
        except Exception as message:
            return render_template('login.html', message=message)

# Path for sending an email


@app.route('/sendMail', methods=['POST'])
def send_mail():
    # From POST method, we request the inputs from the view
    if request.method == 'POST':
        _Or = request.form["emailOrigin"]
        _Des = request.form["emailDestination"]
        _message = request.form["message"]
        user = {
            "email": request.form["emailOrigin"],
            "usuario": request.form["usuario"]
        }
        try:
            # PRUEBA DE ENVIO SMTP CON SERVIDOR LOCAL
            # definimos las variables necesarias para el envío del mensaje (remitente, destinatario, asunto y mensaje -en formato HTML-):

            print("Impresion de valores")
            print(_Or)
            print(_Des)
            print(_message)

            from_addr = f"""Remitente <{_Or}>"""
            to_addr = f"""Destinatario <{_Des}>"""

            print(from_addr)
            print(user)

            # creamos un objeto smtp y realizamos el envío:
            smtp = smtplib.SMTP('localhost', 25)
            smtp.sendmail(from_addr=from_addr, to_addrs=to_addr, msg=_message)
            message = "Correo enviado"
            return render_template('mail.html', user=user, message=message)
        except Exception as message:
            print('Error occurred:')
            print(message)
    return render_template('login.html', message=message, user=user)


def get_emails_with_pop3():
    user = 'usuario01'
    Mailbox = poplib.POP3('localhost', '110')
    Mailbox.user(user)
    Mailbox.pass_('1234')
    numMessages = len(Mailbox.list()[1])
    print(Mailbox.retr(1))
    emails = []
    for i in range(numMessages):
        email_p = []
        for msg in Mailbox.retr(i+1)[1]:
            email_p.append(msg.decode("utf-8").replace('\t', ''))
        emails.append(email_p)
    Mailbox.quit()
    return emails


if __name__ == '__main__':
    get_emails_with_pop3()
    app.run(debug=True)
