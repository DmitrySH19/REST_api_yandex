from config import SQLITE, databaseFile
from sqlalchemy import create_engine, MetaData, Table, Column
from sqlalchemy.orm import mapper, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Integer, String, Text, FLOAT
from sqlalchemy.ext.hybrid import hybrid_property, hybrid_method
from sqlalchemy import and_
from date_utils import time_intersection
from courier_model import courier_model,formatted_date

class Couriers(object):

    id = Column(Integer)
    courier_type = Column(String)

    def __init__(self, id, courier_type):
        self.id = id
        self.courier_type = courier_type     

class Regions(object):

    id = Column(Integer)
    courier_id = Column(Integer)
    region = Column(Integer)

    def __init__(self,courier_id, region):
        self.courier_id = courier_id
        self.region = region

class Working_hours(object):

    id = Column(Integer)
    courier_id = Column(Integer)
    start_hours = Column(String)
    end_hours = Column(String)

    def __init__(self,courier_id, start_hours, end_hours):
        self.courier_id = courier_id
        self.start_hours = start_hours
        self.end_hours = end_hours

class Orders(object):

    order_id = Column(Integer)
    weight = Column(FLOAT())
    region = Column(Integer)
   

    def __init__(self,order_id, weight, region):

        self.order_id = order_id
        self.weight = weight
        self.region = region

class Delivery_hours(object):
    
    id = Column(Integer)
    order_id = Column(Integer)
    start_hours = Column(String)
    end_hours = Column(String)

    def __init__(self,order_id, start_hours, end_hours):
        self.order_id = order_id
        self.start_hours = start_hours
        self.end_hours = end_hours

class Complete_order_id(object):

    order_id = Column(Integer)
    courier_id = Column(Integer)
    assign_time = Column(String)
    complite_time = Column(String)
    order_num = Column(Integer)

    def __init__(self,order_id, courier_id, assign_time, complite_time = None, order_num = None):
        self.order_id = order_id
        self.courier_id = courier_id
        self.assign_time = assign_time
        self.complite_time = complite_time
        self.order_num = order_num

