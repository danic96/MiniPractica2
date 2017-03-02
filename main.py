#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: set fileencoding=utf8 :

import sys
import urllib2
from bs4 import BeautifulSoup as bs
import json
import requests

api_key = None


class WeatherClient(object):
    """docstring foe WeatherClient."""

    url_base = "http://api.wunderground.com/api/"
    url_service = {
        "almanac": "/almanac/q/CA/",
        "hourly": "/hourly/q/CA/"
    }
    def __init__(self, api_key):
        super(WeatherClient, self).__init__()
        self.api_key = api_key

    def almanac(self, location):
        # baixar-se la web
        url = self.url_base + self.api_key + self.url_service["almanac"] + \
            location + ".xml"
        print url
        data = requests.get(url).text

        # llegir-la
        soup = bs(data, 'lxml')
        maximes = soup.find("temp_high")
        minimes = soup.find("temp_low")
        normal_maximes = maximes.find("normal").find("c").text
        record_maximes = maximes.find("record").find("c").text

        normal_minimes = minimes.find("normal").find("c").text
        record_minimes = minimes.find("record").find("c").text

        resultats = {}
        resultats["maximes"] = {}
        resultats["minimes"] = {}
        resultats["maximes"]["normal"] = normal_maximes
        resultats["maximes"]["record"] = record_maximes
        resultats["minimes"]["normal"] = normal_minimes
        resultats["minimes"]["record"] = record_minimes

        # retornar resultats
        return resultats


if __name__ == "__main__":
    if not api_key:
        try:
            api_key = sys.argv[1]
        except IndexError:
            key_file = open('api_key', 'r')
            api_key = key_file.read()
            print "API Key must be in CLI option"

    print api_key
    """
    wc = WeatherClient(api_key)
    result = wc.almanac("Lleida")
    print result
    """
