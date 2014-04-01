# -*- coding: utf-8 -*-
"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase

from .micro_crawler import *

class MicroCrawlerTest(TestCase):

    def run_read_entry(self, tpl_list):

        donations=[]

        for body, result in tpl_list:
            read_entry(body, donations)
            self.assertEqual(donations, result)

    def test_read_entry_1(self):
        arg = [
                (
                    "325950 - 950 = 325000",
                    [{"value":950}]
                ),
                (
                    """Będzie możliwe rozdzielenie wpisów i przydzielenie im stosownych dat.

                    325950 - 450 - 500 = 325000
                    daty: 2014-03-09, 2014-03-28

                    #korekta

                    jeżeli wartości donacji są typowe (450-krew, 500-plytki, 200-osocze), automatycznie zostanie przydzielony odpowiedni typ donacji.""",
                    [{"value":450, "date":"2014-03-09", "type":"Blood"}, {"value":500, "date":"2014-03-28", "type":"Platelets"}]
                ),
            ]
        self.run_read_entry(arg)

    def test_read_entry_2(self):
        arg = [
                (
                    """328000 - 450 = 327550
                    data donacji: 2014-03-01""",
                    [{"value":450, "date":"2014-03-01", "type":"Blood"}]
                ),
            ]
        self.run_read_entry(arg)

    def test_read_entry_3(self):
        arg = [
                (
                    """328000 - 450 = 327550
                    data donacji: 2014-3-1""",
                    [{"value":450, "date":"2014-03-01", "type":"Blood"}]
                ),
            ]
        self.run_read_entry(arg)

    def test_read_entry_4(self):
        arg = [
                (
                    """327550 - 500 = 327050
                    data: 2014.3.5
                    #testowywpis #test""",
                    [{"value":500, "date":"2014-03-05", "type":"Platelets"}]
                ),
            ]
        self.run_read_entry(arg)

    def test_read_entry_5(self):
        arg = [
                (
                    """327050 - 450 - 500 = 326100
                    #testowywpis #test""",
                    [{"value":450, "type":"Blood"}, {"value":500, "type":"Platelets"}]
                ),
                (
                    """daty donacji: 2014-03-07, 2014-03-27
                    #korekta""",
                    [{"value":450, "type":"Blood", "date":"2014-03-07"}, {"value":500, "type":"Platelets", "date":"2014-03-27"}]
                ),
            ]
        self.run_read_entry(arg)

    def test_read_entry_6(self):
        arg = [
                (
                    """326100 - 150 = 325850
                    #testowywpis #test""",
                    [{"value":150}]
                ),
                (
                    """@noisy:
                    326100 - 150 = 325850
                    data: 2014-03-28
                    skladnik: krew
                    #korekta""",
                    [{"value":150, "type":"Blood", "date":"2014-03-28"}]
                ),
                (
                    """@noisy:
                    326100 - 150 = 325950
                    #korekta""",
                    [{"value":150, "type":"Blood", "date":"2014-03-28"}]
                ),
            ]
        self.run_read_entry(arg)

    def test_read_entry_7(self):
        arg = [
                (
                    """325850 - 233 = 325617
                    #testowywpis #test""",
                    [{"value":233}]
                ),
                (
                    u"""@noisy:
                    data: 2014.3.17
                    skladnik: płytki
                    #korekta""",
                    [{"value":233, "type":"Platelets", "date":"2014-03-17"}]
                ),
            ]
        self.run_read_entry(arg)

    def test_read_entry_8(self):
        arg = [
                (
                    """327050 ml - 450 ml - 500 ml = 326100 ml
                    #testowywpis #test""",
                    [{"value":450, "type":"Blood"}, {"value":500, "type":"Platelets"}]
                ),
            ]
        self.run_read_entry(arg)