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