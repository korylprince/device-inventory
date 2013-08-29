from __future__ import unicode_literals
import datetime
from ddl import *

db.create_all()
session = db.session

u = User()
u.username, u.name = 'kory.prince', 'Kory Prince'

dt = Device_Type()
dt.manufacturer = 'HTC'
dt.model = 'One'

d = Device()
d.user = u
d.device_type = dt
d.inventory_number = 100

n = Note()
n.type = 'device'
n.user = u
n.date = datetime.datetime.now()
n.text = 'Awesome note!'

d.notes.append(n)

for x in [u,dt,d,n]:
    session.add(x)

session.commit()
