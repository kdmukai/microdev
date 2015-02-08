import httplib2

from oauth2client.client import OAuth2WebServerFlow
from apiclient.discovery import build
from apiclient.http import MediaIoBaseUpload

from django.db import transaction

from microdev.google_client_api.models import ServerCredentials


import logging
logger = logging.getLogger(__name__)


def authorize_server(client_id, client_secret, oauth_scope, redirect_uri):
	"""
		This should only need to be done once to authorize a system account for the
		webserver. 

		When prompted, authorize the Google account associated with the webapp itself.

		The resulting credentials will be stored in the DB for reuse.
	"""
	# Initialize an OAuth2 flow to request access.
	flow = OAuth2WebServerFlow(
		client_id,
		client_secret,
		oauth_scope,
		approval_prompt='force',	# Makes sure we get a refresh token
		redirect_uri=redirect_uri
	)

	# Return the authorization URL.
	authorize_url = flow.step1_get_authorize_url()

	return authorize_url



def server_oauth2callback(client_id, client_secret, oauth_scope, redirect_uri, code):
	"""
		Completes the OAuth2 handshake, reads the return code, and stores the
		credentials in the DB.
	"""
	# Need an identical Flow object in order to continue
	flow = OAuth2WebServerFlow(
		client_id,
		client_secret,
		oauth_scope,
		approval_prompt='force',
		redirect_uri=redirect_uri
	)

	# Use the code returned by the authorization URL and exchange it for the access and refresh tokens.
	credentials = flow.step2_exchange(code)

	with transaction.commit_on_success():
		# There should only be one ServerCredentials object. Clear out old ones.
		ServerCredentials.objects.all().delete()

		# Save the credentials in a new ServerCredentials object
		ServerCredentials(
			credentials=credentials
		).save()



def _get_server_credentials():
	# Retrieve only the most recent ServerCredentials entry
	server_credentials = ServerCredentials.objects.all().order_by('-pk')[:1]

	if not server_credentials:
		logger.error("No ServerCredentials found!")
		return None

	else:
		# Return the Google client API's native credentials object
		return server_credentials[0].credentials


def _get_drive_api_service():
	http = httplib2.Http()

	server_credentials = _get_server_credentials()
	if not server_credentials:
		logger.error("No ServerCredentials found!")
		raise Exception("No ServerCredentials found!")

	# Use the credentials to authorize an http request object
	http = server_credentials.authorize(http)

	# Build the Drive API service object using the authorized
	#	http request and return both
	return http, build('drive', 'v2', http=http)



def drive__upload(content, mimetype, title, convert=True):
	http, drive_service = _get_drive_api_service()

	# Assemble the content stream
	media = MediaIoBaseUpload(content, mimetype=mimetype, resumable=False)

	# Specify metadata
	body = {
		'title': title
	}

	# Insert the file
	drive_file = drive_service.files().insert(
		body=body,
		media_body=media,
		convert=convert
	).execute()

	# Return the new file's identifier
	return drive_file['id']



def drive__convert_and_download(fileId, convert_to_mimetype):
	http, drive_service = _get_drive_api_service()

	# Load the target file
	drive_file = drive_service.files().get(fileId=fileId).execute()

	# Get its exportLink for the specified mimetype
	download_url = drive_file['exportLinks'][convert_to_mimetype]

	# Stream the download into memory
	response_headers, content = http.request(download_url, "GET")

	# Return the resulting byte stream
	return content



def drive__delete(fileId):
	http, drive_service = _get_drive_api_service()

	drive_service.files().delete(fileId=fileId).execute()

