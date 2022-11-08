from datetime import datetime
timestamp = datetime.now()

str_date_time = timestamp.strftime("%d%m%Y_%H%M%S_")
print(str_date_time)