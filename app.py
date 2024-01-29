from flask import Flask, request, jsonify
import json
import firebase_admin
from firebase_admin import credentials, firestore
import urllib
from urllib import parse

app = Flask(__name__)

cred = credentials.Certificate('serviceAccountKey.json')
firebase_admin.initialize_app(cred)

db = firestore.client()
collection = db.collection('pills')



@app.route('/update_firestore', methods = ['POST'])
def update_firestore():
    print("Request Headers:", request.headers)
    json_data = request.get_json()
    db.collection("pills").document().set(json_data)
    return {"status": "success", "message": "Data updated in Firestore"}, 200
    
@app.route('/update_pill', methods = ['POST'])
def update_pill():
    print("Request Headers:", request.headers)
    json_data = request.get_json()
    db.collection("pills").document("uid").set(json_data)
    return {"status": "success", "message": "Data updated in Firestore"}, 200
    

@app.route('/get_firestore', methods = ['GET'])
def get_firestore():
  docs = db.collection("pills").stream()
  docsToReturn = []
  for doc in docs:
    print(f"{doc.id} => {doc.to_dict()}")
    docsToReturn.append(doc.to_dict())

  return docsToReturn
     
@app.route('/get_pill', methods = ['GET'])
def get_pill(uid):
  docs = db.collection("pills").stream('uid')
  docsToReturn = []
  for doc in docs:
    print(f"{doc.id} => {doc.to_dict()}")
    docsToReturn.append(doc.to_dict())

  return docsToReturn


 
print("data sent")
if __name__ == '__main__':
  app.run(debug=True)


  
