# -*- coding: utf-8 -*-
"""Street View Module"""
API_KEY = ""


class StreetView(object):
    """Functions for Street View Api from Google"""
    def form_street_view_img_url(self, latlng):
        """Return Street View static image URL"""
        url = 'https://maps.googleapis.com/maps/api/streetview'
        params = '?size=600x400&location=' +latlng + '&key=' + API_KEY
        return url + params

    def get_lat_lng_str(self, bus_stop_detail):
        """Return formatted lat lng string"""
        return bus_stop_detail['lat'] + ',' + bus_stop_detail['lng']
