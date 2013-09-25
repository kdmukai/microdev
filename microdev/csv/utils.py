import csv

from django.db import transaction

from microdev.csv.models import CsvImport, CsvImportRow

import logging
logger = logging.getLogger(__name__)


def ingest_csv(csv_file_form=None, csv_file=None, has_header_row=True, required_fields=[]):
	logger.debug("ingest_csv called")
	if csv_file_form:
		csv_file = csv_file_form.cleaned_data['file']
		has_header_row = csv_file_form.cleaned_data['has_header_row']

	if not csv_file:
		raise Exception("Pass in CsvFileForm instance or csv_file=request.FILES.get('file')")

	column_headers = []
	if has_header_row:
		# Read and store the header row column names
		r = csv.reader(csv_file.read().splitlines())
		row = r.next()
		for column_header in row:
			column_headers.append(column_header)

	# Check for required fields (optional check)
	for field in required_fields:
		if field not in column_headers:
			raise Exception("Invalid CSV file. Must contain %s." % field)

	# Create the parent CsvImport record
	csv_import = CsvImport(
		column_headers = column_headers
	)
	csv_import.save()

	with transaction.commit_on_success():
		csv_file.seek(0)
		for index, row in enumerate(csv.reader(csv_file.read().splitlines())):
			if index == 0 and has_header_row:
				# Don't save the header row as data
				continue

			row_dict = {}
			for column_index, column_value in enumerate(row):
				if column_index == len(column_headers):
					column_headers.append("field_%i" % column_index)
				row_dict[column_headers[column_index]] = column_value

			csv_import_row = CsvImportRow()
			csv_import_row.csv_import = csv_import
			csv_import_row.data_dict = row_dict
			csv_import_row.save()

		# Update the CsvImport record, if necessary (some files may have
		#	additional columns of data with no header)
		if len(column_headers) > len(csv_import.column_headers):
			csv_import.column_headers = column_headers
			csv_import.save()
	# ...Ends transaction

	return csv_import
