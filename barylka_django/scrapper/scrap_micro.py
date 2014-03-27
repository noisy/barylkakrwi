# -*- coding: utf-8 -*-
import wykop
import re
from barylka_django.web.models import *

def scrap(test):
    api = wykop.WykopAPI(appkey="", secretkey="", login="", password="")

    entries = api.tag("barylkakrwi")

    for entry in entries['items']:

        if not DonationEntry.objects.filter(micro_id=entry.id):
            try:
                body = entry.body.replace(" ", "")
                g = re.match('(\d+)\s*-\s*(\d+)\s*=\s*(\d+)', entry.body)
                if g:
                    base = int(g.group(1))
                    donation = int(g.group(2))
                    result = int(g.group(3))

                    print "%d - %d = %d" % (base, donation, result)

                    if base - donation != result:
                        print "Error!!"

                    type = [type for type, ml in DONATION_TYPE if ml == donation][0]

                    user, created = User.objects.get_or_create(name=entry.author)
                    de = DonationEntry.objects.create(micro_id=entry.id, date=entry.date, author=user, msg=entry.body)
                    Donation.objects.create(donor=user, date=entry.date, type=type, value=donation, entry=de, barylka_edition=1)



            except:
                import sys, traceback
                traceback.print_exc()

    from django.http import HttpResponse
    return HttpResponse("ok")


