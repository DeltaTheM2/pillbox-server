from flask import Flask, request, jsonify, send_file
import json
import firebase_admin
from firebase_admin import credentials, firestore
import segno 
from PIL import Image
 
app = Flask(__name__)
cred = credentials.Certificate('serviceAccountKey.json')
firebase_admin.initialize_app(cred)

db = firestore.client()
collection = db.collection('pills')


@app.route('/register_device/<device_id>', methods=["GET"])
def register_device(device_id):
   print("image requested")
   png_filename = f"{device_id}.png"
   bmp_filename = f"{device_id}.bmp"
   qrcode = segno.make_qr(device_id)
   qrcode.save(png_filename, scale = 5)
   convert_to_bmp(png_filename, bmp_filename)
   #user_ref = db.collections('devices')
   print("File generated!")
   return send_file(bmp_filename, mimetype='image/bmp')

@app.route('/isRegistered/<device_id>', methods=["GET"])
def isRegistered(device_id):
    doc_ref = db.collection('users').document()
    for user in doc_ref:
        if user.get('device_id') == device_id:
            return user.get('uid')
    return None

def convert_to_bmp(png_filename, bmp_filename):
   with Image.open(png_filename) as img:
      img.save(bmp_filename)
   


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


  
