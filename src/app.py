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

jackson_family.add_member({
    "first_name": "John",
    "age": 33,
    "lucky_numbers": [7, 13, 22]
})
jackson_family.add_member({
    "first_name": "Jane",
    "age": 35,
    "lucky_numbers": [10, 14, 3]
})
jackson_family.add_member({
    "first_name": "Jimmy",
    "age": 5,
    "lucky_numbers": [1]
})
# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)


##
@app.route('/members', methods=['GET'])
def handle_hello():

    members = jackson_family.get_all_members()
    if members:
        jackson_family.get_all_members()
    else:
            return jsonify({"error": "Members not found"}), 400

    return jsonify(members), 200

@app.route('/member', methods=['POST'])
def add_member():
    member_data = request.get_json()
    if not isinstance(member_data['age'], int):
        return jsonify({"error":"'age'debe contener un valor o ser un entero"}), 400
    if not isinstance(member_data['first_name'], str):
        return jsonify({"error":"'first_name' debe ser una cadena/ no puede quedar vacio"}), 400
    if not isinstance(member_data['lucky_numbers'], list):
        return jsonify({"error":"'lucky_numbers'must be a list"}), 400
    if not all (isinstance(num, int) for num in member_data["lucky_numbers"]):
        return jsonify({"error":"All 'lucky_numbers' must be integers"}), 400

    new_member = jackson_family.add_member(member_data)
    return jsonify(new_member), 200


@app.route('/member/<int:id>', methods=['GET'])
def get_member(id):

    capture_member = jackson_family.get_member(id)
    if capture_member:
        return jsonify(capture_member), 200
    else:
        return jsonify({"error": "no se encontro el miembro"}), 400

@app.route('/member/<int:id>', methods=['DELETE'])
def delete_member(id):
    
    member = jackson_family.get_member(id)
    if member:
        jackson_family.delete_member(id)
    else:
        return jsonify({"error": "member not found"}), 400
    return jsonify({"done": True})
    

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
