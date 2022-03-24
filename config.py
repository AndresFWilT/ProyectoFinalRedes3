import os

class Config(object):
    SECRET_KEY = 'my_secret_key'
    ## Config for mail server
    MAIL_SERVER = "smtp_gmail.com"
    MAIL_PORT = 587
    # Mail configuration
    MAIL_USERNAME = 'asd'
    MAIL_PASSWORD = 'asd'
    MAIL_USE_TLS = True

class DevelopmentConfig(Config):
    Debug = True