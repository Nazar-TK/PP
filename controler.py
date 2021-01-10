from flask import json, Response, request, jsonify
from flask_restful import Resource, Api
from models import *
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.ext.declarative import DeclarativeMeta
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import session

class AlchemyEncoder(json.JSONEncoder):

    def default(self, obj):
        if isinstance(obj.__class__, DeclarativeMeta):
            # an SQLAlchemy class
            fields = {}
            for field in [x for x in dir(obj) if not x.startswith('_') and x != 'metadata']:
                data = obj.__getattribute__(field)
                try:
                    json.dumps(data) # this will fail on non-encodable values, like other classes
                    fields[field] = data
                except TypeError:
                    fields[field] = None
            # a json-encodable dict
            return fields

        return json.JSONEncoder.default(self, obj)


class AddShow(Resource):
    @jwt_required
    def post(self):
        data = request.json
        user_id = get_jwt_identity()
        checkuser = session.query(User).filter(User.id == user_id).one()
        if checkuser.admin != 1:
            return Response(
                response=json.dumps({"message": "Not allowed for users"}),
                status=400,
                mimetype="application/json"
            )
        try:
            show = Show(data["name"], data["show_type"], data["description"], data["time"], data["place"])
            session.add(show)
            session.flush()
            session.commit()
            return Response(
                response=json.dumps({"message": "Show added"}),
                status=200,
                mimetype="application/json"
            )
        except:
            return Response(
                response=json.dumps({"message": "Invalid input"}),
                status=405,
                mimetype="application/json"
            )


class GetAllShows(Resource):
    @jwt_required
    def get(self):
        shows = session.query(Show).all()
        if shows:
            return Response(
                response=json.dumps(shows, cls=AlchemyEncoder),
                status=201,
                mimetype="application/json"
            )
        return Response(
                response=json.dumps({"message": "Not found"}),
                status=404,
                mimetype="application/json"
            )


class SignUpUser(Resource):
    def post(self):
        data = request.json
        try:
            user = User(data["name"], data["password"], data["phone"], data["mail"], data["admin"])
            checkuser = session.query(User).filter(User.mail == user.mail).all()
            if checkuser:
                return Response(
                    response=json.dumps({"message": "user with such email already exist"}),
                    status=405,
                    mimetype="application/json"
                )
            user.password = generate_password_hash(data["password"])
            session.add(user)
            session.flush()
            session.commit()
            return Response(
                response=json.dumps({"message": "User registered"}),
                status=200,
                mimetype="application/json"
            )
        except:
            return Response(
                response=json.dumps({"message": "invalid input"}),
                status=405,
                mimetype="application/json"
            )


class Login(Resource):
    def post(self):
        data = request.json
        user = User.authenticate(**data)
        token = user.get_token()
        return jsonify({'access_token': token})


class GetOwnUser(Resource):
    @jwt_required
    def get(self):
        id = get_jwt_identity()
        user = session.query(User).get(id)
        if user:
            return Response(
                response=json.dumps(user, cls=AlchemyEncoder),
                status=201,
                mimetype="application/json"
            )
        return Response(
            response=json.dumps({"message": "Not found"}),
            status=404,
            mimetype="application/json"
        )


class GetAllUsers(Resource):
    @jwt_required
    def get(self):
        user_id = get_jwt_identity()
        checkuser = session.query(User).filter(User.id == user_id).one()
        if checkuser.admin != 1:
            return Response(
                response=json.dumps({"message": "Not allowed for users"}),
                status=400,
                mimetype="application/json"
            )
        users = session.query(User).all()
        if users:
            return Response(
                response=json.dumps(users, cls=AlchemyEncoder),
                status=201,
                mimetype="application/json"
            )
        return Response(
            response=json.dumps({"message": "Not found"}),
            status=404,
            mimetype="application/json"
        )


class DeleteUser(Resource):
    @jwt_required
    def delete(self, id):
        try:
            user_id = get_jwt_identity()
            checkuser = session.query(User).filter(User.id == user_id).one()
            if checkuser.admin != 1:
                return Response(
                    response=json.dumps({"message": "Not allowed for users"}),
                    status=400,
                    mimetype="application/json"
                )
            tickets = session.query(Ticket).filter(Ticket.user_id == id).all()
            for ticket in tickets:
                ticket.is_avaliable = 1
                ticket.user_id = None
            session.commit()
            user = session.query(User).filter(User.id == id).delete()
            session.commit()
            if user:
                return Response(
                    response=json.dumps({"message": "Success"}),
                    status=200,
                    mimetype="application/json"
                )
        except Exception as e:
            return Response(
                response=json.dumps({"message": "Not found"}),
                status=400,
                mimetype="application/json"
            )


