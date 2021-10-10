import os
import bcrypt
import datetime
from flask import Flask, request, jsonify, make_response
from utils import jwt_utils

import mutant_service

app = Flask(__name__)

@app.route("/", methods=['GET'])
def welcome():
    return make_response("Hello from %s, welcome to Mutant DNA Finder... :)" % os.environ['HOSTNAME'], 200)

@app.route("/api/login", methods=['POST'])
def login():
    content = request.json
    password = content["password"].encode('utf8')
    if bcrypt.checkpw(password, os.environ['MAGNETO_PASSWORD'].encode('utf8')):
        return jsonify({
            "token": jwt_utils.generate_jwt_token("Magneto")
        })
    else:
        return make_response("Your credentials are invalid, sorry!", 401)

@app.route("/api/mutant", methods=['POST'])
def dna_test():
    jwt_utils.validate_jwt_token(request)

    content = request.json
    dna_sequence = content["dna"]
    dna_size = len(dna_sequence)
    is_mutant_response = mutant_service.process_human_dna(dna_sequence, dna_size)
    if is_mutant_response:
        return make_response("Mutant DNA.", 200)
    else:
        return make_response("Human DNA.", 403)

@app.route("/api/stats", methods=['GET'])
def stats():
    jwt_utils.validate_jwt_token(request)

    return jsonify(mutant_service.get_human_dna_statistics())

@app.errorhandler(jwt_utils.AuthenticationError)
def handle_exception(error):
    return jsonify({ "error": error.description }), error.code
