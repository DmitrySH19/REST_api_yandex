from datetimerange import DateTimeRange
from datetime import datetime, timezone

# time_range = DateTimeRange(*("14:09-15:10").split('-'))
# time_range2 =  DateTimeRange(*["9:00", "13:10"])
# t3 =  datetime.timedelta(0,60)
# inntersection = time_range2.intersection(time_range)
# print(type(inntersection),str(inntersection))
# if str(inntersection) == 'NaT - NaT':
#     print('good')
# print(type(inntersection.timedelta >= datetime.timedelta(minutes=1)))
# print(datetime.timedelta(minutes=1))
date = datetime.utcnow().isoformat()[:-3]+'Z'
print ()
#r = datetime.datetime.strptime(str(inntersection), '"%Y-%m-%dT%H:%M:%S%z"')
#print(time_range2.intersection(time_range))
from rfc3339_validator import validate_rfc3339
print(validate_rfc3339(date))