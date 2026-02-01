#!/usr/bin/env python3

from flask import request, session
from flask_restful import Resource
from config import app, db, api
from models import User, UserSchema

# -------------------------
# SIGNUP
# -------------------------
class Signup(Resource):
    def post(self):
        data = request.get_json()

        user = User(username=data['username'])
        user.password_hash = data['password']

        db.session.add(user)
        db.session.commit()

        session['user_id'] = user.id

        return UserSchema().dump(user), 201


# -------------------------
# LOGIN
# -------------------------
class Login(Resource):
    def post(self):
        data = request.get_json()

        user = User.query.filter_by(username=data['username']).first()

        if user and user.authenticate(data['password']):
            session['user_id'] = user.id
            return UserSchema().dump(user), 200

        return {'error': 'Unauthorized'}, 401


# -------------------------
# LOGOUT
# -------------------------
class Logout(Resource):
    def delete(self):
        session['user_id'] = None
        return {}, 204


# -------------------------
# CHECK SESSION
# -------------------------
class CheckSession(Resource):
    def get(self):
        user_id = session.get('user_id')

        if user_id:
            user = User.query.get(user_id)
            return UserSchema().dump(user), 200

        return {}, 204


# -------------------------
# CLEAR (already provided)
# -------------------------
class ClearSession(Resource):
    def delete(self):
        session['page_views'] = None
        session['user_id'] = None
        return {}, 204


# -------------------------
# ROUTES
# -------------------------
api.add_resource(Signup, '/signup')
api.add_resource(Login, '/login')
api.add_resource(Logout, '/logout')
api.add_resource(CheckSession, '/check_session')
api.add_resource(ClearSession, '/clear')

if __name__ == '__main__':
    app.run(port=5555, debug=True)
