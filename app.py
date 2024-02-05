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
    input_json = request.get_json(force=True)
    print('data from client:', input_json)
    #print("Request Headers:", request.headers)
    #json_data = request.get_json()
    db.collection("pills").document().set(input_json)
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
       
  # collection_name = request.args.get('pills')
  # document_name = request.args.get('uid')

  # if not collection_name:
  #   return "Missing collection or document name ", 400

  # try:
  #   doc_ref = db.collection(collection_name)
  #   doc = doc_ref.get()
  #   if doc.exists:
  #     return doc.to_dic(), 200
  #   else:
  #     return "Document not found", 404

  # except Exception as e:
  #   return f"an error occured: {str(e)}", 500


firebasedata = {
      'med_count': 0,
      'med_history': "2023-1-1T07:22Z",
      'med_name': "somethingnewnew",
      'reminder' : 0
      }
 
print("data sent")
if __name__ == '__main__':
  app.run(debug=True)


  
