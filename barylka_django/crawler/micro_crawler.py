# -*- coding: utf-8 -*-
import os
import re
import wykop
from barylka_django.web.models import *
from django.db.models import DateField
from unidecode import unidecode

def read_entry(body, donations):
    body = unidecode(body.lower())

    equation = re.search('(\d+)(?:\s*ml)*((?:\s*-\s*\d+(?:\s*ml)*)*)\s*=\s*(\d+)(?:\s*ml)*', body, re.MULTILINE|re.DOTALL)

    dates = re.search('dat[ay](?: donacji)?:\s*(\d{4}[-\.]\d{1,2}[-\.]\d{1,2}(?:\s*,\s*\d{4}[-\.]\d{1,2}[-\.]\d{1,2})*)', body, re.MULTILINE|re.DOTALL)

    types = re.search('skladniki?:\s*((?:krew|plytki|osocze)(?:\s*,\s*(?:krew|plytki|osocze))*)', body, re.MULTILINE|re.DOTALL)

    if equation:
        base = int(equation.group(1))
        ds = equation.group(2).replace("ml", "").strip("- ").split("-")
        donation_values = [int(dv.strip()) for dv in ds]
        result = int(equation.group(3))

        print "%d - %d = %d" % (base, sum(donation_values), result)

        if base - sum(donation_values) != result:
            print "Error"

        if not donations:
            for dv in donation_values:
                donations.append({"value":dv})
        else:
            for dv, i in zip(donation_values, range(len(donation_values))):
                if len(donations) <= i:
                    donations.append({"value":dv})
                else:
                    donations[i]["value"] = dv

        for donation in donations:
            for type, ml in DONATION_TYPE:
                if donation["value"] == ml:
                    donation["type"] = type

    if dates:
        donation_dates = dates.group(1).split(",")
        for date, i in zip(donation_dates, range(len(donation_dates))):
            date = date.replace(".", "-")
            donations[i]["date"] = str(DateField().to_python(date.strip()))

    if types:
        trl = {"krew":"Blood", "plytki":"Platelets", "osocze":"Plasma"}
        donation_types = types.group(1).split(",")
        for type, i in zip(donation_types, range(len(donation_types))):
            donations[i]["type"] = trl[type.strip()]

    for donation in donations:
        print str(donation)



def crawl(test):

    api = wykop.WykopAPI(appkey=os.environ['BARYLKA_WYKOP_API_KEY'], secretkey=os.environ['BARYLKA_WYKOP_SECRET_KEY'],
                         login=os.environ['BARYLKA_WYKOP_SECRET_KEY'], accountkey=os.environ['BARYLKA_WYKOP_SECRET_KEY'])

    entries = api.tag("testowywpis")

    for entry in reversed(entries['items']):

        if not DonationEntry.objects.filter(micro_id=entry.id):
            try:
                donations=[]

                read_entry(entry.body, donations)


                for donation in donations:
                    print str(donation)

                for comment in entry.comments:
                    if '#korekta' in comment.body:
                        read_entry(comment.body, donations)

                        for donation in donations:
                            print str(donation)

                """
                user, created = User.objects.get_or_create(name=entry.author)
                de = DonationEntry.objects.create(micro_id=entry.id, date=entry.date, author=user, msg=entry.body)

                for donation in donations:

                    type = [type for type, ml in DONATION_TYPE if ml == donation][0]
                    Donation.objects.create(donor=user, date=entry.date, type=type, value=donation, entry=de, barylka_edition=1)
                """
                print entry.body
                for donation in donations:
                    print str(donation)


            except:
                import sys, traceback
                traceback.print_exc()

    from django.http import HttpResponse
    return HttpResponse("ok")