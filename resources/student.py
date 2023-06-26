from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask import jsonify

from datetime import timedelta

from db import db
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    get_jwt_identity,
    get_jwt,
    jwt_required,
)
from passlib.hash import pbkdf2_sha256

from models import StudentModel
from schemas import StudentSchema
from schemas import loginSchema
from models import Blocklist

blp = Blueprint("Students", "students", description="Operations on stores")

@blp.route("/register")
class StudentRegister(MethodView):
    @blp.arguments(StudentSchema)
    def post(self, student_data):
        if StudentModel.find_by_mis(student_data["mis"]):
            # print(student_data["mis"])
            abort(409, message="A student with that mis already exists.")

        student = StudentModel(**student_data)
        student.password=pbkdf2_sha256.hash(student_data["password"])
        student.save_to_db()
        
        try:
            student.save_to_db()
        except SQLAlchemyError:
            abort(500, message="An error occurred registering the student.")
            
        return student.json()

@blp.route("/login")
class StudentLogin(MethodView):
    @blp.arguments(loginSchema)
    def post(self, student_data):
        user = StudentModel.find_by_mis(student_data["mis"])
        # print(student_data["mis"])
        # print(student_data["password"])
        if user and pbkdf2_sha256.verify(student_data["password"], user.password):
            access_token_duration = timedelta(days=31)
            refresh_token_duration = timedelta(days=93)
            access_token = create_access_token(identity=user.mis, fresh=True, expires_delta=access_token_duration)
            refresh_token = create_refresh_token(identity=user.mis, expires_delta=refresh_token_duration)
            # return {"access_token": access_token, "refresh_token": refresh_token}, 200
            return {"access_token": access_token, "refresh_token": refresh_token, "target": user.target}, 200

        abort(401, message="Invalid credentials.")
    
@blp.route("/refresh")
class TokenRefresh(MethodView):
    @jwt_required(refresh=True)
    def post(self):
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user, fresh=False)
        # Make it clear that when to add the refresh token to the blocklist will depend on the app design
        jti = get_jwt()["jti"]
        revoked_token = Blocklist(jti=jti)
        db.session.add(revoked_token)
        db.session.commit()
        return {"access_token": new_token}, 200

@blp.route("/logout")
class StudentLogout(MethodView):
    @jwt_required()
    def post(self):
        try:
            jti = get_jwt()["jti"]
            # print(jti)
            revoked_token = Blocklist(jti=jti)
            db.session.add(revoked_token)
            db.session.commit()

            
        except:
            # print("error")
            return {'message': 'error occured'}, 401
    
        return {"message": "Successfully logged out"}, 200
    
    
@blp.route("/student/<string:mis>")
class User(MethodView):

    @blp.response(200, StudentSchema)
    # @jwt_required()
    def get(self, mis):
        student = StudentModel.find_by_mis(mis)
        if not student:
            abort(404, message="Student not found.")
        return student.json()

    # @jwt_required(fresh=True)
    def delete(self, mis):
        
        # jwt = get_jwt()
        # if not jwt.get("is_admin"):
        #     abort(401, message="Admin privilege required.")
        
        student = StudentModel.find_by_mis(mis)
        if not student:
            abort(404, message="Student not found.")
        tmis=student.mis
        student.delete_from_db()
        return {"message": "Student with mis deleted.", "mis": tmis}, 200

@blp.route("/all_students")
class ItemList(MethodView):
    @jwt_required()
    @blp.response(200, StudentSchema(many=True))
    def get(self):
        return StudentModel.find_all()