from dashboard import db
from dashboard.models import Trigger, SelfCheck
import json, os
import datetime

triggers = os.path.abspath('dashboard/data/trigger')
selfchecks = os.path.abspath('dashboard/data/selfcheck')

def json_to_sql():

    for f in os.listdir(path=triggers):
        try:
            f_opened = open(os.path.join(triggers, f))
            data = json.load(f_opened)
            
            serial_number = data.get("Serial number")
            status = data.get("Status")
            date = data.get("Date")

            new_trigger = Trigger(serial_number=serial_number, status=status, date=datetime.datetime.fromtimestamp(date/1000), assessed=0)

            db.session.add(new_trigger)
            db.session.commit()

        except FileNotFoundError:
            continue

    for f in os.listdir(path=selfchecks):
        try:
            f_opened = open(os.path.join(selfchecks, f))
            data = json.load(f_opened)
            
            serial_number = data.get("Serial number")
            status = data.get("Status")
            date = data.get("Date")

            new_selfcheck = SelfCheck(serial_number=serial_number, status=status, date=datetime.datetime.fromtimestamp(date/1000), assessed=0)

            db.session.add(new_selfcheck)
            db.session.commit()

        except FileNotFoundError:
            continue