from flask import json, Response, request
from flask_restful import Resource, Api
from models import *
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.ext.declarative import DeclarativeMeta
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
    def post(self):
        data = request.json

        try:
            show = Show(data["name"],data["show_type"],data["description"],data["time"],data["place"])
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
            user = User(data["name"],data["password"],data["phone"],data["mail"])
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


class GetAllUsers(Resource):
    def get(self):
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
    def delete(self, id):
        user = session.query(User).filter(User.id==id).delete()
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
    def get(self, id):
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



class AddTicket(Resource):
    def post(self, sid):

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
    def put(self, tid, uid):

        try:
            ticket = session.query(Ticket).get(tid)
            if not ticket.is_avaliable:
                return Response(
                    response=json.dumps({"message": "This item is already bought or reserved"}),
                    status=405,
                    mimetype="application/json"
                )
            ticket.is_avaliable = 0
            ticket.user_id = uid

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
    def put(self, tid, uid):

        try:
            ticket = session.query(Ticket).get(tid)
            if not ticket.is_avaliable:
                return Response(
                    response=json.dumps({"message": "This item is already bought or reserved"}),
                    status=405,
                    mimetype="application/json"
                )
            ticket.is_avaliable = 0
            ticket.user_id = uid

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
    def put(self, tid):

        try:
            ticket = session.query(Ticket).get(tid)
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
    def get(self, id):
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

class GetAllTickets(Resource):

    def get(self):
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
    def get(self, uid):
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
