# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'UsPostalAddress'
        db.create_table(u'postal_address_uspostaladdress', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('country_code', self.gf('django.db.models.fields.CharField')(default='US', max_length=3)),
            ('address_line_1', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('address_line_2', self.gf('django.db.models.fields.CharField')(max_length=128, blank=True)),
            ('city', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('state', self.gf('django.db.models.fields.CharField')(max_length=2)),
            ('zip_code', self.gf('django.db.models.fields.CharField')(max_length=5)),
            ('zip_plus_four', self.gf('django.db.models.fields.CharField')(max_length=4, blank=True)),
        ))
        db.send_create_signal(u'postal_address', ['UsPostalAddress'])


    def backwards(self, orm):
        # Deleting model 'UsPostalAddress'
        db.delete_table(u'postal_address_uspostaladdress')


    models = {
        u'postal_address.uspostaladdress': {
            'Meta': {'object_name': 'UsPostalAddress'},
            'address_line_1': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'address_line_2': ('django.db.models.fields.CharField', [], {'max_length': '128', 'blank': 'True'}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'country_code': ('django.db.models.fields.CharField', [], {'default': "'US'", 'max_length': '3'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'zip_code': ('django.db.models.fields.CharField', [], {'max_length': '5'}),
            'zip_plus_four': ('django.db.models.fields.CharField', [], {'max_length': '4', 'blank': 'True'})
        }
    }

    complete_apps = ['postal_address']