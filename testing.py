from models import Session, show, users, ticket
session1 = Session()
show1 = show(name = 'Jazz Fest', show_id = '1', show_type = 'sitting', description = 'the fest of jazz music', time = '2020-12-28', place = 'park')

user1 = users(name = 'Mark', phone = '0985555552', mail = 'marrrrrkkk@ur.com', id = 1)
user2 = users(name = 'Sin', phone = '0997775552', mail = 'marrk2222k@ur.com', id = 2)

ticket1 = ticket(code = 1234, is_avaliable = 'yes', clas = 'vvip' ,show_ = 1, user_id = 1 )

session1.add(show1)
session1.commit()
session1.add(user1)
session1.add(user2)
session1.commit()
session1.add(ticket1)
session1.commit()
session1.close()
