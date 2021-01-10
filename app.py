from flask import Flask
from flask_jwt_extended import JWTManager
from flask_restful import Resource, Api

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from controler import *


app = Flask(__name__)
api = Api(app)

app.config['JWT_SECRET_KEY'] = 'dsfaklgjfodklfjgroakjgkopdankflGADJHGFJKADGN'
jwt = JWTManager(app)

engine = create_engine('postgresql://postgres:1234@localhost/mydb', echo=True)

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

if __name__ == "__main__":

    api.add_resource(AddShow, '/show')
    api.add_resource(GetAllShows, '/shows')

    api.add_resource(SignUpUser, '/register')
    api.add_resource(Login, '/login')
    api.add_resource(DeleteUser, '/user/<int:id>')
    api.add_resource(GetUser, '/user/<int:id>')
    api.add_resource(GetOwnUser, '/user')
    api.add_resource(DeleteMyself, '/user')
    api.add_resource(GetAllUsers, '/users')
    api.add_resource(UpdateUser, '/user')

    api.add_resource(AddTicket, '/ticket/<int:sid>')
    api.add_resource(BuyTicket, '/ticket/buy/<int:tid>')
    api.add_resource(ReserveTicket, '/ticket/reserve/<int:tid>')
    api.add_resource(DeleteReservationTicket, '/ticket/<int:tid>')
    api.add_resource(GetAllUserTickets, '/tickets/<int:uid>')
    api.add_resource(GetMyTickets, '/tickets/own')
    api.add_resource(GetAllTickets, '/tickets')

    app.run(debug=True)

"""               SHOW
  {
    "description": "very funny show",
    "name": "Varjaty Show",
    "place": "Dovjenka theatre",
    "show_id": 1,
    "show_type": "comedy",
    "time": "18-12-2020 18:00:00"
}
    
       USER
{
    "name": "a",
    "password": "!@#123",
    "phone": "22324345",
    "mail": "a@gmail.com",
    "admin": 0
}
    TICKET
{
    "clas": "VIP"
}
"""

