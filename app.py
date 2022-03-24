from flask import Flask, render_template
from flask_mail import Mail, Message
from config import DevelopmentConfig
import cx_Oracle
import json
import os

# Global
app = Flask(__name__)
app.config.from_object(DevelopmentConfig)
mail = Mail()

# Default server path
@app.route('/')
def init():
  mail.init_app(app)
  return index()

# Path for login
@app.route('/login')
def index():
  return render_template('login.html')

# Path for register
@app.route('/register')
def view_register():
  return render_template('register.html')

if __name__ == '__main__':
    app.run(debug=True)