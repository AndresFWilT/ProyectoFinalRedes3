from flask import Flask, render_template, request
from config import DevelopmentConfig
import smtplib
import poplib
import poplib


# Global
app = Flask(__name__)
app.config.from_object(DevelopmentConfig)


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
            
            Mailbox = poplib.POP3('localhost', '110')
            Mailbox.user(_user)
            Mailbox.pass_(_password)
            user = {
                "usuario": _user,
                "email": "correox@redes3.udistrital.edu.co",
                "contra": _password
            }
            # succesfull message
            return render_template('mail.html', user=user)
        except Exception as message:
            return render_template('login.html', message='No se pudo autenticar')


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
        print(_Or)
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
    emails = []
    for i in range(numMessages):
        email_p = []
        for msg in Mailbox.retr(i+1)[1]:
            email_p.append(msg.decode("utf-8").replace('\t', ''))
        emails.append(email_p)
    Mailbox.quit()
    return emails


if __name__ == '__main__':
    app.run(debug=True)
