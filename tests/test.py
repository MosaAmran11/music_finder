import datetime

date = datetime.datetime.fromisoformat('2025-06-27T00:00:00+00:00')
print(date)
print(date.isoformat())
print(date.strftime('%Y'))
print(date.strftime('%Y-%m-%d'))
print(date.strftime('%Y-%m-%d %H:%M:%S'))
print(date.strftime('%Y-%m-%d %H:%M:%S.%f'))
print(date.strftime('%Y-%m-%d %H:%M:%S.%f%z'))
print(date.strftime('%Y-%m-%d %H:%M:%S.%f%z'))