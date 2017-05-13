''' Bus API Class '''

from datetime import datetime
import time
import json
import requests
from dateutil.parser import parse

API_KEY = ""

class BusApi(object):
    """Bus API methods"""
    def get_date_diff_min(self, now, bus_arrival_str):
        """Return mins diffence of two dates"""
        bus_arrival = parse(bus_arrival_str)
        d1_ts = time.mktime(now.timetuple())
        d2_ts = time.mktime(bus_arrival.timetuple())
        mins = int(d2_ts-d1_ts) / 60
        return int(mins)

    def get_min_diff_str(self, mins):
        """Check time left and return as string"""
        if mins > 1:
            mins_str = str(mins) + ' mins'
        elif mins is 1:
            mins_str = str(mins) + ' min'
        else:
            mins_str = 'Arriving'
        return mins_str

    def check_for_bus_service(self, res):
        """Check for any bus services at bus stop and return bool"""
        if len(res.get('Services')) is not 0:
            return True
        return False

    def get_bus_arrival_json(self, bus_stop_id):
        """Call http get request and return JSON data"""
        url = 'http://datamall2.mytransport.sg/ltaodataservice/BusArrival?BusStopID='
        url += bus_stop_id +'&SST=True'
        headers = {'AccountKey': API_KEY}
        result = requests.get(url, headers=headers)
        res = json.loads(result.text)
        return res

    def get_bus_arrival_msg(self, bus_stop_id):
        """Return formatted bus arrival message"""
        res = self.get_bus_arrival_json(bus_stop_id)
        got_bus_services = self.check_for_bus_service(res)
        msg = 'Bus Stop: ' + res.get('BusStopID') + '\n\n'
        if got_bus_services:
            for service in res.get('Services'):
                msg += '' + service.get('ServiceNo') + '\n'
                now = datetime.now()
                nxt_bus_arrival_str = service.get('NextBus').get('EstimatedArrival')
                sub_bus_arrival_str = service.get('SubsequentBus').get('EstimatedArrival')
                sub_bus_arrival_str3 = service.get('SubsequentBus3').get('EstimatedArrival')
                # Next bus arrival time
                if nxt_bus_arrival_str != "":
                    diff_nxt_bus_mins = self.get_date_diff_min(now, nxt_bus_arrival_str)
                    mins = self.get_min_diff_str(diff_nxt_bus_mins)
                    msg += 'Next: ' + mins + '\n'
                else:
                    msg += 'Next: No ETA \n'
                # Subsequent arrival time
                if sub_bus_arrival_str != "":
                    diff_sub_bus_mins = self.get_date_diff_min(now, sub_bus_arrival_str)
                    mins = self.get_min_diff_str(diff_sub_bus_mins)
                    msg += 'Sub: ' + mins + '\n'
                else:
                    msg += 'Sub: No ETA \n'
                # After subsequent arrival time
                if sub_bus_arrival_str3 != "":
                    diff_sub_bus3_mins = self.get_date_diff_min(now, sub_bus_arrival_str3)
                    mins = self.get_min_diff_str(diff_sub_bus3_mins)
                    msg += 'After: ' + mins + '\n'
                else:
                    msg += 'After: No ETA \n'
        else:
            msg += 'No bus services found.'
        return msg
