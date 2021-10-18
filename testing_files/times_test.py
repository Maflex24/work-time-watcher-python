from useful_functions import debugInfo
from datetime import date, datetime
times = {
        'today_date': '',
        'worktime_hours': None,
        'workrime_minutes': None,
        'total_worktime': None,
        'total_breaktime': None,
        'works': [
            {
                'key1': "value",
                'key2': None
            },
            {
                "key1": "some value",
                'key2': 16
            }
        ], 
        'breaks': []
    }

print(times)
# times['works'][0] = {
#         'start': datetime.now().timestamp(),
#         'stop': None,
#         'time': None
#     }

times['works'].append({"key3": "some value", 'key3': 38})

print(times['works'][0])
print(times['works'][1])
print(times['works'][2])