from datetime import datetime, timedelta
from random import random
from webapp.models import Device, Transmission


'''
To run this script, open the server shell and run the following command:
exec(open('sim_data/simulate.py').read())
'''

# Device we are assigining this data to
device = Device.objects.first()

# Starting date for simulated data
date = datetime(2019, 12, 1, 0, 0)
depth = 0.0
flowrate = 0

# Loop through an entire day
while date < datetime(2019, 12, 2):
    # print('{0} - flowrate = {1}, depth = {2}'.format(date, flowrate, depth))

    # Store the transmission in the database
    Transmission.objects.create(timestamp=date, device=device, depth=depth,
                                flowrate=flowrate)

    # Transission interval increment
    date = date + timedelta(minutes=6)

    # Generate random event for the weather
    rand = random()

    # 0.02 chance water starts flowing in harder
    if rand > 0.98 and flowrate < 3:
        flowrate += 1

    # 0.25 chance it water decreases the rate it is flowing in
    if flowrate > 0 and rand < 0.25:
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
