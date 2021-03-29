import dateutil.parser
import numpy as np


class courier_statistic():
    def __init__(self, courier, complite_orders):
        self.courier = courier
        self.complite_orders = sorted(complite_orders, key=lambda x: x[1])
        self.count_orders = len(self.complite_orders)

    def calulate_statistic(self):
        self.split_by_region()
        self.sort_in_order()
        mean_time = self.find_min_time()
        # print(self.complite_orders)
        # print(self.courier)
        # print(self.count_orders)
        rating = self.rating(mean_time)
        earnings = self.earnings()
        return (rating, earnings)

    def rating(self, mean_time):
        return ((60*60 - min(mean_time, 60*60))/(60*60)) * 5

    def earnings(self):
        koef = 2
        if self.courier['courier_type'] == 'bike':
            koef = 5
        elif self.courier['courier_type'] == 'car':
            koef = 9
        return self.count_orders * (500 * koef)

    def split_by_region(self):
        cur_region = self.complite_orders[0][1]
        orderered_orders = [[]]
        counter = 0
        for order in self.complite_orders:
            if cur_region == order[1]:

                orderered_orders[counter].append(order)
            else:
                orderered_orders.append([order])
                cur_region = order[1]
                counter += 1
        self.complite_orders = orderered_orders

    def sort_in_order(self):
        print('before', self.complite_orders)
        sorted_orders = []
        for ord in self.complite_orders:
            sorted_orders.append(sorted(ord, key=lambda x: x[4]))

        self.complite_orders = sorted_orders
        print('after', self.complite_orders)

    def find_min_time(self):
        mean_times = []
        for region in self.complite_orders:
            mean_times.append(self.calculate_mean_times(region))
        print('mean_times', mean_times)
        mean_per_region = list(map(np.mean, mean_times))
        print('mean_times', mean_per_region)
        min_mean_time = min(mean_per_region)
        print('min_time', min_mean_time)
        return min_mean_time

    def calculate_mean_times(self, region):
        prev_time = None
        mean_times = []
        for ord in region:
            if prev_time:
                complite = dateutil.parser.isoparse(ord[3])
                delta = abs(prev_time - complite)
                prev_time = complite
                mean_times.append(delta.seconds)
            else:
                assign, complite = dateutil.parser.isoparse(
                    ord[2]), dateutil.parser.isoparse(ord[3])
                delta = abs(assign - complite)
                mean_times.append(delta.seconds)
                prev_time = complite

        return mean_times
