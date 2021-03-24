
import datetime
from datetimerange import DateTimeRange

def formatted_date():
    return datetime.datetime.utcnow().isoformat()[:-3]+'Z'

class courier_model():
    def __init__(self,courier,orders):
        if courier['courier_type'] == 'foot':
            self.max_weight = 10.0
        elif courier['courier_type'] == 'bike':
            self.max_weight = 15.0
        elif courier['courier_type'] == 'car':
            self.max_weight = 50.0
        self.cur_weight = 0
        self.courier = tuple(courier.values())
        self.avaliable_ord = orders
        self.time_delta = datetime.timedelta(minutes=1)
        
       

    def data_intersection(self,date1,date2):

        intersection = DateTimeRange(*(date1.split('-')))\
                            .intersection(DateTimeRange(*(date2.split('-'))))
        if str(intersection) != 'NaT - NaT':
            intersection = DateTimeRange(*(date1.split('-')))\
                            .intersection(DateTimeRange(*(date2.split('-'))))               
            return intersection.timedelta >= self.time_delta
        else:
            return False  
    def weight_check(self):
        take_orders = []
        self.take_orders = sorted(self.take_orders, key=lambda x: x[1])
        temp_weight = self.take_orders[0][1]
        for order in self.take_orders:
            print(order)
            if temp_weight + order[1] <= self.max_weight:
                temp_weight += order[1]
                take_orders.append(order)
        
        self.take_orders = take_orders


    def assign_orders(self):
        self.take_orders = []
        take_orders = []
        for time_interval in self.courier[3]:
            print("courer:{}".format(time_interval))
            for order in self.avaliable_ord:
                for order_interval in order[3]:
                    if not (order[0] in take_orders):
                        print("order {}:{}".format(order[0],order_interval))
                        if self.data_intersection(time_interval,order_interval):
                            take_orders.append(order[0])
                            self.take_orders.append(order)
                            print('take order {}'.format(order[0]))
        
        del self.avaliable_ord
        if self.take_orders:
            self.weight_check()
        return self.take_orders





