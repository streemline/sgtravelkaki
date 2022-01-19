# -*- coding: utf-8 -*-
""" Nearby Scraper API Class """

from html.parser import HTMLParser
from emojicode import EmojiCode
import re
import requests

EMOJICODE = EmojiCode()

class BusInfo(HTMLParser):
    """Bus Info scraping fuctions"""
    def get_bus_info_msg(self, bus_no):
        """Scrap from www.transitlink.com.sg and return proper data set"""
        url = 'http://www.transitlink.com.sg/eservice/eguide/service_route.php?service=' + bus_no
        res = requests.get(url)
        self.reset_variable()
        self.feed(res.text)
        return self.format_data_set(bus_no)

    def format_data_set(self, bus_no):
        """Return formatted bus info message"""
        first_route = self.data_set['first_route']
        second_route = self.data_set['second_route']
        msg = EMOJICODE.bus() + ' *' + bus_no + '*\n\n'
        msg += EMOJICODE.office() + ' Company: ' +  self.data_set['company'] + '\n\n'
        
        msg += EMOJICODE.busstop() + ' From ' + first_route['int_name'] + '\n'
        msg += '- Weekday first bus : ' + first_route['wd_first_bus'] + '\n'
        msg += '- Weekday last bus : ' + first_route['wd_last_bus'] + '\n'
        msg += '- Saturday first bus : ' + first_route['sat_first_bus'] + '\n'
        msg += '- Saturday last bus : ' + first_route['sat_last_bus'] + '\n'
        msg += '- Sunday/P.Hs first bus : ' + first_route['sun_first_bus'] + '\n'
        msg += '- Sunday/P.Hs last bus : ' + first_route['sun_last_bus'] + '\n\n'

        msg += EMOJICODE.busstop() + ' From ' + second_route['int_name'] + '\n'
        msg += '- Weekday first bus : ' + second_route['wd_first_bus'] + '\n'
        msg += '- Weekday last bus : ' + second_route['wd_last_bus'] + '\n'
        msg += '- Saturday first bus : ' + second_route['sat_first_bus'] + '\n'
        msg += '- Saturday last bus : ' + second_route['sat_last_bus'] + '\n'
        msg += '- Sunday/P.Hs first bus : ' + second_route['sun_first_bus'] + '\n'
        msg += '- Sunday/P.Hs last bus : ' + second_route['sun_last_bus']
        return msg


    def reset_variable(self):
        """Set variables"""
        self.first_route = False
        self.second_route = False
        self.data_set = {
            'company': '',
            'first_route': {
                'int_name': '',
                'wd_first_bus': '',
                'wd_last_bus': '',
                'sat_first_bus': '',
                'sat_last_bus': '',
                'sun_first_bus': '',
                'sun_last_bus': ''
            },
            'second_route':{
                'int_name': '',
                'wd_first_bus': '',
                'wd_last_bus': '',
                'sat_first_bus': '',
                'sat_last_bus': '',
                'sun_first_bus': '',
                'sun_last_bus': ''
            }
        }
        return True

    def handle_starttag(self, tag, attrs):
        """HTMLParser starttag function"""
        if (
            tag == 'td'
            and len(attrs) == 1
            and attrs[0][0] == 'width'
            and attrs[0][1] == '20%'
        ):
            if self.first_route is False:
                self.first_route = True
            elif self.second_route is False:
                self.second_route = True

    def handle_data(self, data):
        """HTMLParser handle_data function"""
        if data in [
            'SBS Transit',
            'Tower Transit',
            'Go-Ahead Singapore',
            'SMRT Buses',
        ]:
            self.data_set['company'] = data
        elif self.first_route is True and self.data_set['first_route']['int_name'] == '':
            if re.search('[a-zA-Z]+', data) != None:
                self.data_set['first_route']['int_name'] = data
            else:
                self.first_route = False
        elif self.second_route is True and self.data_set['second_route']['int_name'] == '':
            if re.search('[a-zA-Z]+', data) is None:
                self.second_route = False
            else:
                self.data_set['second_route']['int_name'] = data
        elif data == '-':
            self.set_bus_timing(data)
        elif len(data) == 4:
            try:
                int(data)
                self.set_bus_timing(data)
            except ValueError:
                return
    
    def set_bus_timing(self, data):
        """Set timing to dataset"""
        #first route timing
        if self.data_set['first_route']['wd_first_bus'] == '':
            self.data_set['first_route']['wd_first_bus'] = data
        elif self.data_set['first_route']['wd_last_bus'] == '':
            self.data_set['first_route']['wd_last_bus'] = data
        elif self.data_set['first_route']['sat_first_bus'] == '':
            self.data_set['first_route']['sat_first_bus'] = data
        elif self.data_set['first_route']['sat_last_bus'] == '':
            self.data_set['first_route']['sat_last_bus'] = data
        elif self.data_set['first_route']['sun_first_bus'] == '':
            self.data_set['first_route']['sun_first_bus'] = data
        elif self.data_set['first_route']['sun_last_bus'] == '':
            self.data_set['first_route']['sun_last_bus'] = data

        #second route timing
        elif self.data_set['second_route']['wd_first_bus'] == '':
            self.data_set['second_route']['wd_first_bus'] = data
        elif self.data_set['second_route']['wd_last_bus'] == '':
            self.data_set['second_route']['wd_last_bus'] = data
        elif self.data_set['second_route']['sat_first_bus'] == '':
            self.data_set['second_route']['sat_first_bus'] = data
        elif self.data_set['second_route']['sat_last_bus'] == '':
            self.data_set['second_route']['sat_last_bus'] = data
        elif self.data_set['second_route']['sun_first_bus'] == '':
            self.data_set['second_route']['sun_first_bus'] = data
        elif self.data_set['second_route']['sun_last_bus'] == '':
            self.data_set['second_route']['sun_last_bus'] = data
