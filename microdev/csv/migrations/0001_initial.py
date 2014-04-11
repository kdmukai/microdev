# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'CsvImport'
        db.create_table(u'csv_csvimport', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('date_created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
        ))
        db.send_create_signal(u'csv', ['CsvImport'])

        # Adding model 'CsvImportRow'
        db.create_table(u'csv_csvimportrow', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('csv_import', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['csv.CsvImport'])),
            ('_json_data', self.gf('django.db.models.fields.TextField')(db_column='json_data')),
        ))
        db.send_create_signal(u'csv', ['CsvImportRow'])


    def backwards(self, orm):
        # Deleting model 'CsvImport'
        db.delete_table(u'csv_csvimport')

        # Deleting model 'CsvImportRow'
        db.delete_table(u'csv_csvimportrow')


    models = {
        u'csv.csvimport': {
            'Meta': {'object_name': 'CsvImport'},
            'date_created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'csv.csvimportrow': {
            'Meta': {'object_name': 'CsvImportRow'},
            '_json_data': ('django.db.models.fields.TextField', [], {'db_column': "'json_data'"}),
            'csv_import': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['csv.CsvImport']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        }
    }

    complete_apps = ['csv']