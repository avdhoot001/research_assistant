from flask import request, jsonify, current_app
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from .models import User
from app import create_app

app = create_app()

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    hashed_password = generate_password_hash(data['password'], method='sha256')
    
    new_user = User(
        name=data['name'],
        email=data['email'],
        password=hashed_password,
        gender=data.get('gender'),
        age=data.get('age'),
        field_of_education=data.get('field_of_education'),
        interests=data.get('interests')
    )
    
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'User registered successfully!'}), 201

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(email=data['email']).first()

    if not user or not check_password_hash(user.password, data['password']):
        return jsonify({'message': 'Invalid email or password!'}), 401

    return jsonify({'message': 'Logged in successfully!'}), 200
