from django.db import models
from django.contrib.auth.models import User
from django_extensions.db.fields import CreationDateTimeField


class ChangeLogManager(models.Manager):
    
    def log_if_changed(self, user, obj_id, field_name, original_value, updated_value):
        if original_value == updated_value:
            return
        
        if len(str(original_value)) > ChangeLog.VALUE_MAX_LENGTH:
            original_value = str(original_value)[:(ChangeLog.VALUE_MAX_LENGTH-3)] + '...'

        if len(str(updated_value)) > ChangeLog.VALUE_MAX_LENGTH:
            updated_value = str(updated_value)[:(ChangeLog.VALUE_MAX_LENGTH-3)] + '...'

        # Create the new log entry
        self.get_query_set().create(user=user, obj_id=obj_id, field_name=field_name, original_value=str(original_value), updated_value=str(updated_value))


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

    class Meta:
        abstract = True
        ordering = ('-id',)
    
    # Override in implementation classes accordingly
    def __init__(self, *args, **kwargs):
        super(ChangeLog, self).__init__(*args, **kwargs)
        self.model = 'MyModel'

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