def import_data(test):
    import urllib
    import os.path
    api = wykop.WykopAPI(appkey="", secretkey="", login="", password="")

    data={}

    with open("/home/work/podsumowanie.csv") as f:
        i=1
        for line in f:
            line=line.split(",")
            entry_date = line[0]
            nick = line[2].strip()
            url = line[14]

            new_data={
                "krew": line[3] if line[3] else 0,
                "plytki": line[4] if line[4] else 0,
                "osocze": line[5] if line[5] else 0,
            }

            if "http://www.wykop.pl/" in url:

                id = url.split("/")[4]
                """"
                if not os.path.isfile("/tmp/barylka/" + str(id)+".jpg"):
                    try:

                        entry = api.get_entry(id)
                        if entry["embed"]:
                            print entry.embed.preview
                            urllib.urlretrieve(entry.embed.preview, "/tmp/barylka/" + str(id)+".jpg")
                    except wykop.EntryDoesNotExistError:
                        print "wykop.EntryDoesNotExistError: Wpis nie istnieje lub zostal usuniety - " + id
                """

                if nick not in data:
                    data[nick] = {}
                    data[nick]["razem"] = 0



                pl_en={"krew":"Blood", "plytki":"Platelets", "osocze":"Plasma"}

                for skladnik, ml in [("krew", 450), ("plytki", 500), ("osocze", 200)]:
                    if skladnik not in data[nick]:
                        data[nick][skladnik] = 0
                        data[nick][skladnik+"_ml"] = 0


                    if (new_data[skladnik] != 0):
                        user, creaded = User.objects.get_or_create(name=nick)

                        e_body=""
                        try:
                            e_body = api.get_entry(id).body
                        except wykop.EntryDoesNotExistError:
                            e_body = ""
                        db_entry, creaded = DonationEntry.objects.get_or_create(date=entry_date, micro_id=id, author=user,
                                                                msg=e_body)

                        for i in range(int(float(new_data[skladnik]))):
                            Donation.objects.create(donor=user, date=entry_date, type=pl_en[skladnik], value=ml,
                                                    entry = db_entry, barylka_edition=1)


                    data[nick][skladnik] += float(new_data[skladnik])
                    data[nick][skladnik+"_ml"] += float(new_data[skladnik]) * ml
                    data[nick]["razem"] += float(new_data[skladnik]) * ml


    male=0
    female=0
    no_info=0

    pinfo={
        "author_group":{
            0:0,
            1:0,
            2:0,
            5:0,
            1001:0,
            1002:0,
            2001:0,
        },
    }

    maxrank=999999999
    maxrank_nick=""
    dont_want_pm=[]
    group_info=0

    group_info_group = {}


    for nick in data.keys():
        try:
            profile = api.get_profile(nick)
            blood_type=None
            sex=None
            if profile.sex == 'male':
                sex="M"
                male+=1
            elif profile.sex == 'female':
                sex="F"
                female+=1
            else:
                no_info+=1
            #print nick + " is " + profile.sex

            #print "Sending to " + nick
            try:

                con_list = api.get_conversation(nick)
                if not con_list:
                    pass
                    #print nick + " send now!"
                    #print nick + " TODO"
                    """
                    api.send_message(nick, u"Hej! Jestem malutkim botem napisanym przez noisy'ego, który dopytuje wszystkich "
                                   u"uczestnikow #barylkakrwi o grupę krwi :) Byłbym niezwykle wdzięczny, gdybyś mógł mi"
                                   u"odpowiedzieć na pytanie jaką grupę krwi posiadasz?\n\n"
                                   u"Ponieważ jestem dość głupim botem, to zrozumiem odpowiedź tylko wtedy, "
                                   u"jeżeli wpiszesz dokładnie swoją grupę krwi, czyli jedną z tych:"
                                   u"odpowiednio: A-, A+, B-, B+, 0-, 0+, AB-, AB+ - nie wpisuj proszę żadnych innych "
                                   u"kombinacji np. 0 RH-, bo nie połapię się ;)\n\n"
                                   u"Z góry dziękuję :)")
                    """

                else:

                    msg_sent=False

                    for conv in con_list:
                        if "A-, A+, B-, B+, 0-, 0+, AB-, AB+" in conv.body:
                            #print nick + " sent"
                            msg_sent=True
                            continue

                        if conv.body.replace(" ", "") in ["A-", "A+", "B-", "B+", "0-", "0+", "AB-", "AB+"]:
                            print nick + ", " + conv.body
                            blood_type = conv.body.replace(" ", "")

                            group_info+=1
                            if conv.body.replace(" ", "") not in group_info_group:
                                group_info_group[conv.body.replace(" ", "")]=0

                            group_info_group[conv.body.replace(" ", "")] += 1
                            data[nick]["grupa"]=conv.body.replace(" ", "")

                            break



                    else:
                        pass
                        """
                        print nick + " send now!"
                        api.send_message(nick, u"Hej! Jestem malutkim botem napisanym przez noisy'ego, który dopytuje wszystkich "
                                   u"uczestnikow #barylkakrwi o grupę krwi :) Byłbym niezwykle wdzięczny, gdybyś mógł mi"
                                   u"odpowiedzieć na pytanie jaką grupę krwi posiadasz?\n\n"
                                   u"Ponieważ jestem dość głupim botem, to zrozumiem odpowiedź tylko wtedy, "
                                   u"jeżeli wpiszesz dokładnie swoją grupę krwi, czyli jedną z tych:"
                                   u"odpowiednio: A-, A+, B-, B+, 0-, 0+, AB-, AB+ - nie wpisuj proszę żadnych innych "
                                   u"kombinacji np. 0 RH-, bo nie połapię się ;)\n\n"
                                   u"Z góry dziękuję :)")
                        """

            except wykop.UserDontWantToGetPMError:
                print u"wykop.WykopAPIError: %s nie chce odbierać wiadomości prywatnych" % nick
                dont_want_pm.append(nick)
            except:
                import sys, traceback
                traceback.print_exc()

            pinfo["author_group"][profile.author_group] += 1

            try:
                r = int(profile.rank)
                if r < maxrank and r != 0:
                    maxrank = r
                    maxrank_nick = nick
            except ValueError:
                #print "Not in rank"
                pass

            print nick, blood_type, sex
            user, created = User.objects.get_or_create(name=nick)
            user.gender = sex
            user.blood_type = blood_type
            user.save()

            #print profile.avatar_big
            #urllib.urlretrieve(profile.avatar_big, "avatars/"+nick+".jpg")
        except wykop.UserDoesNotExistError:
            import sys, traceback
            traceback.print_exc()


    print "male: " + str(male)
    print "female: " + str(female)
    print "no_info: " + str(no_info)
    print ""

    print "Najwyższą pozycje w rankingu ma %s - %d\n" % (maxrank_nick, maxrank)

    print "W akcji brało udział:"
    print "%s - zielonych" % pinfo["author_group"][0]
    print "%s - pomarańczowych" % pinfo["author_group"][1]
    print "%s - bordowych" % pinfo["author_group"][2]
    print "%s - administratorow" % pinfo["author_group"][5]
    print "%s - obecnie zbanowanych" % pinfo["author_group"][1001]
    print "%s - osob, ktore usuneły konta" % pinfo["author_group"][1002]
    print "%s - klientow (niebieskich)\n" % pinfo["author_group"][2001]

    print "Użytkownicy, którzy nie chcą otrzymywać prywatnych wiadomości (%d):" % len(dont_want_pm)
    print "@" + ", @".join(dont_want_pm)


    gr_sr={}
    gr_max={}
    for gr in ["A-", "A+", "B-", "B+", "0-", "0+", "AB-", "AB+"]:
        gr_sr[gr]=[]
        gr_max[gr]={"wartosc":0, "kto":[]}


    for nick in data.keys():
        if "grupa" in data[nick] and data[nick]["grupa"] in ["A-", "A+", "B-", "B+", "0-", "0+", "AB-", "AB+"]:
            gr = data[nick]["grupa"]
            gr_sr[gr].append(data[nick]["razem"])

            if gr_max[gr]["wartosc"] < data[nick]["razem"]:
                gr_max[gr]["wartosc"] = data[nick]["razem"]
                gr_max[gr]["kto"] = [nick]
            elif gr_max[gr]["wartosc"] == data[nick]["razem"]:
                gr_max[gr]["kto"].append(nick)


    print "\n"
    print "Mamy informacje o grupie krwi od %d osób\n" % group_info

    print "Liczba osób biorących udział w akcji z daną grupą krwi"
    for gr in ["A-", "A+", "B-", "B+", "0-", "0+", "AB-", "AB+"]:
        print gr + " - " + str(group_info_group[gr])

    print "Najlepsze wyniki:\n"
    for gr in ["A-", "A+", "B-", "B+", "0-", "0+", "AB-", "AB+"]:
        if len(gr_sr[gr]) != 0:
            v = sum(gr_sr[gr])/float(len(gr_sr[gr]))
            print "Uzytkownicy z grupa %s oddali srednio %.3f, najwięcej (%d ml) odda%s: %s" % (gr, v, gr_max[gr][
                "wartosc"] , "l" if len(gr_max[gr]["kto"]) == 1 else "li", ", ".join(gr_max[gr]["kto"]))



    #print str(gr_max)



    results = [(nick, data[nick]["razem"], data[nick]) for nick in data.keys()]

    sorted_by_second = sorted(results, key=lambda tup: tup[1], reverse=True)

    i=1
    for record in sorted_by_second:
        print "%d. @%s - %d ml " % (i, record[0], record[1])
        i+=1


    print "Raking według grupy krwi:\n"
    for gr in ["A-", "A+", "B-", "B+", "0-", "0+", "AB-", "AB+"]:
        print "\nGrupa %s:" % gr
        results = [(nick, data[nick]["razem"], data[nick]) for nick in data.keys() if "grupa" in data[nick] and data[nick]["grupa"] == gr]

        sorted_by_second = sorted(results, key=lambda tup: tup[1], reverse=True)

        i=1
        for record in sorted_by_second:
            print "%d. @%s - %d ml " % (i, record[0], record[1])
            i+=1

    print "Mamy informacje o grupie krwi od %d osób\n" % group_info

    from django.http import HttpResponse
    return HttpResponse("ok")
