from django.db import models
from django.contrib import admin

# Create your models here.

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

class DonationEntry(models.Model):
    date = models.DateTimeField()
    micro_id = models.IntegerField(primary_key=True)
    author = models.ForeignKey(User, related_name="wrote")
    corrector = models.ForeignKey(User, related_name="corrected", null=True)
    msg = models.CharField(max_length=4098)

    def __unicode__( self ):
        return u"{2} #{3} - {0}, {1}".format(self.author, self.corrector, self.date, self.micro_id)

admin.site.register(DonationEntry)

class Donation(models.Model):
    donor = models.ForeignKey(User, related_name="donate")
    date = models.DateTimeField()
    type = models.CharField(max_length=10, choices=DONATION_TYPE)
    value = models.IntegerField()
    entry = models.ForeignKey(DonationEntry)
    stamp_img_url = models.CharField(max_length=2048, blank=True, null=True)
    barylka_edition = models.IntegerField()

    def __unicode__( self ):
        return u"{0} ml - {1}, {2} - @{3}".format(
            self.value, self.date, self.type, self.entry.author.name
        )

admin.site.register(Donation)
