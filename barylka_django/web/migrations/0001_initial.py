# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Edition'
        db.create_table(u'web_edition', (
            ('number', self.gf('django.db.models.fields.IntegerField')(primary_key=True)),
            ('capacity', self.gf('django.db.models.fields.IntegerField')()),
            ('start_date', self.gf('django.db.models.fields.DateField')()),
            ('end_date', self.gf('django.db.models.fields.DateField')(null=True)),
        ))
        db.send_create_signal(u'web', ['Edition'])

        # Adding model 'User'
        db.create_table(u'web_user', (
            ('name', self.gf('django.db.models.fields.CharField')(max_length=120, primary_key=True)),
            ('corrector', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('blood_type', self.gf('django.db.models.fields.CharField')(max_length=3, null=True)),
            ('gender', self.gf('django.db.models.fields.CharField')(max_length=1, null=True)),
        ))
        db.send_create_signal(u'web', ['User'])

        # Adding model 'DonationEntry'
        db.create_table(u'web_donationentry', (
            ('date', self.gf('django.db.models.fields.DateTimeField')()),
            ('micro_id', self.gf('django.db.models.fields.IntegerField')(primary_key=True)),
            ('author', self.gf('django.db.models.fields.related.ForeignKey')(related_name='wrote', to=orm['web.User'])),
            ('corrector', self.gf('django.db.models.fields.related.ForeignKey')(related_name='corrected', null=True, to=orm['web.User'])),
            ('msg', self.gf('django.db.models.fields.CharField')(max_length=4098)),
        ))
        db.send_create_signal(u'web', ['DonationEntry'])

        # Adding model 'Donation'
        db.create_table(u'web_donation', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('donor', self.gf('django.db.models.fields.related.ForeignKey')(related_name='donate', to=orm['web.User'])),
            ('date', self.gf('django.db.models.fields.DateTimeField')()),
            ('type', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('value', self.gf('django.db.models.fields.IntegerField')()),
            ('entry', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['web.DonationEntry'])),
            ('stamp_img_url', self.gf('django.db.models.fields.CharField')(max_length=2048)),
            ('barylka_edition', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal(u'web', ['Donation'])


    def backwards(self, orm):
        # Deleting model 'Edition'
        db.delete_table(u'web_edition')

        # Deleting model 'User'
        db.delete_table(u'web_user')

        # Deleting model 'DonationEntry'
        db.delete_table(u'web_donationentry')

        # Deleting model 'Donation'
        db.delete_table(u'web_donation')


    models = {
        u'web.donation': {
            'Meta': {'object_name': 'Donation'},
            'barylka_edition': ('django.db.models.fields.IntegerField', [], {}),
            'date': ('django.db.models.fields.DateTimeField', [], {}),
            'donor': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'donate'", 'to': u"orm['web.User']"}),
            'entry': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['web.DonationEntry']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'stamp_img_url': ('django.db.models.fields.CharField', [], {'max_length': '2048'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'value': ('django.db.models.fields.IntegerField', [], {})
        },
        u'web.donationentry': {
            'Meta': {'object_name': 'DonationEntry'},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'wrote'", 'to': u"orm['web.User']"}),
            'corrector': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'corrected'", 'null': 'True', 'to': u"orm['web.User']"}),
            'date': ('django.db.models.fields.DateTimeField', [], {}),
            'micro_id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'msg': ('django.db.models.fields.CharField', [], {'max_length': '4098'})
        },
        u'web.edition': {
            'Meta': {'object_name': 'Edition'},
            'capacity': ('django.db.models.fields.IntegerField', [], {}),
            'end_date': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'number': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'start_date': ('django.db.models.fields.DateField', [], {})
        },
        u'web.user': {
            'Meta': {'object_name': 'User'},
            'blood_type': ('django.db.models.fields.CharField', [], {'max_length': '3', 'null': 'True'}),
            'corrector': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'gender': ('django.db.models.fields.CharField', [], {'max_length': '1', 'null': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '120', 'primary_key': 'True'})
        }
    }

    complete_apps = ['web']