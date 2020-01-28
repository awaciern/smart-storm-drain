from datetime import datetime, timedelta
from random import random
from webapp.models import Device, Transmission


'''
To run this script, open the server shell and run the following command:
exec(open('sim_data/simulate.py').read())
NOTE: The simulated data will be associated with the device specified by pk
'''

# Device we are assigining this data to
device = Device.objects.get(pk=3)

# Starting date for simulated data
date = datetime(2020, 1, 1, 0, 0)
depth = 0.0
flowrate = 0
voltage = 4.05

# Loop until specified date
while date < datetime(2020, 1, 8):
    print('{0} - flowrate = {1}, depth = {2}, voltage={3}'
          .format(date, flowrate, depth, voltage))

    # Store the transmission in the database
    Transmission.objects.create(timestamp=date, device=device, depth=depth,
                                flowrate=flowrate, voltage=voltage)

    # Allow for a transmission rate change in the middle of the data
    if date > datetime(2020, 1, 4, 11, 59):
        m = 15
        v = 0.0002
    else:
        m = 6
        v = 0.0001

    # Transission interval increment
    date = date + timedelta(minutes=m)

    # Generate random event for the weather
    rand = random()

    # Decrease battery linearly
    voltage -= v

    # 0.02 chance it starts raining
    if flowrate < 1:
        if rand > 0.995:
            flowrate += 1

    # 0.15 chance it starts raining harder
    elif flowrate < 3:
        if rand > 0.85:
            flowrate += 1

    # 0.25 chance it starts raining less hard
    if flowrate > 0 and rand < 0.3:
        flowrate -= 1

    # How water depth changes based on the flow rate
    if flowrate == 0 and depth > 0.01:
        depth -= 0.01
    if flowrate == 1:
        depth += 0.05
    if flowrate == 2:
        depth += 0.1
    if flowrate == 3:
        depth += 0.2
