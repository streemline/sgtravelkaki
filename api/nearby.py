""" Nearby API Class """

from math import cos, asin, sqrt
import json

class Nearby(object):
    """Functions for nearby command"""
    def get_bus_stop_data(self):
        """Load busstop.json file and return bus stop json data"""
        with open('data/busstop.json') as json_data:
            data = json.load(json_data)
            return data

    def distance(self, lat1, lon1, lat2, lon2):
        """Calculate distance between 2 lat lng using Haversine formula"""
        p = 0.017453292519943295
        a = 0.5 - cos((lat2-lat1)*p)/2 + cos(lat1*p)*cos(lat2*p) * (1-cos((lon2-lon1)*p)) / 2
        return 12742 * asin(sqrt(a))

    def get_nearest_three_bus_stops(self, lat, lng):
        """Return three nearest bus stop list from user current location"""
        bus_stop_data = self.get_bus_stop_data()
        for bus_stop in bus_stop_data:
            dist = self.distance(lat, lng, float(bus_stop['lat']), float(bus_stop['lng']))
            bus_stop['distance'] = dist
        sort_bus_stop_list = sorted(bus_stop_data, key=lambda k: k['distance'])
        top_three_list = [sort_bus_stop_list[0], sort_bus_stop_list[1], sort_bus_stop_list[2]]
        return top_three_list

    def get_nearby_cmd_msg(self, bus_stop_list):
        """Return formatted message of the three nearest bus stop from
        user current location"""
        bus_stop_1 = bus_stop_list[0]
        bus_stop_2 = bus_stop_list[1]
        bus_stop_3 = bus_stop_list[2]
        msg = '*Nearest 3 bus stop from your location* \n\n'
        msg += '1. 🚏 *'+bus_stop_1['no'] + '* - ' + bus_stop_1['name'] + '\n'
        msg += '2. 🚏 *'+bus_stop_2['no'] + '* - ' + bus_stop_2['name'] + '\n'
        msg += '3. 🚏 *'+bus_stop_3['no'] + '* - ' + bus_stop_3['name'] + '\n'
        return msg
