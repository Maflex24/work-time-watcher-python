from datetime import datetime, date
import time

# start_date = datetime.now().timestamp()
# print("start_date", start_date)

# time.sleep(30)

# next_date = datetime.now().timestamp()
# print("next_date", next_date)

# date_diffrence = datetime.fromtimestamp(next_date - start_date)
# print("date_diffrence", date_diffrence.minute, date_diffrence.second)


no_utc = datetime.fromtimestamp(10_800)
with_utc = datetime.utcfromtimestamp(10_800)

print(no_utc)
print(with_utc)