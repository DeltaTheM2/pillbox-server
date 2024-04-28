from flask import Flask, request, jsonify, send_file
import json
import firebase_admin
from firebase_admin import credentials, firestore, messaging
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


#Get Device ID
String deviceID = ""
doc_ref = db.collection('users').document()
    for user in doc_ref:
        if user.get('device_id') == device_id:
           deviceID = device_id
         
@app.route('/send_pill_notification', methods = ['POST'])
def send_notification(token, title, body):
    # See documentation for more options
    message = messaging.Message(
        notification=messaging.Notification(
            title=title,
            body=body,
        ),
        token=token
    )
    # Send the message
    response = messaging.send(message)
    return response
 
 response = send_notification(deviceID, 'Hello', 'This is a test message')
 print('Successfully sent message:', response)

     #docs = db.collection("pills").stream('uid')
    # notificationList = []
    #for doc in docs:
     #    print(f"{doc.id} => {doc.to_dict()}")
     #    if doc.get('med_history')[0] % 3600 < 1800:
             #call the custom firebase method here
        #     notificationList.append(f"time to take {doc.get('med_name')} in 30 minutes!")


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


  
