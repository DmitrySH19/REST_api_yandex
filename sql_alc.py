from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from courier_model import courier_model, formatted_date
from courier_statistic import courier_statistic

# class for connect database and flask requests


class sqlite_connector():
    def __init__(self, db_obj):
        self.db = db_obj

    def insert_couers(self, json_response):
        insert_id = []
        couriers = json_response['data']
        session = self.db.load_sesion()

        for courier in couriers:
            self.db.insert_courier(courier, session)
            insert_id.append({'id': courier['courier_id']})

        session.commit()
        session.close()

        return insert_id

    def patch_courier(self, json_response, courier_id):
        session = self.db.load_sesion()
        edited = self.db.valid_id_courier(courier_id, session)
        if edited:
            for key in json_response.keys():
                edited = self.db.courier_patch_by_key(
                    courier_id, {key: json_response[key]}, session)
        if self.db.courier_is_in_complete_orders(edited['courier_id'], session):
            uncomplite_ids = [x[0] for x in self.db.get_uncomplete_orders(
                edited['courier_id'], session)]
            check_orders = []
            for ord in uncomplite_ids:
                check_orders.append(self.db.get_order_by_id(ord, session))

            check_output = courier_model(edited, check_orders).assign_orders()
            check_orders = [x['order'] for x in check_orders]
            #check_output = [x['order_id'] for x in check_output]
            print('change_cour', edited)
            if check_orders != check_output:
                print('change')
                for ord in check_orders:
                    print(ord)
                    self.db.delete_uncomplete_by_id(ord, session)
                self.db.insert_into_complete(edited, check_output, session)

            print("1", check_orders)
            print("2", check_output)

        session.commit()
        session.close()
        return edited

    def insert_orders(self, json_response):
        insert_id = []
        orders = json_response['data']
        session = self.db.load_sesion()

        for order in orders:
            self.db.insert_order(order, session)
            insert_id.append({'id': order['order_id']})
        session.commit()
        session.close()
        return insert_id

    def assign_orders(self, json_response):
        session = self.db.load_sesion()
        if self.db.valid_id_courier(json_response['courier_id'], session):
            # filter orders by region and weight
            uncomplete = self.db.get_uncomplete_orders(
                json_response['courier_id'], session)
            print('UNCOMPLETE', uncomplete)
            if uncomplete:
                answer = {
                    'orders': [{'id': x[0]} for x in uncomplete],
                    "assign_time": uncomplete[0][1]
                }

                session.commit()
                session.close()
                return answer
            else:
                available_orders = self.db.order_filtered(
                    json_response['courier_id'], session)

                courier = self.db.get_couier_by_id(
                    json_response['courier_id'], session)
                answer = {'orders': []}
                if available_orders:

                    take_ids = courier_model(
                        courier=courier, orders=available_orders).assign_orders()
                    answer = self.db.insert_into_complete(
                        courier, take_ids, session)

                    session.commit()
                    session.close()
                return answer
        else:
            return False

    def complete_orders(self, json_request):

        session = self.db.load_sesion()
        if self.db.is_in_complete_orders(json_request['order_id'], session)\
                and self.db.courier_is_in_complete_orders(json_request['courier_id'], session):
            answer = self.db.inset_complete_time(json_request['order_id'], json_request['courier_id'],
                                                 json_request['complete_time'], session)
            session.commit()
            session.close()
            return answer
        else:
            return False

    def get_courier(self, courier_id):
        session = self.db.load_sesion()
        if self.db.valid_id_courier(courier_id, session):
            courier = self.db.get_couier_by_id(courier_id, session)
            if self.db.is_courier_complete_orders(courier_id, session):
                orders = self.db.get_complete_orders(courier_id, session)
                rating, earnings = courier_statistic(
                    courier, orders).calulate_statistic()
                print('rating', rating)
                print('earnings', earnings)
                session.commit()
                session.close()
                courier['rating'] = rating
                courier['earnings'] = earnings
                return courier
            else:
                print('not one complete_order')
                return courier
