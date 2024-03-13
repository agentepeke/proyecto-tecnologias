import os

from dotenv import load_dotenv
from pymongo import MongoClient
import pymongo

def get_client():
    load_dotenv()
    username = os.getenv('MONGO_USER')
    password = os.getenv('MONGO_PASS')
    cluster = os.getenv('MONGO_CLUSTER')
    try:
        client = MongoClient("mongodb+srv://" + username + ":" + password + "@" + cluster + ".n9gxabn.mongodb.net/?retryWrites=true&w=majority&appName=commentsDB")
        print('Conexión exitosa')
        return client
    except pymongo.errors.ConnectionFailure as error:
        print('Error al conectarse a la base de datos: ', error)
    except pymongo.errors.ServerSelectionTimeoutError as error:
        print('Error al conectarse a la base de datos: ', error)
        
