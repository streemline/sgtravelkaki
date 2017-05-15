""" Bus API Class """

from datetime import datetime
import time
import json
import requests
from dateutil.parser import parse

API_KEY = ""

class BusApi(object):
    """Bus arrival API"""
    def get_bus_arrival_json(self, bus_stop_id):
        """Call http get request and return JSON data"""
        url = 'http://datamall2.mytransport.sg/ltaodataservice/BusArrival?BusStopID='
        url += bus_stop_id +'&SST=True'
        headers = {'AccountKey': API_KEY}
        result = requests.get(url, headers=headers)
        res = json.loads(result.text)
        return res

    def get_bus_arrival_msg(self, bus_stop_id, bus_no=''):
        """Return formatted bus arrival message"""
        res = self.get_bus_arrival_json(bus_stop_id)
        got_bus_services = self.check_for_bus_service(res)
        msg = '🚏 *' + res.get('BusStopID') + '* - '
        if got_bus_services:
            bus_detail = self.get_bus_stop_detail(bus_stop_id)
            msg += bus_detail['name'] + "\n\n"
            if bus_no == '':
                for service in res.get('Services'):
                    msg += self.format_bus_arrival_info(service)
            else:
                for service in res.get('Services'):
                    if service.get('ServiceNo') == bus_no:
                        msg += self.format_bus_arrival_info(service)
                        break
        else:
            msg += 'No bus services found. \n\n'
        formatted_now = 'Updated on ' + datetime.now().strftime("%d %b %Y %I:%M:%S %p")
        msg += formatted_now
        return msg

    def check_for_bus_service(self, res):
        """Check for any bus services at bus stop and return bool"""
        if len(res.get('Services')) is not 0:
            return True
        return False

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

    def format_bus_arrival_info(self, service):
        """Return formatted bus arrival info"""
        msg = '🚍 *' + service.get('ServiceNo') + '*\n'
        now = datetime.now()
        nxt_bus_arrival_str = service.get('NextBus').get('EstimatedArrival')
        sub_bus_arrival_str = service.get('SubsequentBus').get('EstimatedArrival')
        sub_bus_arrival_str3 = service.get('SubsequentBus3').get('EstimatedArrival')
        # Next bus arrival time
        if nxt_bus_arrival_str != "":
            mins = self.get_date_diff_min(now, nxt_bus_arrival_str)
            mins_str = self.get_min_diff_str(mins)
            bus_load = service.get('NextBus').get('Load')
            bus_feature = service.get('NextBus').get('Feature')
            msg += 'Next: ' + mins_str + self.check_bus_load(bus_load)
            msg += self.check_bus_feature(bus_feature) + '\n'
        else:
            msg += 'Next: No ETA \n'
        # Subsequent arrival time
        if sub_bus_arrival_str != "":
            mins = self.get_date_diff_min(now, sub_bus_arrival_str)
            mins_str = self.get_min_diff_str(mins)
            bus_load = service.get('NextBus').get('Load')
            bus_feature = service.get('NextBus').get('Feature')
            msg += 'Sub: ' + mins_str + self.check_bus_load(bus_load)
            msg += self.check_bus_feature(bus_feature) + '\n'
        else:
            msg += 'Sub: No ETA \n'
        # After subsequent arrival time
        if sub_bus_arrival_str3 != "":
            mins = self.get_date_diff_min(now, sub_bus_arrival_str3)
            mins_str = self.get_min_diff_str(mins)
            bus_load = service.get('NextBus').get('Load')
            bus_feature = service.get('NextBus').get('Feature')
            msg += 'After: ' + mins_str + self.check_bus_load(bus_load)
            msg += self.check_bus_feature(bus_feature) + '\n\n'
        else:
            msg += 'After: No ETA \n\n'
        return msg

    def check_bus_load(self, load):
        """Check how pack is the bus"""
        load_emoji = " 😠"
        if load == 'Seats Available':
            load_emoji = " 😁"
        elif load == 'Standing Available':
            load_emoji = " 😓"
        return load_emoji

    def check_bus_feature(self, feature):
        """Check is it wheel chair accessible"""
        feature_emoji = "♿"
        if feature == "":
            feature_emoji = ""
        return feature_emoji

    def get_bus_stop_detail(self, bus_stop_id):
        """Return bus stop details"""
        with open('data/busstop.json') as json_data:
            data = json.load(json_data)
            for bus_stop in data:
                if bus_stop['no'] == bus_stop_id:
                    return bus_stop
