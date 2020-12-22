from flask import Flask
from flask_restful import Resource, Api

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from controler import *

app = Flask(__name__)
api = Api(app)

engine = create_engine('postgresql://postgres:1111@localhost/mydb', echo=True)

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

if __name__=="__main__":

    api.add_resource(AddShow, '/shows')
    api.add_resource(GetAllShows, '/shows')

    api.add_resource(SignUpUser, '/user')
    api.add_resource(DeleteUser, '/user/<int:id>')
    api.add_resource(GetUser, '/user/<int:id>')
    api.add_resource(GetAllUsers, '/user')

    api.add_resource(AddTicket, '/tickets/<int:sid>')
    api.add_resource(BuyTicket, '/tickets/buy/<int:tid>/<int:uid>')
    api.add_resource(ReserveTicket, '/tickets/reserve/<int:tid>/<int:uid>')
    api.add_resource(DeleteReservationTicket, '/tickets/<int:tid>')
    api.add_resource(GetAllUserTickets, '/tickets/<int:uid>')
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
    "name": "Petro",
    "password": "!@#123",
    "phone": "22324345",
    "mail": "wamatj@gmail.com"
}
    TICKET
{
    "clas": "VIP"
}
"""

