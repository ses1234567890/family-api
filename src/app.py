"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# create the jackson family object
jackson_family = FamilyStructure("Jackson")

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/members', methods=['GET'])
def handle_hello():
    members = jackson_family.get_all_members()
    response_body = members
    return jsonify(response_body), 200

@app.route('/member/<int:member_id>', methods=['GET'])
def get_member_by_id(member_id):
    member = jackson_family.get_member(member_id)
    response_body = {
        "hello": "world",
        "family": member
    }
    return jsonify(response_body), 200

@app.route('/member', methods=['POST'])
def create_member():
    body_first_name = request.json.get("first_name")
    body_age = request.json.get("age")
    body_lucky_number = request.json.get("lucky_numbers")
    body_id = request.json.get("id")
    
    jackson_family.add_member({
        "id": body_id if body_id is not None else jackson_family._generateId(),
        "last_name": jackson_family.last_name,
        "first_name": body_first_name,
        "age": body_age,
        "lucky_number": body_lucky_number,
    })

    response_body = {
        "hello": "world",
    }
    return jsonify(response_body), 200

@app.route('/member/<int:member_id>', methods=['DELETE'])
def delete_member(member_id):
    jackson_family.delete_member(member_id)
    response_body = {
        "done": True
    }
    return jsonify(response_body), 200

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
