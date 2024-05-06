from flask import Flask, request, jsonify, send_file
import json
import firebase_admin
from firebase_admin import credentials, firestore, messaging
import segno 
from PIL import Image
import time
 
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


@app.route('/fetch_notification/<device_id>', methods=['GET'])
def fetch_notification(device_id):
    current_time = int(time.time())
    pills_ref = db.collection('pills').where('owner', '==', device_id)
    for pill in pills_ref.stream():
        pill_data = pill.to_dict()
        last_taken_time = max(pill_data['med_history']) if pill_data['med_history'] else None
        if last_taken_time:
            next_dose_time = last_taken_time + (pill_data['reminder'] * 3600)
            if next_dose_time - 1800 <= current_time <= next_dose_time:
                return jsonify({
                    'notification_text': f'Time to take your {pill_data["med_name"]} soon.',
                    'time': str(next_dose_time)
                }), 200
    return jsonify({'message': 'No pending notifications'}), 200
@app.route('/get_pill', methods = ['GET'])
def get_pill(uid):
  docs = db.collection("pills").stream('uid')
  docsToReturn = []
  for doc in docs:
    print(f"{doc.id} => {doc.to_dict()}")
    docsToReturn.append(doc.to_dict())

  return docsToReturn

@app.route('/get_pills_for_device/<device_id>', methods=['GET'])
def get_pills_for_device(device_id):
    try:
        # First, find the user associated with this device ID
        user_ref = db.collection('users').where('device_id', '==', device_id).limit(1)
        users = user_ref.stream()
        user_id = None
        for user in users:
            user_data = user.to_dict()
            user_id = user.id  # Assuming there's an id field or use user.id if the document ID is the user ID
            break

        if not user_id:
            return jsonify({'error': 'User not found for the given device ID'}), 404

        # Now, fetch all pills associated with this user ID
        pills_ref = db.collection('pills').where('owner', '==', user_id)
        pills = pills_ref.stream()
        pills_data = [{'med_name': pill.to_dict()['med_name'], 'med_count': pill.to_dict().get('med_count', 0)} for pill in pills]

        return jsonify(pills_data), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

print("data sent")
if __name__ == '__main__':
  app.run(debug=True)


  