class DeleteMyself(Resource):
    @jwt_required
    def delete(self):
        user_id = get_jwt_identity()
        checkuser = session.query(User).filter(User.id == user_id).one()
        if checkuser.admin == 1:
            return Response(
                response=json.dumps({"message": "Not allowed for admin"}),
                status=400,
                mimetype="application/json"
            )
        tickets = session.query(Ticket).filter(Ticket.user_id == user_id).all()
        for ticket in tickets:
            ticket.is_avaliable = 1
            ticket.user_id = None
        session.commit()
        user = session.query(User).filter(User.id == id).delete()
        session.commit()
        if user:
            return Response(
                response=json.dumps({"message": "Success"}),
                status=200,
                mimetype="application/json"
            )
        return Response(
                response=json.dumps({"message": "Not found"}),
                status=400,
                mimetype="application/json"
            )

class GetUser(Resource):
    @jwt_required
    def get(self, id):
        user_id = get_jwt_identity()
        checkuser = session.query(User).filter(User.id == user_id).one()
        if checkuser.admin != 1:
            return Response(
                response=json.dumps({"message": "Not allowed for users"}),
                status=400,
                mimetype="application/json"
            )
        user = session.query(User).get(id)
        if user:
            return Response(
                response=json.dumps(user, cls=AlchemyEncoder),
                status=201,
                mimetype="application/json"
            )
        return Response(
                response=json.dumps({"message": "Not found"}),
                status=404,
                mimetype="application/json"
            )


class UpdateUser(Resource):
    @jwt_required
    def put(self):
        data = request.json
        user_id = get_jwt_identity()
        try:
            user = session.query(User).get(user_id)
            if not user:
                return Response(
                    response=json.dumps({"message": "invalid id"}),
                    status=400,
                    mimetype="application/json"
                )
            if "password" in data:
                user.password = generate_password_hash(data['password'])
            if "name" in data:
                user.name = data["name"]
            if "phone" in data:
                user.phone = data["phone"]
            session.commit()
            return Response(
                response=json.dumps({"message": "Success"}),
                status=200,
                mimetype="application/json"
            )
        except Exception as e:
            return Response(
                response=json.dumps({"message": "Invalid input"}),
                status=405,
                mimetype="application/json"
            )


class AddTicket(Resource):
    @jwt_required
    def post(self, sid):
        user_id = get_jwt_identity()
        checkuser = session.query(User).filter(User.id == user_id).one()
        if checkuser.admin != 1:
            return Response(
                response=json.dumps({"message": "Not allowed for users"}),
                status=400,
                mimetype="application/json"
            )
        data = request.json
        try:
            ticket = Ticket(1, data["clas"], sid, None)

            session.add(ticket)
            session.flush()
            session.commit()

            return Response(
                response=json.dumps({"message": "Success"}),
                status=200,
                mimetype="application/json"
            )
        except:
            return Response(
                response=json.dumps({"message": "Invalid input"}),
                status=405,
                mimetype="application/json"
            )


class BuyTicket(Resource):
    @jwt_required
    def put(self, tid):
        user_id = get_jwt_identity()
        checkuser = session.query(User).filter(User.id == user_id).one()
        if checkuser.admin == 1:
            return Response(
                response=json.dumps({"message": "Not allowed for admins"}),
                status=400,
                mimetype="application/json"
            )
        try:
            ticket = session.query(Ticket).get(tid)
            if not ticket.is_avaliable:
                return Response(
                    response=json.dumps({"message": "This item is already bought or reserved"}),
                    status=405,
                    mimetype="application/json"
                )
            ticket.is_avaliable = 0
            ticket.user_id = user_id

            session.commit()
            return Response(
                response=json.dumps({"message": "User registered"}),
                status=200,
                mimetype="application/json"
            )
        except:

            return Response(
                response=json.dumps({"message": "invalid input"}),
                status=404,
                mimetype="application/json"
            )


