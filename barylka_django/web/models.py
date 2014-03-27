from django.db import models

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

class User(models.Model):
    name = models.CharField(max_length=120, primary_key=True)
    blood_type = models.CharField(max_length=3, choices=BLOOD_TYPE, null=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, null=True)

class DonationEntry(models.Model):
    date = models.DateTimeField()
    micro_id = models.IntegerField(primary_key=True)
    author = models.ForeignKey(User)
    msg = models.CharField(max_length=4098)

class Donation(models.Model):
    donor = models.ForeignKey(User)
    date = models.DateTimeField()
    type = models.CharField(max_length=10, choices=DONATION_TYPE)
    value = models.IntegerField()
    entry = models.ForeignKey(DonationEntry)

