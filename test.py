from datetime import datetime, timedelta, timezone

today = datetime.now()
after_10_day = today + timedelta(days = 20)
print(today)
print(after_10_day)