class MyDatabase:
    
    DB_ENGINE = {
        SQLITE: 'sqlite:///{DB}'
    }

    db_engine = None
    def __init__(self, dbtype, username='', password='', dbname=''):
        dbtype = dbtype.lower()
        if dbtype in self.DB_ENGINE.keys():
            engine_url = self.DB_ENGINE[dbtype].format(DB=dbname)
            # loadas db engine
            self.db_engine = create_engine(engine_url)
            #loads meta existing databasese
            self.meta = MetaData(bind=self.db_engine)

            couriers = Table('couriers', self.meta, autoload=True)
            mapper(Couriers, couriers)

            regions = Table('regions', self.meta, autoload=True)
            mapper(Regions, regions)

            working_hours = Table('working_hours', self.meta, autoload=True)
            mapper(Working_hours, working_hours)

            orders = Table('orders', self.meta, autoload=True)
            mapper(Orders, orders)

            delivery_hours = Table('delivery_hours', self.meta, autoload=True)
            mapper(Delivery_hours, delivery_hours)

            complete_order_id = Table('complete_order_id', self.meta, autoload=True)
            mapper(Complete_order_id, complete_order_id)

        else:
            print("DBType is not found in DB_ENGINE")

        
    def load_sesion(self):
        Session = sessionmaker(bind=self.db_engine)
        return Session()
        
    def insert_courier(self,courier, session):

        session.add(Couriers(id=courier['courier_id'], courier_type=courier['courier_type'])) 

        for j in range(len(courier['regions'])):
            session.add(Regions(courier_id=courier['courier_id'], region = courier['regions'][j]))

        for j in range(len(courier['working_hours'])):
            parse_hours = courier['working_hours'][j].split('-')
            session.add(Working_hours(courier_id = courier['courier_id'],\
                                      start_hours = parse_hours[0], end_hours = parse_hours[1]))
        
    def courier_patch_by_key(self, courier_id, field , session):
        
        if 'courier_type' in field.keys():
            edited = session.query(Couriers).filter_by(id=int(courier_id)).one()
            edited.courier_type = field['courier_type']
            session.add(edited)
        elif 'regions' in field.keys():
            delete = session.query(Regions).filter_by(courier_id=int(courier_id))
            for d in delete:
                session.delete(d)
            for j in range(len(field['regions'])):
                session.add(Regions(courier_id=int(courier_id), region = field['regions'][j]))

        elif 'working_hours' in field.keys():
            delete = session.query(Working_hours).filter_by(courier_id=int(courier_id))
            for d in delete:
                session.delete(d)
            for j in range(len(field['working_hours'])):
                parse_hours = field['working_hours'][j].split('-')
                session.add(Working_hours(courier_id = int(courier_id),\
                                        start_hours = parse_hours[0], end_hours = parse_hours[1]))
        
        return self.get_couier_by_id(courier_id, session)


    def get_couier_by_id(self, courier_id, session):
       
        if self.valid_id_courier(courier_id, session):
            courier = {"courier_id": courier_id}
            courier_type = session.query(Couriers).filter_by(id=int(courier_id)).all()
            
            courier['courier_type'] =  courier_type[0].courier_type
            regions = session.query(Regions).filter_by(courier_id=int(courier_id)).all()
            region_list = []
            for r in regions:
                region_list.append(r.region)
            courier['regions'] = region_list
            times = session.query(Working_hours).filter_by(courier_id=int(courier_id)).all()
            time = []
            for t in times:
                time.append("{}-{}".format(t.start_hours,t.end_hours))
            courier['working_hours'] = time
            return courier
      

    def valid_id_courier(self, courier_id, session):
        return bool(session.query(Couriers).filter_by(id=int(courier_id)).all())

    def valid_order_id(self,order_id, session):
        return bool(session.query(Orders).filter_by(order_id=int(order_id)).all())

    def is_in_complete_orders(self,order_id,session):
        return bool(session.query(Complete_order_id).filter_by(order_id=int(order_id)).all())
    
    def courier_is_in_complete_orders(self,courier_id,session):
        return bool(session.query(Complete_order_id).filter_by(courier_id=int(courier_id)).all())
    
    def is_courier_complete_orders(self, courier_id, session):
        return bool(session.query(Complete_order_id).filter(Complete_order_id.courier_id == int(courier_id),\
            Complete_order_id.assign_time != None, Complete_order_id.complite_time != None).all())


    def insert_order(self, order, session):
        session.add(Orders(order_id=order['order_id'],\
                             weight=order['weight'], region = order['region']))
        for j in range(len(order['delivery_hours'])):
            parse_hours = order['delivery_hours'][j].split('-')
            session.add(Delivery_hours(order_id = order['order_id'],\
                                    start_hours = parse_hours[0], end_hours = parse_hours[1]))

    def get_order_by_id(self, order_id, session):
        if self.valid_order_id(order_id, session):
            order = {"order": order_id}
            order_weight = session.query(Orders).filter_by(order_id=int(order_id)).first()
            
            order['weight'] =  float(order_weight.weight)
            order['region'] = order_weight.region

            times = session.query(Delivery_hours).filter_by(order_id=int(order_id)).all()
            time = []
            for t in times:
                time.append("{}-{}".format(t.start_hours,t.end_hours))
            order['working_hours'] = time
            return order

    def insert_into_complete(self,courier,order_ids,session):
        if order_ids:

            answer = {
                    'orders':[],
                    "assign_time": formatted_date(),
                    }
            
            for order in order_ids:
                answer['orders'].append({'id':order})
                session.add(Complete_order_id(order_id = order, courier_id = courier['courier_id'],\
                            assign_time = answer['assign_time']))
            
            return answer
        else:
            return {'orders':[]}

    def inset_complete_time(self,order_id,courier_id,complete_time, session):
        count_complite_orders = len(self.get_complete_orders(courier_id,session))
        session.query(Complete_order_id)\
                .filter(Complete_order_id.order_id==order_id,
                        Complete_order_id.courier_id == courier_id)\
                .update({'complite_time':complete_time, 'order_num': count_complite_orders + 1})

        return {'order_id':order_id}

    def order_filtered(self,courier_id, session):

        courier = self.get_couier_by_id(courier_id, session)
        condition = (0.01,50.0)
        if courier['courier_type'] == 'foot':
            condition = (0.01,10.0)
        elif courier['courier_type'] == 'bike':
            condition = (0.01,15.0)
        elif courier['courier_type'] == 'car':
            condition = (0.01,50.0)

        cur_orders = [r.order_id for r in session.query(Complete_order_id.order_id).distinct()]

        #find orders matched by region and weight
        available_orders = [r.order_id for r in \
                                session.query(Orders.order_id)\
                                .filter(
                                Orders.region.in_(courier['regions']),
                                Orders.weight.between(*condition),
                                Orders.order_id == Delivery_hours.order_id,
                                Orders.order_id.notin_(cur_orders)
                                                            ).all()]
        # unique orders id's
        available_orders = list(set(available_orders))

        if available_orders:
            orders = []
            for id in available_orders:
                orders.append(self.get_order_by_id(id,session))

            return orders
        else:
            return False
    
    def delete_uncomplete_by_id(self,order_id, session):
        
        delete = session.query(Complete_order_id).filter(Complete_order_id.order_id == order_id).one()
        session.delete(delete)

    def get_uncomplete_orders(self, courier_id, session):
        uncomplite= session.query(Complete_order_id.order_id,Complete_order_id.assign_time)\
                            .filter(Complete_order_id.courier_id == courier_id,\
                                    Complete_order_id.complite_time == None)\
                            .all()
        print(uncomplite)
        #uncomplite = [x[0] for x in uncomplite]
        return uncomplite
    
    def get_complete_orders(self, courier_id,session):
        complite = session.query(Orders.order_id,Orders.region,Complete_order_id.assign_time,Complete_order_id.complite_time,Complete_order_id.order_num)\
                            .filter(Complete_order_id.courier_id == courier_id,\
                                    Complete_order_id.complite_time != None,\
                                    Complete_order_id.order_id == Orders.order_id
                                    )\
                            .all()      
        return complite