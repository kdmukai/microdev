from django.db import models
from django.contrib.auth.models import User
from django.contrib import admin
from django_extensions.db.fields import CreationDateTimeField, ModificationDateTimeField
import shortuuid


class ChangeLogManager(models.Manager):
	
	def log_change(self, user, model, obj_id, field_name, original_value, updated_value):
		if len(str(original_value)) > ChangeLog.VALUE_MAX_LENGTH:
			original_value = str(original_value)[:(ChangeLog.VALUE_MAX_LENGTH-3)] + '...'

		if len(str(updated_value)) > ChangeLog.VALUE_MAX_LENGTH:
			updated_value = str(updated_value)[:(ChangeLog.VALUE_MAX_LENGTH-3)] + '...'

		# Create the new log entry
		self.get_query_set().create(user=user, model=model, obj_id=obj_id, field_name=field_name, original_value=str(original_value), updated_value=str(updated_value))


"""--------------------------------------------------------------------
	Abstract 
--------------------------------------------------------------------"""
class ChangeLog(models.Model):
	VALUE_MAX_LENGTH = 1024
	
	date_created = CreationDateTimeField()
	user = models.ForeignKey(User, blank=True, null=True)
	model = models.CharField(max_length=128)
	obj_id = models.IntegerField()
	field_name = models.CharField(max_length=128)
	original_value = models.CharField(max_length=VALUE_MAX_LENGTH)
	updated_value = models.CharField(max_length=VALUE_MAX_LENGTH)
	
	objects = ChangeLogManager()

	class Meta:
		abstract = True
		ordering = ('-pk',)

class ChangeLogAdmin(admin.ModelAdmin):
	# inlines = [VideoRecipientInline]
	list_display = ('date_created',	'model', 'obj_id', 'field_name', 'original_value', 'updated_value',)
	list_filter = ('date_created', 'model', 'obj_id',)


"""--------------------------------------------------------------------
	Modified from:
	http://stackoverflow.com/a/111364/1639020
--------------------------------------------------------------------"""
class ChangeLoggerMixin():
	_original_state = {}
	
	# Override in the implementation class to exclude change tracking on listed fields
	_change_logger_mixin__ignore_list = ['date_updated']
	
	# Must override to specify which ChangeLog implementation class to write to
	_change_logger_mixin__change_log_class = None
	

	# Begin tracking changes to the instance
	def track_changes(self):
		self._original_state = dict(self.__dict__)
	
	# Check model's status - name is extended to avoid namespace conflicts
	def change_logger_mixin__is_changed(self):
		if not self._change_logger_mixin__change_log_class:
			raise Exception('microdev.models.ChangeLoggerMixin: _change_logger_mixin__change_log_class was not defined in the implementation class %s' % self.__class__.__name__)
			return
		
		missing = None
		for key, orig_value in self._original_state.iteritems():
			if key not in self._change_logger_mixin__ignore_list:
				new_value = self.__dict__.get(key, missing)
				if str(orig_value) != str(new_value):
					return True
		return False

					
	# Log any changes to the instance to the specified change_log_class
	def log_changes(self, user=None):
		from django.db import transaction
		if not self._change_logger_mixin__change_log_class:
			raise Exception('microdev.models.ChangeLoggerMixin: _change_logger_mixin__change_log_class was not defined in the implementation class %s' % self.__class__.__name__)
			return
		
		missing = None
		with transaction.commit_on_success():	# Batches up all the log entry saves
			for key, orig_value in self._original_state.iteritems():
				if key not in self._change_logger_mixin__ignore_list and key != '_original_state':
					new_value = self.__dict__.get(key, missing)
					if str(orig_value) != str(new_value):
						self._change_logger_mixin__change_log_class.objects.log_change(user, self.__class__.__name__, self.id, key, orig_value, new_value)



class ChangeLoggedModel(models.Model, ChangeLoggerMixin):
	""" 
		A newer, more convenient approach that automatically logs all changes to
		existing objects. 
	"""
	class Meta:
		abstract = True

	def __init__(self, *args, **kwargs):
		super(ChangeLoggedModel, self).__init__(*args, **kwargs)
		if self.pk:
			# Only track changes after initial save
			self.track_changes()

	def save(self, *args, **kwargs):
		if self.pk:
			self.log_changes()
		super(ChangeLoggedModel, self).save(*args, **kwargs)



class UuidModel(models.Model):
	"""
		A simple abstract base class to automatically generate a standard UUID 
		for each instance of a model.
	"""
	uuid = models.CharField(max_length=36, null=True, blank=True)

	class Meta:
		abstract = True

	def generate_uuid(self):
		""" Can be explictly called at any time and will be automatically called on save
			if uuid is None """
		import uuid
		self.uuid = uuid.uuid4()

	def save(self, *args, **kwargs):
		if not self.uuid:
			self.generate_uuid()
		super(UuidModel, self).save(*args, **kwargs)

class UuidModelAdmin(admin.ModelAdmin):
	readonly_fields = ('uuid',)



class ShortUuidModel(models.Model):
	"""
		A simple abstract base class to automatically generate a short UUID 
		for each instance of a model.
	"""
	uuid = models.CharField(max_length=22, null=True, blank=True)

	class Meta:
		abstract = True

	def save(self, *args, **kwargs):
		if not self.uuid:
			self.uuid = shortuuid.uuid()
		super(ShortUuidModel, self).save(*args, **kwargs)

class ShortUuidModelAdmin(admin.ModelAdmin):
	readonly_fields = ('uuid',)



class TimestampModel(models.Model):
	"""
		Abstract base class that automatically logs date_created and
		date_updated
	"""
	date_created = CreationDateTimeField()
	date_updated = ModificationDateTimeField()

	class Meta:
		abstract = True

class TimestampModelAdmin(admin.ModelAdmin):
	readonly_fields = ('date_created', 'date_updated',)



class CsrNoteModel(models.Model):
	"""
		A simple abstract base class for customer service reps to log
		their actions 
	"""
	note = models.TextField()
	date_created = CreationDateTimeField()
	csr_agent = models.ForeignKey('auth.User', null=True, blank=True)

	class Meta:
		abstract = True


class CsrNoteModelInline(admin.StackedInline):
	readonly_fields = ('date_created', 'csr_agent',)
	extra = 1


