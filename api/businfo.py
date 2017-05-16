# -*- coding: utf-8 -*-
""" Nearby Scraper API Class """

from html.parser import HTMLParser
import re
import requests


DATASET = {
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

class BusInfo(HTMLParser):
    """Bus Info scraping fuctions"""
    def get_data_set(self, bus_no):
        """Scrap from www.transitlink.com.sg and return proper data set"""
        url = 'http://www.transitlink.com.sg/eservice/eguide/service_route.php?service=' + bus_no
        res = requests.get(url)
        self.reset_variable()
        self.feed(res.text)
        return DATASET

    def reset_variable(self):
        """Set variables"""
        self.first_route = False
        self.second_route = False
        return True

    def handle_starttag(self, tag, attrs):
        """HTMLParser starttag function"""
        if tag == 'td' and len(attrs) == 1:
            if attrs[0][0] == 'width' and attrs[0][1] == '20%':
                if self.first_route is False:
                    self.first_route = True
                elif self.second_route is False:
                    self.second_route = True

    def handle_data(self, data):
        """HTMLParser handle_data function"""
        if data == 'SBS Transit' or data == 'Tower Transit' or data == 'Go-Ahead Singapore':
            DATASET['company'] = data
        elif self.first_route is True and DATASET['first_route']['int_name'] == '':
            if re.search('[a-zA-Z]+', data) != None:
                DATASET['first_route']['int_name'] = data
            else:
                self.first_route = False
        elif self.second_route is True and DATASET['second_route']['int_name'] == '':
            if re.search('[a-zA-Z]+', data) != None:
                DATASET['second_route']['int_name'] = data
            else:
                self.second_route = False
        elif len(data) == 4:
            try:
                test_parse = int(data)

                #first route timing
                if DATASET['first_route']['wd_first_bus'] == '':
                    DATASET['first_route']['wd_first_bus'] = data
                elif DATASET['first_route']['wd_last_bus'] == '':
                    DATASET['first_route']['wd_last_bus'] = data
                elif DATASET['first_route']['sat_first_bus'] == '':
                    DATASET['first_route']['sat_first_bus'] = data
                elif DATASET['first_route']['sat_last_bus'] == '':
                    DATASET['first_route']['sat_last_bus'] = data
                elif DATASET['first_route']['sun_first_bus'] == '':
                    DATASET['first_route']['sun_first_bus'] = data
                elif DATASET['first_route']['sun_last_bus'] == '':
                    DATASET['first_route']['sun_last_bus'] = data

                #second route timing
                elif DATASET['second_route']['wd_first_bus'] == '':
                    DATASET['second_route']['wd_first_bus'] = data
                elif DATASET['second_route']['wd_last_bus'] == '':
                    DATASET['second_route']['wd_last_bus'] = data
                elif DATASET['second_route']['sat_first_bus'] == '':
                    DATASET['second_route']['sat_first_bus'] = data
                elif DATASET['second_route']['sat_last_bus'] == '':
                    DATASET['second_route']['sat_last_bus'] = data
                elif DATASET['second_route']['sun_first_bus'] == '':
                    DATASET['second_route']['sun_first_bus'] = data
                elif DATASET['second_route']['sun_last_bus'] == '':
                    DATASET['second_route']['sun_last_bus'] = data
            except ValueError:
                return
