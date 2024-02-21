#!/usr/bin/python3
"""
 This script tests cities access from a state
"""
from models import storage
from models.city import City
from models.state import State

"""
 Objects creations
"""
state1 = State(name="California")
print("New state: {}".format(state1))
state1.save()
state_2 = State(name="Arizona")
print("New state: {}".format(state_2))
state_2.save()

city1_1 = City(state_id=state1.id, name="Napa")
print("New city: {} in the state: {}".format(city1_1, state1))
city1_1.save()
city_1_2 = City(state_id=state1.id, name="Sonoma")
print("New city: {} in the state: {}".format(city_1_2, state1))
city_1_2.save()
city_2_1 = City(state_id=state_2.id, name="Page")
print("New city: {} in the state: {}".format(city_2_1, state_2))
city_2_1.save()

"""
 Verification
"""
print("")
states_all = storage.all(State)
for state_id, state in states_all.items():
    for city in state.cities:
        print("Find the city {} in the state {}".format(city, state))
