import random
import string
import os, json
import datetime, time

from flask_mail import Message
from dashboard import mail, db
from dashboard.models import Trigger, SelfCheck, Sensor
from geopy.geocoders import Nominatim

triggers = os.path.abspath('dashboard/data/trigger')
selfchecks = os.path.abspath('dashboard/data/selfcheck')

engine = db.create_engine("mysql+pymysql://root@localhost/kifss")
connection = engine.connect()

def generate_password(length):
    """Method to generate a random password for a given length"""
    password = "".join(random.choices(string.ascii_uppercase + string.digits, k=length))
    return password


def send_notification(recipients, subject, message):
    """Method to send email notifications"""
    msg = Message(
        subject=subject,
        sender=os.environ.get('MAIL_USERNAME'),
        recipients=recipients
    )
    msg.body = message
    mail.send(msg)

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

            if sensor:
                for row in sensor:
                    exists = db.session.query(Trigger).filter_by(serial_number=serial_number, date=date).first()
                    if not exists:
                        new_trigger = Trigger(serial_number=serial_number, status=status, date=date, assessed=0)
                        db.session.add(new_trigger)

        except FileNotFoundError:
            continue

    db.session.commit()

    for f in os.listdir(path=selfchecks):
        try:
            f_opened = open(os.path.join(selfchecks, f))
            data = json.load(f_opened)
            
            serial_number = data.get("Serial number")
            status = data.get("Status")
            date = data.get("Date")
            date = datetime.datetime.fromtimestamp(date/1000)

            sensor = connection.execute('SELECT * FROM Sensor WHERE serial_number="' + serial_number + '"')

            if sensor:
                for row in sensor:
                    exists = db.session.query(SelfCheck).filter_by(serial_number=serial_number, date=date).first()
                    if not exists:
                        new_selfcheck = SelfCheck(serial_number=serial_number, status=status, date=date, assessed=0)
                        db.session.add(new_selfcheck)

        except FileNotFoundError:
            continue

    db.session.commit()
        

def add_example_sensors(organization):
    sensors = []
    locations = [["187 Fairview Drive", "Danestone", "Aberdeen"], ["191 Fairview Drive", "Danestone", "Aberdeen"], ["197 Fairview Drive", "Danestone", "Aberdeen"],
                 ["215 Fairview Drive", "Danestone", "Aberdeen"], ["71 Fairview Drive", "Danestone", "Aberdeen"], ["21 Tillydrone Ave", "Aberdeen", "AB24 2TE"],
                 ["21 Station Road", "Dyce", "Aberdeen"], ["25 Station Road", "Dyce", "Aberdeen"], ["27 Station Road", "Dyce", "Aberdeen"],
                 ["14 Trinity Court", "Westhill", "Aberdeenshire"]]
    locator = Nominatim(user_agent="kifss")

    for i in range(len(locations)):
        loc = locator.geocode(locations[i][0] + ", " + locations[i][1] + ", " + locations[i][2])
        if i < 9:
            if loc is not None:
                sensors.append(Sensor("A00000000" + str(i+1), "Flat 1", organization, locations[i][0], locations[i][1], locations[i][2], loc.latitude, loc.longitude))
            else:
                sensors.append(Sensor("A00000000" + str(i+1), "Flat 1", organization, locations[i][0], locations[i][1], locations[i][2], "", ""))
        else:
            if loc is not None:
                sensors.append(Sensor("A000000010", "Flat 1", organization, locations[i][0], locations[i][1], locations[i][2], loc.latitude, loc.longitude))
            else:
                sensors.append(Sensor("A000000010", "Flat 1", organization, locations[i][0], locations[i][1], locations[i][2], "", ""))
    
    for i in sensors:
        db.session.merge(i)
    
    db.session.commit()


def get_sensors(org_id):
    sensors = db.session.query(Sensor).all()
    list = {'data': []}
    for s in sensors:
        d = s.__dict__
        d.pop("_sa_instance_state")
        list['data'].append(d)

    return list
        

def get_self_checks(org_id):
    sql ="""WITH first_query AS (
            SELECT *
            FROM Sensor
            WHERE organization_id = """ + str(org_id) + """ GROUP BY serial_number) SELECT
            * FROM SelfCheck JOIN first_query ON SelfCheck.serial_number
            = first_query.serial_number ORDER BY SelfCheck.date"""
    selfchecks = connection.execute(sql).fetchall()

    # print(selfchecks)

    columns = ['id', 'serial_number', 'status', 'date', 'assessed']
    list = {'selfchecks': []}
    for s in selfchecks:
        d = {key:value for key,value in zip(columns, s)}
        d["date"] = time.mktime(d["date"].timetuple())
        list['selfchecks'].append(d)

    return list

def get_triggers(org_id):
    sql ="""WITH first_query AS (
            SELECT *
            FROM Sensor
            WHERE organization_id = """ + str(org_id) + """ GROUP BY serial_number) SELECT
            * FROM Trigger JOIN first_query ON Trigger.serial_number
            = first_query.serial_number ORDER BY Trigger.date"""
    triggers = connection.execute(sql).fetchall()

    # print(triggers)

    columns = ['id', 'serial_number', 'status', 'date', 'assessed']
    list = {'triggers': []}
    for s in triggers:
        d = {key:value for key,value in zip(columns, s)}
        d["date"] = time.mktime(d["date"].timetuple())
        list['triggers'].append(d)

    return list