
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
        self.avaliable_ord = []
        for ord in orders:
            self.avaliable_ord.append(tuple(ord.values()))
        self.time_delta = datetime.timedelta(minutes=1)
        
    
    def time_intersection(self, date1, date2, time_delta = datetime.timedelta(minutes=1)):
        print(date1)
        print(date2)
        intersection = DateTimeRange(*(date1.split('-')))\
                            .intersection(DateTimeRange(*(date2.split('-'))))
        if str(intersection) != 'NaT - NaT':
            intersection = DateTimeRange(*(date1.split('-')))\
                            .intersection(DateTimeRange(*(date2.split('-'))))               
            return intersection.timedelta >= time_delta
        else:
            return False     

    def data_intersection(self,date1,date2):

        intersection = DateTimeRange(*(date1.split('-')))\
                            .intersection(DateTimeRange(*(date2.split('-'))))
        if str(intersection) != 'NaT - NaT':
            intersection = DateTimeRange(*(date1.split('-')))\
                            .intersection(DateTimeRange(*(date2.split('-'))))               
            return intersection.timedelta >= self.time_delta
        else:
            return False  
    
    def maximize_weight(self, min = True, max = False):
        take_orders = []
        self.take_orders = sorted(self.take_orders, key=lambda x: x[1],reverse=(min or max))
        if self.take_orders[0][1] <= self.max_weight:
            temp_weight = self.take_orders[0][1]
            take_orders.append(self.take_orders[0])
            for i in range(1,len(self.take_orders)):
                print('weight',self.take_orders[i])
                if temp_weight + self.take_orders[i][1] <= self.max_weight:
                    temp_weight += self.take_orders[i][1]
                    take_orders.append(self.take_orders[i])
            return take_orders
    
    def weight_check(self):
        take_orders_min = self.maximize_weight(min=False)
        take_orders_max = self.maximize_weight(max=True)
        print(take_orders_min)
        print(take_orders_max)

        if take_orders_min and (not take_orders_max):
            self.take_orders = take_orders_min
        elif (not take_orders_min) and take_orders_max:
            self.take_orders = take_orders_max
        elif take_orders_max and take_orders_min:

            if (len(take_orders_max) == len(take_orders_min))\
                or (len(take_orders_max) > len(take_orders_min)):
                self.take_orders = take_orders_max
            elif len(take_orders_max) < len(take_orders_min):
                self.take_orders = take_orders_min
        else:
            self.take_orders = []
        
        return self.take_orders

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
        print('take_orders:', self.take_orders)
        if self.take_orders:
            self.weight_check()
        take_ids = [r[0] for r in self.take_orders]
        return take_ids





