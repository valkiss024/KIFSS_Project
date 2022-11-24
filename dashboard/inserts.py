from dashboard import db
from dashboard.models import Trigger, SelfCheck, Sensor
from geopy.geocoders import Nominatim
import json, os
import datetime

triggers = os.path.abspath('dashboard/data/trigger')
selfchecks = os.path.abspath('dashboard/data/selfcheck')

engine = db.create_engine("mysql+pymysql://root@localhost/kifss")
connection = engine.connect()

def json_to_sql():

    for f in os.listdir(path=triggers):
        try:
            f_opened = open(os.path.join(triggers, f))
            data = json.load(f_opened)
            
            serial_number = data.get("Serial number")
            status = data.get("Status")
            date = data.get("Date")
            date = datetime.datetime.fromtimestamp(date/1000)

            sensor = connection.execute('SELECT * FROM Sensor WHERE serial_number="' + serial_number + '"')

            for row in sensor:
                new_trigger = Trigger(serial_number=serial_number, status=status, date=date, assessed=0)
                exists = db.session.query(Trigger).filter_by(serial_number=serial_number, date=date).first()
                if not exists:
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
            date = datetime.datetime.fromtimestamp(date/1000)

            sensor = connection.execute('SELECT * FROM Sensor WHERE serial_number="' + serial_number + '"')

            for row in sensor:
                new_selfcheck = SelfCheck(serial_number=serial_number, status=status, date=date, assessed=0)
                exists = db.session.query(SelfCheck).filter_by(serial_number=serial_number, date=date).first()
                if not exists:
                    db.session.add(new_selfcheck)

            db.session.commit()

        except FileNotFoundError:
            continue
        

def add_example_sensors(organization):
    sensors = []
    locations = [["187 Fairview Drive", "Aberdeen", "Aberdeenshire"], ["191 Fairview Drive", "Aberdeen", "Aberdeenshire"], ["197 Fairview Drive", "Aberdeen", "Aberdeenshire"],
                 ["215 Fairview Drive", "Aberdeen", "Aberdeenshire"], ["71 Fairview Drive", "Aberdeen", "Aberdeenshire"], ["21 Tillydrone Avenue", "Aberdeen", "Aberdeenshire"],
                 ["9 Merrivale, Station Road", "Dyce", "Aberdeenshire"], ["5 Merrivale, Station Road", "Dyce", "Aberdeenshire"], ["7 Merrivale, Station Road", "Dyce", "Aberdeenshire"],
                 ["14 Trinity Court", "Westhill", "Aberdeenshire"]]
    locator = Nominatim(user_agent="kifss")

    for i in range(len(locations)):
        loc = locator.geocode(locations[i][0] + "," + locations[i][1] + "," + locations[i][2])
        if loc is not None:
            sensors.append(Sensor("A00000000" + str(i+1), "Flat 1", "Pass", datetime.datetime.now(), organization, locations[i][0], locations[i][1], locations[i][2], loc.latitude, loc.longitude))
        else:
            sensors.append(Sensor("A00000000" + str(i+1), "Flat 1", "Pass", datetime.datetime.now(), organization, locations[i][0], locations[i][1], locations[i][2], "", ""))
    
    for i in sensors:
        db.session.merge(i)
    
    db.session.commit()