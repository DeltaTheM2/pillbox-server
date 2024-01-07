from flask import Flask, request
import firebase_admin
from firebase_admin import credentials, firestore

app = Flask(__name__)

cred = credentials.Certificate('serviceAccountKey.json')
firebase_admin.initialize_app(cred)

db = firestore.client()

@app.route('/update_firestore', methods=['POST'])
def update_firestore():
    # Get data as a plain string
    data_string = request.data.decode('utf-8')

    try:
        # Attempt to parse the string as JSON
        data = json.loads(data_string)
        # Process the data
        # (Add your Firestore updating logic here)
        return jsonify({"status": "success", "message": "Data processed"}), 200
    except json.JSONDecodeError:
        return jsonify({"status": "error", "message": "Invalid JSON format"}), 400


if __name__ == '__main__':
  app.run(debug=True)

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
