# -*- coding: utf-8 -*-
from django.db import models
from django.contrib import admin

# Create your models here.
from django.utils.html import format_html
from django.utils.safestring import mark_safe

BLOOD_TYPE = (
    ('A-', 'A Rh-'),
    ('A+', 'A Rh+'),
    ('B-', 'B Rh-'),
    ('B+', 'B Rh+'),
    ('0-', '0 Rh-'),
    ('0+', '0 Rh+'),
    ('AB-', 'AB Rh-'),
    ('AB+', 'AB Rh+'),
)

GENDER_CHOICES = (
    ('M', 'Male'),
    ('F', 'Female'),
)

DONATION_TYPE = (
    ('Blood', 450),
    ('Platelets', 500),
    ('Plasma', 200),
)

class Edition(models.Model):
    number = models.IntegerField(primary_key=True)
    capacity = models.IntegerField()
    start_date = models.DateField()
    end_date = models.DateField(null=True)

admin.site.register(Edition)

class User(models.Model):
    name = models.CharField(max_length=120, primary_key=True)
    corrector = models.BooleanField(default=False)
    blood_type = models.CharField(max_length=3, choices=BLOOD_TYPE, null=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, null=True)

    def __unicode__( self ):
        return u"@{0}".format(self.name)

admin.site.register(User)

from django.contrib.admin.views.main import ChangeList


class SpecialOrderingChangeList(ChangeList):
    def apply_special_ordering(self, queryset):
        order_type, order_by = [self.params.get(param, None) for param in ('ot', 'o')]
        special_ordering = self.model_admin.special_ordering
        if special_ordering and order_type and order_by:
            try:
                order_field = self.list_display[int(order_by)]
                ordering = special_ordering[order_field]
                if order_type == 'desc':
                    ordering = ['-' + field for field in ordering]
                queryset = queryset.order_by(*ordering)
            except IndexError:
                return queryset
            except KeyError:
                return queryset
        return queryset

    def get_query_set(self, request):
        queryset = super(SpecialOrderingChangeList, self).get_query_set(request)
        queryset = self.apply_special_ordering(queryset)
        return queryset


class DonationEntry(models.Model):
    date = models.DateTimeField()
    micro_id = models.IntegerField(primary_key=True)
    author = models.ForeignKey(User, related_name="wrote")
    corrector = models.ForeignKey(User, related_name="corrected", null=True)
    msg = models.CharField(max_length=4098)

    def msg_html(self):
        return format_html(self.msg)

    msg.allow_tags = True

    def date_(self):
        return self.date.strftime(
            "%Y-%m-%d %H:%M:%S"
        ).replace(
            ' ', u'\u00A0'
        ).replace(
            '-', u'\u2011'
        )


class DonationEntryAdmin(admin.ModelAdmin):
    list_display = ['micro_id', 'date', 'date_', 'author', 'msg_html']
    special_ordering = {'date': ('date', 'author'), 'author': ('author', 'date_')}

    def get_changelist(self, request, **kwargs):
        return SpecialOrderingChangeList

admin.site.register(DonationEntry, DonationEntryAdmin)


class Donation(models.Model):
    donor = models.ForeignKey(User, related_name="donate")
    date = models.DateTimeField()
    type = models.CharField(max_length=10, choices=DONATION_TYPE)
    value = models.IntegerField()
    entry = models.ForeignKey(DonationEntry)
    stamp_img_url = models.CharField(max_length=2048, blank=True, null=True)
    barylka_edition = models.IntegerField()

    def date_(self):
        return self.date.strftime(
            "%Y-%m-%d %H:%M:%S"
        ).replace(
            ' ', u'\u00A0'
        ).replace(
            '-', u'\u2011'
        )

    def type_(self):
        return {
            'Blood': u'Krew',
            'Platelets': u'Płytki',
            'Plasma': u'Osocze',
        }[self.type]

    def stamp(self):
        if self.stamp_img_url == '':
            return 'NONE'
        from rfc3987 import parse
        try:
            parse(self.stamp_img_url, rule='IRI')
            return 'OK'
        except ValueError:
            return 'ERROR'


class DonationAdmin(admin.ModelAdmin):
    list_display = ['date', 'date_', 'donor', 'type_', 'value', 'stamp']
    special_ordering = {'date': ('date', 'donor'), 'donor': ('donor', 'date_')}

    def get_changelist(self, request, **kwargs):
        return SpecialOrderingChangeList

admin.site.register(Donation, DonationAdmin)
