from django.db import models
from django_extensions.db.fields import CreationDateTimeField
from django_extensions.db.fields import ModificationDateTimeField
from microdev.models import ChangeLog
from microdev.models import ChangeLoggerMixin


"""-----------------------------------------------------------------
    Trivial ChangeLog implementation class to store logs.
-----------------------------------------------------------------"""
class DefaultChangeLog(ChangeLog): pass


"""-----------------------------------------------------------------
    Django abstract base model using the DefaultChangeLog
-----------------------------------------------------------------"""
class ChangeLoggerModel(models.Model, ChangeLoggerMixin):
    date_created = CreationDateTimeField()          # Automatic timestamp on initial save.
    date_updated = ModificationDateTimeField()      # Automatic timestamps on subsequent saves.

    # Override from ChangeLoggerMixin
    _change_logger_mixin__ignore_list = ['date_updated',]       # Don't log changes to the date_updated timestamp
    _change_logger_mixin__change_log_class = DefaultChangeLog   # Specify where changes get logged to

    class Meta:
        abstract = True


"""-----------------------------------------------------------------
    Django model using the DefaultChangeLog
-----------------------------------------------------------------"""
class MyModel(ChangeLoggerModel):
    favorite_color = models.CharField(max_length=64)
    favorite_number = models.IntegerField()
    
    # If you need to define Meta attributes, be sure to subclass 
    #    the base class' Meta...
    class Meta(ChangeLoggerModel.Meta):
        pass


"""-----------------------------------------------------------------
    Django model using a custom ChangeLog
-----------------------------------------------------------------"""
class MyOtherModelChangeLog(ChangeLog): pass
class MyOtherModel(ChangeLoggerModel):
    favorite_color = models.CharField(max_length=64)
    favorite_number = models.IntegerField()
    do_not_log_me = models.IntegerField()

    # Override from ChangeLoggerMixin
    _change_logger_mixin__ignore_list = ['date_updated', 'do_not_log_me',]
    _change_logger_mixin__change_log_class = MyOtherModelChangeLog

    class Meta(ChangeLoggerModel.Meta):
        pass
