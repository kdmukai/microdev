import json
import pickle

from django.db import models
from django.contrib import admin

from django_extensions.db.fields import CreationDateTimeField


class CsvImport(models.Model):
	date_created = CreationDateTimeField()
	_column_headers = models.TextField(db_column="column_headers", null=True)
	notes = models.TextField(null=True)

	def get_column_headers(self):
		if self._column_headers:
			return pickle.loads(self._column_headers)
		else:
			return None

	def set_column_headers(self, value):
		if not value:
			self._column_headers = None
		else:
			self._column_headers = pickle.dumps(value)

	column_headers = property(get_column_headers, set_column_headers)

class CsvImportAdmin(admin.ModelAdmin):
	readonly_fields = ('date_created',)

	class Meta:
		model = CsvImport


class CsvImportRow(models.Model):
	csv_import = models.ForeignKey(CsvImport)
	_json_data = models.TextField(db_column="json_data")

	def get_data_dict(self):
		if self._json_data:
			return json.loads(self._json_data)
		else:
			return None

	def set_data_dict(self, value):
		if not value:
			self._json_data = None
		else:
			self._json_data = json.dumps(value)

	data_dict = property(get_data_dict, set_data_dict)
