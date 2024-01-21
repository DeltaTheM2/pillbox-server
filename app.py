from crypt import methods
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
    json_data = request.get_json()
    # if type(data) != dict:
    #    encoded_data = urllib.parse.urlencode(data)
    #    db.collection("pills").document().set(encoded_data)
    # else:
    db.collection("pills").document().set(json_data)
    # Access the 'pills' collection and update/create a document with the UID
    #db.collection('pills').add(data)

    return {"status": "success", "message": "Data updated in Firestore"}, 200
    


@app.route('/get_firestore', methods = ['GET'])
def get_firestore():
  collection_name = request.args.get('pills')
  document_name = request.args.get('uid')

  if not collection_name or not document_name:
    return "Missing collection or document name ", 400

  try:
    doc_ref = db.collection(collection_name).document(document_name)
    doc = doc_ref.get()
    if doc.exists:
      return doc.to_dic(), 200
    else:
      return "Document not found", 404

  except Exception as e:
    return f"an error occured: {str(e)}", 500
firebasedata = {
      'med_count': 0,
      'med_history': "2023-1-1T07:22Z",
      'med_name': "somethingnewnew",
      'reminder' : 0
      }
 
print("data sent")
if __name__ == '__main__':
  app.run(debug=True)


  
