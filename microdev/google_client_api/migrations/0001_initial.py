# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'ServerCredentials'
        db.create_table(u'google_client_api_servercredentials', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('credentials', self.gf('oauth2client.django_orm.CredentialsField')(null=True)),
        ))
        db.send_create_signal(u'google_client_api', ['ServerCredentials'])


    def backwards(self, orm):
        # Deleting model 'ServerCredentials'
        db.delete_table(u'google_client_api_servercredentials')


    models = {
        u'google_client_api.servercredentials': {
            'Meta': {'object_name': 'ServerCredentials'},
            'credentials': ('oauth2client.django_orm.CredentialsField', [], {'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        }
    }

    complete_apps = ['google_client_api']