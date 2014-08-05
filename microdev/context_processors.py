import os

import logging
logger = logging.getLogger(__name__)


def inject_current_appengine_version_num(request):
	try:
		current_version_id = os.environ['CURRENT_VERSION_ID']
		current_appengine_version = current_version_id.split('.', 1)[0]
		logger.debug("os.environ['CURRENT_VERSION_ID']: %s" % os.environ['CURRENT_VERSION_ID'])
		logger.debug("current_appengine_version: %s" % current_appengine_version)
	except AttributeError:
		current_appengine_version = None

	return {'current_appengine_version': current_appengine_version,}
