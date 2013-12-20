import unicodecsv

from django.db import transaction
from django.http import HttpResponse

from microdev.csv.models import CsvImport, CsvImportRow

import logging
logger = logging.getLogger(__name__)


def validate_and_return_rows(csv_file_form=None, csv_file=None, has_header_row=True, required_fields=[]):
	"""
		Opens a CSV file and optionally checks for required fields in the header. Returns
		the rows of the CSV and a list of the headers as a tuple: (csv_rows, headers)
	"""
	if csv_file_form:
		csv_file = csv_file_form.cleaned_data['file']
		has_header_row = csv_file_form.cleaned_data['has_header_row']

	if not csv_file:
		raise Exception("Pass in CsvFileForm instance or csv_file=request.FILES.get('file')")

	column_headers = []
	if has_header_row:
		# Read and store the header row column names
		r = unicodecsv.reader(csv_file.read().splitlines(), encoding='utf-8')
		row = r.next()
		for column_header in row:
			column_headers.append(column_header)

		# Check for required fields (optional check)
		for field in required_fields:
			if field not in column_headers:
				raise Exception("Invalid CSV file. Must contain %s." % field)

	csv_file.seek(0)
	return (unicodecsv.reader(csv_file.read().splitlines(), encoding='utf-8'), column_headers)



def ingest_csv(csv_file_form=None, csv_file=None, has_header_row=True, required_fields=[]):
	logger.debug("ingest_csv called")

	csv_rows, column_headers = validate_and_return_rows(csv_file_form, csv_file, has_header_row, required_fields)

	# Create the parent CsvImport record
	csv_import = CsvImport(
		column_headers = column_headers
	)
	csv_import.save()

	with transaction.commit_on_success():
		for index, row in enumerate(csv_rows):
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





def generate_csv_response(data_array, output_filename, headers=None):
	# Create the HttpResponse object with the appropriate CSV header.
	response = HttpResponse(content_type='text/csv')
	if not output_filename.endswith(".csv"):
		output_filename += ".csv"
	response['Content-Disposition'] = 'attachment; filename="%s"' % output_filename

	writer = unicodecsv.writer(response, encoding='utf-8')

	if headers:
		writer.writerow(headers)
	for data_row in data_array:
		writer.writerow(data_row)

	return response


