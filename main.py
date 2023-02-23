from os import getenv
from secrets import token_bytes

from bson import CodecOptions, STANDARD
from flask_migrate import Migrate
from flask_mongoengine import MongoEngine
from flask import Flask
from flask_pymongo import PyMongo
#from Models.Battle import Battle
import pymongo
from pymongo.encryption import ClientEncryption
from pymongo.encryption_options import AutoEncryptionOpts

key_bytes = token_bytes(96)
kms_providers = {"local": {"key": key_bytes}}
csfle_opts = AutoEncryptionOpts(
   kms_providers=kms_providers, key_vault_namespace="csfle_demo.__keystore"
)

client = pymongo.MongoClient(
    'mongodb+srv://server:a37e0RwBBKL2QKzp@cluster0.dkt5fwz.mongodb.net/?retryWrites=true&w=majority', auto_encryption_opts=csfle_opts)
db = client.get_database('herocode')

client_encryption = ClientEncryption(
      kms_providers,
      "csfle_demo.__keystore",
      client,
      CodecOptions(uuid_representation=STANDARD),
   )

key_id = client_encryption.create_data_key("local", key_alt_names=["example"])
print("Client encryption key: {}".format(key_id))

read_only_client = pymongo.MongoClient(
    'mongodb+srv://public:bALBnMNRVyiGb21W@cluster0.dkt5fwz.mongodb.net/?retryWrites=true&w=majority')
read_only_db = read_only_client.get_database('herocode')



#w92WdYDt0CkX6imY
#bALBnMNRVyiGb21W - public
#a37e0RwBBKL2QKzp - server

def main():
    global db
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "adiokjai3kiokdaioskdio32"
    app.config["MONGODB_HOST"] = "mongodb+srv://server:a37e0RwBBKL2QKzp@cluster0.dkt5fwz.mongodb.net/?retryWrites=true&w=majority"
    #app.config["MONGO_URI"] = "mongodb+srv://server:a37e0RwBBKL2QKzp@cluster0.dkt5fwz.mongodb.net/?retryWrites=true&w=majority"
    app.config['MONGODB_SETTINGS'] = {
        'db': 'herocode',
        'host': 'mongodb+srv://server:a37e0RwBBKL2QKzp@cluster0.dkt5fwz.mongodb.net/?retryWrites=true&w=majority'
    }
    #db.init_app(app)
    #db = client.herocode

    #mongo_client = PyMongo(app)
    #db = mongo_client.db
    #print(db.get_collection('Enemy').count_documents({}))

    from Routes.battle import battle
    app.register_blueprint(battle, url_prefix='/battle')
    from Routes.read_only import read_only
    app.register_blueprint(read_only, url_prefix='/get')

    host = getenv('host')
    port = getenv('port')
    debug = getenv('debug') == '1'
    app.run(host=host, port=port, debug=debug)


if __name__ == '__main__':
    main()
