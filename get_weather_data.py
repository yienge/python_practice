#!/usr/bin/python
# -*- coding: utf-8 -*-
import requests
import xml.etree.ElementTree as ET


class get_weather_data(object):
    """
    get weather data from http://opendata.cwb.gov.tw
    """
    def __init__(self):
        self.get_data()
        self.process_xml_data()

    def get_data(self):
        weather_per_hour = requests.get('http://opendata.cwb.gov.tw/opendata/MFC/F-C0032-001.xml')
        # weather_helper_via_city = requests.get('http://opendata.cwb.gov.tw/opendata/MFC/F-C0032-009.xml')
        # weather_in_2_days_via_town = requests.get('http://opendata.cwb.gov.tw/opendata/MFC/F-D0047-005.xml')
        # weather_in_7_days_via_town = requests.get('http://opendata.cwb.gov.tw/opendata/MFC/F-D0047-007.xml')
        data_raw_content = weather_per_hour.text
        data_encode = weather_per_hour.encoding
        self.data_content = data_raw_content.encode(data_encode)

    def process_xml_data(self):
        root = ET.fromstring(self.data_content)

        for county in root.iter('location'):
            print '=======', county[0].text, '======='
            time = []
            wx = []
            maxt = []
            ci = []

            for wx_node in county.iter('Wx'):
                for time_node in wx_node.findall('time'):
                    time.append([time_node.attrib['start'], time_node.attrib['end']])
                    wx.append(time_node.find('text').text)

            for maxt_node in county.iter('MaxT'):
                for time_node in maxt_node.findall('time'):
                    value_node = time_node.find('value')
                    maxt.append(value_node.text)

            for ci_node in county.iter('CI'):
                for time_node in ci_node.findall('time'):
                    text_node = time_node.find('text')
                    ci.append(text_node.text)

            for i in range(3):
                print u'時間區段：', time[i]
                print u'天氣：', wx[i]
                print u'最高溫度：', maxt[i]
                print u'體感：', ci[i]

get_data = get_weather_data()