class ReserveTicket(Resource):
    @jwt_required
    def put(self, tid):
        user_id = get_jwt_identity()
        checkuser = session.query(User).filter(User.id == user_id).one()
        if checkuser.admin == 1:
            return Response(
                response=json.dumps({"message": "Not allowed for admins"}),
                status=400,
                mimetype="application/json"
            )
        try:
            ticket = session.query(Ticket).get(tid)
            if not ticket.is_avaliable:
                return Response(
                    response=json.dumps({"message": "This item is already bought or reserved"}),
                    status=405,
                    mimetype="application/json"
                )
            ticket.is_avaliable = 0
            ticket.user_id = user_id

            session.commit()
            return Response(
                response=json.dumps({"message": "Success"}),
                status=200,
                mimetype="application/json"
            )
        except Exception as e:
            return Response(
                response=json.dumps({"message": "This item is already bought or reserved"}),
                status=405,
                mimetype="application/json"
            )


class DeleteReservationTicket(Resource):
    @jwt_required
    def put(self, tid):
        try:
            user_id = get_jwt_identity()
            ticket = session.query(Ticket).get(tid)
            if ticket.user_id != user_id:
                return Response(
                    response=json.dumps({"message": "Not allowed"}),
                    status=400,
                    mimetype="application/json"
                )
            ticket.is_avaliable = 1
            ticket.user_id = None

            session.commit()
            return Response(
                response=json.dumps({"message": "Success"}),
                status=200,
                mimetype="application/json"
            )
        except Exception as e:
            return Response(
                response=json.dumps({"message": "Invalid input"}),
                status=405,
                mimetype="application/json"
            )


class GetTicket(Resource):
    @jwt_required
    def get(self, id):
        try:
            user_id = get_jwt_identity()
            checkuser = session.query(User).filter(User.id == user_id).one()
            if checkuser.admin != 1:
                return Response(
                    response=json.dumps({"message": "Not allowed for user"}),
                    status=400,
                    mimetype="application/json"
                )
            ticket = session.query(Ticket).get(id)
            if ticket:
                return Response(
                    response=json.dumps(ticket, cls=AlchemyEncoder),
                    status=201,
                    mimetype="application/json"
                )
            return Response(
                    response=json.dumps({"message": "Not found"}),
                    status=404,
                    mimetype="application/json"
                )
        except Exception as e:
            return Response(
                response=json.dumps({"message": "Invalid input"}),
                status=405,
                mimetype="application/json"
            )


class GetAllTickets(Resource):
    @jwt_required
    def get(self):
        user_id = get_jwt_identity()
        checkuser = session.query(User).filter(User.id == user_id).one()
        if checkuser.admin != 1:
            return Response(
                response=json.dumps({"message": "Not allowed for users"}),
                status=400,
                mimetype="application/json"
            )
        ticket = session.query(Ticket).all()
        if ticket:
            return Response(
                response=json.dumps(ticket, cls=AlchemyEncoder),
                status=201,
                mimetype="application/json"
            )
        return Response(
                response=json.dumps({"message": "Not found"}),
                status=404,
                mimetype="application/json"
            )


class GetAllUserTickets(Resource):
    @jwt_required
    def get(self, uid):
        user_id = get_jwt_identity()
        checkuser = session.query(User).filter(User.id == user_id).one()
        if checkuser.admin != 1:
            return Response(
                response=json.dumps({"message": "Not allowed for users"}),
                status=400,
                mimetype="application/json"
            )
        ticket = session.query(Ticket).filter(Ticket.user_id == uid).all()

        if ticket:
            return Response(
                response=json.dumps(ticket, cls=AlchemyEncoder),
                status=201,
                mimetype="application/json"
            )
        return Response(
            response=json.dumps({"message": "Not found"}),
            status=404,
            mimetype="application/json"
        )


class GetMyTickets(Resource):
    @jwt_required
    def get(self):
        uid = get_jwt_identity()
        ticket = session.query(Ticket).filter(Ticket.user_id == uid).all()

        if ticket:
            return Response(
                response=json.dumps(ticket, cls=AlchemyEncoder),
                status=201,
                mimetype="application/json"
            )
        return Response(
                response=json.dumps({"message": "Not found"}),
                status=404,
                mimetype="application/json"
            )
