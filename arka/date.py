from datetime import datetime
from zoneinfo import ZoneInfo

jkt = ZoneInfo("Asia/Jakarta")

def getTodayDate(zoneinfo: ZoneInfo = jkt):
    return datetime.now(zoneinfo).date().strftime("%d-%m-%Y")
