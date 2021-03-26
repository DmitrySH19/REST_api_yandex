#{"data": [{"courier_id": 1,"courier_type": "foot","regions": [1, 12, 22],"working_hours": ["11:35-14:05", "09:00-11:00"]},{"courier_id": 2,"courier_type": "bike","regions": [22],"working_hours": ["09:00-18:00"]},{"courier_id": 3,"courier_type": "car","regions": [12, 22, 23, 33],"working_hours": []}]}

#curl --header "Content-Type: application/json"   --request POST   --data '{"data": [{"courier_id": 1,"courier_type": "foot","regions": [1, 12, 22],"working_hours": ["11:35-14:05", "09:00-11:00"]},{"courier_id": 2,"courier_type": "bike","regions": [22],"working_hours": ["09:00-18:00"]},{"courier_id": 3,"courier_type": "car","regions": [12, 22, 23, 33],"working_hours": []}]}' http://localhost:5000/couriers





from sqlalchemy import *
from sqlalchemy.orm import create_session
from sqlalchemy.schema import Table, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config import DB_URL

DB_URL = 'mysql://root:Ficka1@2@3@@localhost:3306/couriers'
#Create and engine and get the metadata
engine = create_engine(DB_URL)
Base = declarative_base(engine)

metadata = MetaData(bind=engine)
#Reflect each database table we need to use, using metadata
class Couriers(Base):
    __table__ = Table('couriers', metadata, autoload=True)

class Regions(Base):
    __table__ = Table('regions', metadata,autoload=True)

class Working_hours(Base):
    __table__ = Table('working_hours', metadata, autoload=True)

class Orders(Base):
    __table__ = Table('orders', metadata, autoload=True)

class Delivery_hours(Base):
    __table__ = Table('delivery_hours', metadata, autoload=True)

class Complete_order_id(Base):
    __table__ = Table('complete_order_id', metadata, autoload=True)



# #Create a session to use the tables    
# session = create_session(bind=engine)

# #Here I will just query some data using my foreign key relation,  as you would
# #normally do if you had created a declarative data mode.
# #Note that not all test records have an author so I need to accomodate for Null records
# testlist = session.query(Couriers.id,Couriers.courier_type,Regions.region).filter(Couriers.id == Regions.courier_id).all() 

# for test in testlist:
#     #testauthor = session.query(Couriers)
#     print(test.id,test.courier_type,test.region)



# testlist = session.query(Couriers.id,Couriers.courier_type,Regions.region).filter(Couriers.id == Regions.courier_id).all() 

# for test in testlist:
#     #testauthor = session.query(Couriers)
#     print(test.id,test.courier_type,test.region)