import os

class Development(object):
    JSON_AS_ASCII = False
    DEBUG = True
    PORT = 5000
    HOST = "192.168.11.65"
    SECRET_KEY = "pf9Wkove4IKEAXvy-cQkeDPhv9Cb3Ag-wyJILbq_dFw"
    SECURITY_PASSWORD_SALT = "146585145368132386173505678016728509634"
    DATABASE = {
        'name': 'example.db',
        'engine': 'peewee.SqliteDatabase',
    }
    GMAIL = {
        "from_address": "m.partner.official@gmail.com",
        "password": "dfxqywezgizwmclc",
    }

    JINJA_VARIABLE = {
        "system_name": "ADOPT -AI面接ツール-"
    }
    LINE = {
        "error_notify_token": "4zWNM6lR3GlaobbmvNo8RAuClGp8Xe8wzJvwB8ZnVdV"
    }

class Production(Development):
    DEBUG = False
    PORT = 80
    HOST = "0.0.0.0"
    MYSQL_ADDRESS = os.getenv("MYSQL_ADDRESS")
    MYSQL_USER = os.getenv("MYSQL_USER")
    MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")
    MYSQL_PORT = os.getenv("MYSQL_PORT")
    MYSQL_DATABASE = os.getenv("MYSQL_DATABASE")
