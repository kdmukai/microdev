# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'CsvImport._column_headers'
        db.add_column(u'csv_csvimport', '_column_headers',
                      self.gf('django.db.models.fields.TextField')(null=True, db_column='column_headers'),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'CsvImport._column_headers'
        db.delete_column(u'csv_csvimport', 'column_headers')


    models = {
        u'csv.csvimport': {
            'Meta': {'object_name': 'CsvImport'},
            '_column_headers': ('django.db.models.fields.TextField', [], {'null': 'True', 'db_column': "'column_headers'"}),
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