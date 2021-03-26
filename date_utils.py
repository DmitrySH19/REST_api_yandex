
import datetime
from datetimerange import DateTimeRange

def formatted_date():
    return datetime.datetime.utcnow().isoformat()[:-3]+'Z'

def time_intersection(date1, date2, time_delta = datetime.timedelta(minutes=1)):
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