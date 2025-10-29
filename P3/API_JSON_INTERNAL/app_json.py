from flask import Flask, jsonify, request, make_response

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    data = {
        'name': 'John Doe',
        'age': 30,
        'email': 'john.doe@example.com',
        'status': 'success'
    }
    return make_response(jsonify({'data': data}), 200)

@app.route('/karyawan', methods=['GET','POST', 'PUT', 'DELETE'])
def karyawan():
    try:
        if request.method == 'GET':
            data = [{
                'name': 'John Doe GET',
                'age': 30,
                'email': 'john.doe@example.com',
                'status': 'success'
            }]
        elif request.method == 'POST':
            data = [{
                'name': 'John Doe POST',
                'age': 30,
                'email': 'john.doe@example.com',
                'status': 'success'
            }]
        elif request.method == 'PUT':
            data = [{
                'name': 'John Doe PUT',
                'age': 30,
                'email': 'john.doe@example.com',
                'status': 'success'
            }]
        else:
            data = [{
                'name': 'John Doe DELETE',
                'age': 30,
                'email': 'john.doe@example.com',
                'status': 'success'
            }]
        return make_response(jsonify({'data': data}), 200)
    except Exception as e:
        return make_response(jsonify({'error': str(e)}), 400)

if __name__ == '__main__':
    app.run(debug=True)