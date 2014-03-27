# -*- coding: utf-8 -*-
from django.shortcuts import render
from barylka_django.web.models import *

from django.db.models import Sum, Min, Count

def index(request):

    c = {}
    c["total"] = Donation.objects.aggregate(Sum('value'))["value__sum"]-80000
    c["procent_zapelnienia"] = float("%.2f" % ((c["total"]/float(164000))*100))

    c["rank"] = Donation.objects.values("donor", "donor__blood_type").annotate(total=Sum("value")).order_by("-total")

    c["last"] = DonationEntry.objects.all().order_by("-date")[:5]

    for e in c["last"]:
        e.total = Donation.objects.filter(entry=e).values("entry").annotate(total=Sum("value"))[0]["total"]

    c["new_users"] = Donation.objects.values("donor").annotate(join_date=Min("date")).order_by("-join_date")[:5]

    c["minirank"]=[]
    for blood_type in ["A-", "A+", "B-", "B+", "0-", "0+", "AB-", "AB+"]:
        c["minirank"].append(
                (
                    blood_type,
                    Donation.objects.values("donor", "donor__blood_type").filter(donor__blood_type=blood_type).annotate(total=Sum("value")).order_by("-total")[:5]
                )
            )

    c["genderrank"]=[]
    for gender, gender_pl in [("M", u"Mężczyźni"), ("F", u"Kobiety")]:
        c["genderrank"].append((gender_pl, Donation.objects.values("donor", "donor__gender", "donor__blood_type").filter(
            donor__gender=gender).annotate(total=Sum("value")).order_by("-total")[:5]))


    c["all_users"]=User.objects.all().order_by("name").values()
    c["sp_user"] = get_user_data("noisy")

    return render(request, "index.html", c)


def rank(request):
    c = {}
    total = Donation.objects.aggregate(Sum('value'))
    c["procent_zapelnienia"] = float("%.2f" % ((total["value__sum"]/float(164000))*100))

    rank = Donation.objects.values("donor", "donor__blood_type").annotate(total=Sum("value")).order_by("-total")
    rank = [rank[x:x+20] for x in range(0, len(rank),20)]
    c["rank"] = [rank[x:x+3] for x in range(0, len(rank),3)]

    rr={}
    user_stat={}
    for type, ml in DONATION_TYPE:
        rr["type"] = Donation.objects.filter(type=type).values("donor").annotate(**{"total_"+type:Sum("value")}).order_by("-total_"+type)
        for dic in rr["type"]:
            if dic["donor"] not in user_stat:
                user_stat[dic["donor"]]={}

            user_stat[dic["donor"]]["total_"+type] = dic["total_"+type]

    for nick in user_stat.keys():
        for type, ml in DONATION_TYPE:
            if "total_"+type not in user_stat[nick]:
                user_stat[nick]["total_"+type]=0

    c["user_stat"] = user_stat

    c["total_by_type"] = {"max":0}
    for type, ml in DONATION_TYPE:
        c["total_by_type"][type] = Donation.objects.filter(type=type).values("donor", "value").annotate(total=Sum("value")).order_by("-total")[0]["total"]
        if c["total_by_type"][type] > c["total_by_type"]["max"]:
            c["total_by_type"]["max"] = c["total_by_type"][type]

    return render(request, "ranking.html", c)

def get_user_data(user_name):

    d = Donation.objects.values("donor", "donor__name").filter(donor__name=user_name)
    c = d.annotate(total=Sum("value"))[0]
    c.update(User.objects.filter(name=user_name).values()[0])
    c["donations"] = d.values().reverse()

    for type, ml in DONATION_TYPE:
        dic = Donation.objects.filter(type=type, donor=user_name).values("donor").annotate(**{"total_"+type:Sum("value")}).order_by("-total_"+type)
        if dic:
            c["total_"+type] = dic[0]["total_"+type]

    c["donation_type_tr"]={"Blood":u"krew","Platelets":u"płytki","Plasma":u"osocze",}

    return c

def user(request, user_name):
    c = get_user_data(user_name)
    c["join_date"] = Donation.objects.filter(donor=user_name).values("donor").annotate(join_date=Min("date"))[0]["join_date"]
    return render(request, "user.html", c)
