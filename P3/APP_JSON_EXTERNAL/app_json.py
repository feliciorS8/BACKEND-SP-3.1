from flask import Flask, jsonify
import json

app = Flask(__name__)

#fungsi untuk memuat data dari file json
def load_data():
    with open('Pertemuan_3/API-JSON-EXTERNAL/data.json', 'r') as f:
        return json.load(f)

#endpoint untuk mengambil semua data
@app.route('/', methods=['GET'])
def get_users():
    data = load_data()
    return jsonify(data) 

#endpoint untuk mendapatkan data berdasarkan id
@app.route('/<int:id>', methods=['GET'])
def get_user_by_id(id):
    data = load_data()
    user = next((user for user in data if user['id'] == id), None)
    if user:
        return jsonify(user)
    else:
        return jsonify({'message': 'User not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)