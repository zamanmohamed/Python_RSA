from flask import Flask,jsonify,request,session
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from Crypto.Cipher import PKCS1_OAEP
from flask_cors import CORS
from Crypto import Random
from Crypto.PublicKey import RSA
from flask_session import Session
import ast
import base64
import binascii


app =Flask(__name__)
CORS(app)
app.secret_key = 'zaman'


app.config['SQLALCHEMY_DATABASE_URI']='mysql://root:''@localhost/key_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"

Session = Session(app)
db = SQLAlchemy(app)
ma = Marshmallow(app)

class KeyTable(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    public_key_1 = db.Column(db.Text())
    private_key_1 = db.Column(db.Text())
    public_key_2 = db.Column(db.Text())
    private_key_2 = db.Column(db.Text())
    client_public_key = db.Column(db.Text())

    def __init__(self,public_key_1,private_key_1,public_key_2,private_key_2,client_public_key):
        self.public_key_1 = public_key_1
        self.private_key_1 = private_key_1
        self.public_key_2 = public_key_2
        self.private_key_2 = private_key_2
        self.client_public_key = client_public_key

class KeyTableSchema(ma.Schema):
    class Meta:
        fields=('id','public_key_1','private_key_1','public_key_2','private_key_2','client_public_key')

keyTable_schema = KeyTableSchema()
keyTables_schema = KeyTableSchema(many=True)

private_key = RSA.generate(256*4,Random.new().read)
public_key = private_key.publickey()


@app.route('/',methods=['GET'])
def get_articals():
    if session.get("privatekey1"):
        print("hi")
        key = session.get("privatekey1")
        print(key)
    else:
        print("No")
    return jsonify({"Hello":"Shaman"})

@app.route('/getpublic1',methods=['GET'])
def get_public_1():
    session['publickey1'] = public_key.exportKey().decode()
    session['privatekey1'] = private_key.exportKey().decode()
    pubkey1 = session['publickey1']
    prikey = session['privatekey1']
    if not session.get("publickey1"):
        print("no publickey1")
    return jsonify({"public_key_1":str(pubkey1),"private_key_1":str(prikey)})

@app.route('/postClientPublicEncrypt',methods=['POST','GET'])
def post_client_encrypt_public():
    client_encrypt_public_key = request.json['client_encrypt_public_key']
    private_key_1 = request.json['private_key_1']
    print(client_encrypt_public_key)
    client_decrypt_public_key = RSA.import_key(private_key_1).decrypt(base64.b64decode(client_encrypt_public_key))
    print(client_decrypt_public_key)
    return jsonify({"client_encrypt_public_key":str(client_encrypt_public_key)})
    

@app.route('/get', methods=['GET'])
def get_articles():
    all_kyes = KeyTable.query.all()
    results = keyTables_schema.dump(all_kyes)
    return jsonify(results)

@app.route('/add',methods=['POST'])
def add_key():
    public_key_1 = request.json['public_key_1']
    private_key_1 = request.json['private_key_1']
    public_key_2 = request.json['public_key_2']
    private_key_2 = request.json['private_key_2']
    client_public_key = request.json['client_public_key']

    keys = KeyTable(public_key_1,private_key_1,public_key_2,private_key_2,client_public_key)
    db.session.add(keys)
    db.session.commit()
    return keyTable_schema.jsonify(keys)

if __name__ == "__main__":
    app.run(debug=True)
