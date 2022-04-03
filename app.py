from flask import Flask, render_template, request, session, redirect
from flask_session import Session
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
                "pass": _password
            }
            session["user"] = _user
            session["pass"] = _password
            session["email"] = "correox@redes3.udistrital.edu.co"
            # succesfull message
            return render_template('mail.html', user=user)
        except Exception as message:
            return render_template('login.html', message='No se pudo autenticar')


@app.route('/logout')
def logout():
    session["user"] = None
    session["pass"] = None
    return index()

# Path for view mail user
@app.route('/mail', methods=['GET'])
def view_mail_main():
    if request.method == 'GET':
        if not session.get("user") and session.get("pass"):
            return redirect("/login")
        user = {
            "usuario": session.get("user")
        }
        return render_template('mail.html', user=user)


# Path for view visualize sent mails
@app.route('/viewSentMail', methods=['GET'])
def view_sent_mail():
    # From POST method, we request the inputs from the view
    if request.method == 'GET':
        if not session.get("user") and session.get("pass"):
            return redirect("/login")
        emails = get_emails_with_pop3(session.get("user"),session.get("pass"))
        return render_template('sentMail.html', user=session.get("user"), emails=emails)


# Path for view send mail
@app.route('/viewSendMail', methods=['GET'])
def view_send_mail():
    # From POST method, we request the inputs from the view
    if request.method == 'GET':
        if not session.get("user") and session.get("pass"):
            return redirect("/login")

        return render_template('sendMail.html', email=session.get("email"))


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
            "usuario": session.get("user"),
            "pass": session.get("pass")
        }
        try:
            # ENVIO SMTP CON SERVIDOR LOCAL
            # definimos las variables necesarias para el envío del mensaje (remitente, destinatario, asunto y mensaje -en formato HTML-):

            from_addr = f"""Remitente <{_Or}>"""
            to_addr = f"""Destinatario <{_Des}>"""

            # creamos un objeto smtp y realizamos el envío:
            smtp = smtplib.SMTP('localhost', 25)
            smtp.sendmail(from_addr=from_addr, to_addrs=to_addr, msg=_message)
            message = "Correo enviado"
            return render_template('mail.html', user=user, message=message)
        except Exception as message:
            print('Error occurred:')
            print(message)
    message = "Error"
    return render_template('login.html', message=message, user=user)


def get_emails_with_pop3(user,passw):
    Mailbox = poplib.POP3('localhost', '110')
    Mailbox.user(user)
    Mailbox.pass_(passw)
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
