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
    web_type = ".json"
    url_service = {
        "almanac": "/almanac/q/CA/",
        "hourly": "/hourly/q/CA/",
        "astronomy": "/astronomy/q/CA/"
    }

    def __init__(self, api_key):
        """Inicialitzar la clau."""
        super(WeatherClient, self).__init__()
        self.api_key = api_key

    def requestData(self, location, url_service_name):
        """Baixar-se la web."""
        url = self.url_base + self.api_key + \
            self.url_service[url_service_name] + \
            location + self.web_type

        return requests.get(url).text

    def hourly(self, location):
        u"""Baixar-se la informació de hourly."""
        data = self.requestData(location, "hourly")

        jsondata = json.loads(data)["hourly_forecast"]
        resultat = []
        for date in jsondata:

            resultat.append(date["FCTTIME"]["pretty"])
            resultat.append("  Temperature-> " + date["temp"]["metric"] +
                            " ºC".decode("utf-8"))
            resultat.append("  Condition-> " + date["condition"])
            resultat.append("  Windspeed-> " + date["wspd"]["metric"] +
                            " Km/h")
            resultat.append("  Humidity-> " + date["humidity"] + " %")
            resultat.append("  Pressure-> " + date["mslp"]["metric"] + " hPa")

        return resultat

    def almanac(self, location):
        u"""Baixar-se la informació de 'almanac'."""
        data = self.requestData(location, "almanac")

        # llegir-la
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

    wc = WeatherClient(api_key)

    result = wc.hourly("Lleida")
    for linea in result:
        print linea
