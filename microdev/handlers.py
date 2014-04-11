import cgi
from djangoappengine import storage

# From http://stackoverflow.com/a/16038212/1639020
class BlobstoreFileUploadHandler(storage.BlobstoreFileUploadHandler):
	"""Handler that adds blob key info to the file object."""

	def new_file(self, field_name, *args, **kwargs):
		# We need to re-process the POST data to get the blobkey info.
		meta = self.request.META
		meta['wsgi.input'].seek(0)
		fields = cgi.FieldStorage(meta['wsgi.input'], environ=meta)
		if field_name in fields:
			current_field = fields[field_name]
			self.content_type_extra = current_field.type_options
		super(BlobstoreFileUploadHandler, self).new_file(field_name, *args, **kwargs)
