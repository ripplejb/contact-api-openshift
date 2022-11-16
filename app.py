import os

from flask import Flask, jsonify, request
import json

app = Flask(__name__)


@app.route('/')
def index():  # put application's code here
    return jsonify({'message': 'Welcome To The Contact API'})


def get_records():
    data_file = os.environ['DATA']
    if not os.path.isfile(data_file):
        save([])
    with open(os.environ['DATA'], 'r') as f:
        data = f.read()
        if not data:
            return []
        return json.loads(data)


def save(records):
    with open(os.environ['DATA'], 'w+') as f:
        f.write(json.dumps(records, indent=2))


@app.route('/contacts', methods=['GET'])
def get_contacts():
    name = request.args.get('name')
    records = get_records()
    if name == 'all':
        jsonify(records)
    for record in records:
        if record['name'] == name:
            return jsonify(record)
    return jsonify({'error': 'data not found'})


@app.route('/contacts', methods=['POST'])
def post_contact():
    record = json.loads(request.data)
    records = get_records()
    records.append(record)
    save(records)
    return jsonify({'message': 'contact saved successfully'})


if __name__ == '__main__':
    app.run()
