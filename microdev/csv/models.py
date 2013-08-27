import json

from django.db import models

from django_extensions.db.fields import CreationDateTimeField


class CsvImport(models.Model):
	date_created = CreationDateTimeField()

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
