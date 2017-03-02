#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: set fileencoding=utf8 :

import sys
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
            location + ".json"
        print url
        data = requests.get(url).text

        # llegir-la
        # soup = bs(data, 'lxml')
        jsondata = json.loads(data)
        almanac = jsondata["almanac"]

        resultats = {}
        resultats["maximes"] = {}
        resultats["minimes"] = {}
        resultats["maximes"]["normal"] = almanac["temp_high"]["normal"]["C"]
        resultats["maximes"]["record"] = almanac["temp_high"]["record"]["C"]
        resultats["minimes"]["normal"] = almanac["temp_low"]["normal"]["C"]
        resultats["minimes"]["record"] = almanac["temp_low"]["record"]["C"]

        # retornar resultats
        return resultats


if __name__ == "__main__":
    if not api_key:
        try:
            api_key = sys.argv[1]
        except IndexError:
            key_file = open('api_key', 'r')
            api_key = key_file.read().replace('\n', '')
            print "Must provide api key in code or cmdline arg"

    print api_key

    wc = WeatherClient(api_key)
    result = wc.almanac("Lleida")
    print result
