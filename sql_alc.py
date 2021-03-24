from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db_conf import Couriers, Regions, Working_hours, Orders, Delivery_hours,Complete_order_id
from courier_model import courier_model, formatted_date



def sql_insert(json_list,session):

    insert_id = []
    for i in range(len(json_list)): 
        session.add(Couriers(id=json_list[i]['courier_id'], courier_type=json_list[i]['courier_type'])) 
        for j in range(len(json_list[i]['regions'])):
            session.add(Regions(courier_id=json_list[i]['courier_id'], region = json_list[i]['regions'][j]))
        for j in range(len(json_list[i]['working_hours'])):
            parse_hours = json_list[i]['working_hours'][j].split('-')
            session.add(Working_hours(courier_id = json_list[i]['courier_id'],\
                                    start_hours = parse_hours[0], end_hours = parse_hours[1]))
        insert_id.append({'id': json_list[i]['courier_id']})
    session.commit()                                     
    
    return insert_id

def sql_patch(json_list,courier_id,session):
    for key in json_list.keys():
        if key == 'courier_type':
            edited = session.query(Couriers).filter_by(id=int(courier_id)).one()
            edited.courier_type = json_list['courier_type']
            session.add(edited)
            session.commit()
        elif key == 'regions':
            delete = session.query(Regions).filter_by(courier_id=int(courier_id))
            for d in delete:
                session.delete(d)
            session.commit()
            for j in range(len(json_list['regions'])):
                session.add(Regions(courier_id=int(courier_id), region = json_list['regions'][j]))
            session.commit() 
        elif key == 'working_hours':
            delete = session.query(Working_hours).filter_by(courier_id=int(courier_id))
            for d in delete:
                session.delete(d)
            session.commit()
            for j in range(len(json_list['working_hours'])):
                parse_hours = json_list['working_hours'][j].split('-')
                session.add(Working_hours(courier_id = int(courier_id),\
                                        start_hours = parse_hours[0], end_hours = parse_hours[1]))
            session.commit()
    return get_info_by_id(courier_id,session)



def get_info_by_id(courier_id,session):
    courier = {"courier_id": courier_id}
    c_type = session.query(Couriers).filter_by(id=int(courier_id)).all()
    print(c_type)
    if c_type:
        courier['courier_type'] =  c_type[0].courier_type
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

def valid_id_courier(courier_id,session):
    return bool(session.query(Couriers).filter_by(id=int(courier_id)).all())

def inset_orders(json_list,session):
    insert_id = []
    for i in range(len(json_list)): 
        session.add(Orders(order_id=json_list[i]['order_id'],\
                             weight=json_list[i]['weight'], region = json_list[i]['region']))
        session.commit()
        for j in range(len(json_list[i]['delivery_hours'])):
            parse_hours = json_list[i]['delivery_hours'][j].split('-')
            session.add(Delivery_hours(order_id = json_list[i]['order_id'],\
                                    start_hours = parse_hours[0], end_hours = parse_hours[1]))
        insert_id.append({'id': json_list[i]['order_id']})
    session.commit()
    return insert_id

def assign_orders(json_list,session):
    courier = get_info_by_id(json_list['courier_id'], session)
    condition = (0.01,50.0)
    if courier['courier_type'] == 'foot':
        condition = (0.01,10.0)
    if courier['courier_type'] == 'bike':
        condition = (0.01,15.0)
    if courier['courier_type'] == 'car':
        condition = (0.01,50.0)
    
    cur_orders = [r.order_id for r in session.query(Complete_order_id.order_id).distinct()]

    x = session.query(Orders.order_id,
                     Orders.weight,
                     Orders.region,
                     Delivery_hours.start_hours,
                     Delivery_hours.end_hours,
                     )\
        .filter(
            Orders.region.in_(courier['regions']),
            Orders.weight.between(*condition),
            Orders.order_id == Delivery_hours.order_id,
            Orders.order_id.notin_(cur_orders)
                                        ).all()
    
   
    if x != None:
        c = session.query(Orders.order_id).\
            filter(Orders.order_id == (Complete_order_id.order_id)).all()
        avaibale_orders = []
        prev_ord = None
        count = 0
        first = False
        for st in x:
            if not prev_ord:
                prev_ord = st.order_id
                first = True
            if prev_ord == st.order_id and (not first):
                avaibale_orders[count-1][3].append(str(st.start_hours)+'-'+str(st.end_hours))
            else:
                count += 1
                avaibale_orders.append((
                    st.order_id,
                    st.weight,
                    st.region,
                    [str(st.start_hours)+'-'+str(st.end_hours)]
                ))
                first = False
                prev_ord = st.order_id
        c = courier_model(courier=courier,orders = avaibale_orders).assign_orders()
        if c:
            answer = {
                'orders':[],
                "assign_time": formatted_date(),
                }
            print(c)
            for order in c:
                answer['orders'].append({'id':order[0]})
                session.add(Complete_order_id(order_id = order[0], courier_id = courier['courier_id'],\
                            assign_time = answer['assign_time']))
            session.commit()
            return answer
        else:
            return {'orders':[]}

def complete_orders(json_list,session):
    pass

def validate_order_courier(json_list,session):
    x = session.query(Complete_order_id.order_id,Complete_order_id.courier_id)\
                .filter(
                        Complete_order_id.order_id == json_list["order_id"],
                        Complete_order_id.courier_id == json_list["courier_id"]
                                                    ).all()
    if x:
        session.query(Complete_order_id).\
        filter(Complete_order_id.order_id == json_list["order_id"],
               Complete_order_id.courier_id == json_list["courier_id"]).\
        update({"complete_time": json_list["complete_time"]})
        session.commit()
        return True  
    else:
        return False