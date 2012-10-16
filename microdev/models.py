from django.db import models
from django.contrib.auth.models import User
from django_extensions.db.fields import CreationDateTimeField



class ChangeLogManager(models.Manager):
    
    def log_change(self, user, obj_id, field_name, original_value, updated_value):
        if len(str(original_value)) > ChangeLog.VALUE_MAX_LENGTH:
            original_value = str(original_value)[:(ChangeLog.VALUE_MAX_LENGTH-3)] + '...'

        if len(str(updated_value)) > ChangeLog.VALUE_MAX_LENGTH:
            updated_value = str(updated_value)[:(ChangeLog.VALUE_MAX_LENGTH-3)] + '...'

        # Create the new log entry
        self.get_query_set().create(user=user, obj_id=obj_id, field_name=field_name, original_value=str(original_value), updated_value=str(updated_value))


    def log_if_changed(self, user, obj_id, field_name, original_value, updated_value):
        if original_value == updated_value:
            return
        
        self.log_change(user, obj_id, field_name, original_value, updated_value)


"""--------------------------------------------------------------------
    Abstract 
--------------------------------------------------------------------"""
class ChangeLog(models.Model):
    VALUE_MAX_LENGTH = 1024
    
    date_created = CreationDateTimeField()
    user = models.ForeignKey(User)
    model = models.CharField(max_length=128)
    obj_id = models.IntegerField()
    field_name = models.CharField(max_length=128)
    original_value = models.CharField(max_length=VALUE_MAX_LENGTH)
    updated_value = models.CharField(max_length=VALUE_MAX_LENGTH)
    
    objects = ChangeLogManager()

    # ***** Override in implementation classes *****
    def _get_model_name(self):
        return 'MyModel'

    
    class Meta:
        abstract = True
        ordering = ('-id',)
    
    def __init__(self, *args, **kwargs):
        super(ChangeLog, self).__init__(*args, **kwargs)
        self.model = self._get_model_name()
    
    def __unicode__(self):
        if len(self.original_value) > 32:
            _orig_value = self.original_value[:32] + '...'
        else:
            _orig_value = self.original_value
            
        if len(self.updated_value) > 32:
            _updated_value = self.updated_value[:32] + '...'
        else:
            _updated_value = self.updated_value[:32]
        return "%s | User %i | %s %i | %s: %s->%s" % (self.date_created, self.user.id, self.model, self.obj_id, self.field_name, _orig_value, _updated_value)



class ChangeLoggerMixin():
    _original_state = {}
    
    def _get_change_logger_mixin_ignore_list(self):
        return []

    # Begin tracking changes to the instance
    def track_changes(self):
        self._original_state = dict(self.__dict__)
            
    # Log any changes to the instance to the specified change_log_class
    def log_changes(self, change_log_class, user):
        missing = None
        for key, orig_value in self._original_state.iteritems():
            if key not in self._get_change_logger_mixin_ignore_list():
                new_value = self.__dict__.get(key, missing)
                if str(orig_value) != str(new_value):
                    print(key)
                    print(orig_value)
                    print(new_value)
                    change_log_class.objects.log_if_changed(user, self.id, key, orig_value, new_value)
                    
