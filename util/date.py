import time
from datetime import datetime

def get_date_str():
    now = datetime.now()
    dt_string = now.strftime("%d%m%Y")
    return dt_string

print(get_date_str())