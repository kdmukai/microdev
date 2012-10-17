# microdev #

A collection of reusable Django utility modules.

This is mostly for my own uses as I build more projects in Django. Whenever I create a bit of functionality that I'll probably need to re-use later, I'll add it here.


## ChangeLoggerMixin ##
The microdev.models.ChangeLoggerMixin provides per-field change logging for any Django model.

The database can only keep track of a model instance's latest state, but there are plenty of use cases where it's important or useful to keep track of previous states. There are basic auditing uses but, more interestingly, tracking previous states opens up new avenues for data analysis.

For example, if you were running a dating site, you could average all users' popularity before and after changing their smoker status to "I quit". 


### Integration ###
Here's a simple Django model:

```python
class MyModel(models.Model):
	favorite_color = models.CharField(max_length=128)
	favorite_number = models.IntegerField()
```

Next we define a trivial ChangeLog implementation class and add ChangeLoggerMixin to our model:

```python
from microdev.models import ChangeLog
from microdev.models import ChangeLoggerMixin
	
class MyModelChangeLog(ChangeLog):
	pass

class MyModel(models.Model, ChangeLoggerMixin):
	favorite_color = models.CharField(max_length=128)
	favorite_number = models.IntegerField()
	
    # Overrides from ChangeLoggerMixin
    _change_logger_mixin__change_log_class = MyModelChangeLog
```

The \_change\_logger\_mixin\_\_change\_log\_class variable needs to point to a ChangeLog implementation class so that the mix-in will know where to write the log entries. You don't have to have a dedicated ChangeLog implementation class for each model that you're logging. You could have all models write to the same ChangeLog implementation class, but it seems cleaner to me for each model to have its own separate set of logs. The mix-in supports either approach.

Remember to run:
```
./manage.py syncdb
```
This will add the MyModelChangeLog table to your database.


### Usage ###
Now in your client code you can activate ChangeLoggerMixin logging with two simple calls: track_changes() and log_changes():

```python
def do_something(request):
	# Create an instance just to have some initial data...
	my_model = MyModel()
	my_model.favorite_color = 'blue'
	my_model.favorite_number = 3
	my_model.save()
	
	# Now activate change tracking
	my_model.track_changes()
	
	# Make changes
	my_model.favorite_color = 'purple'
	my_model.favorite_number = 9
	my_model.save()
	
	# Log the changes
	my_model.log_changes(request.user)
```

The design assumes a specific Django User is driving these changes and expects the User to be passed in.


### Output ###
You'll see two new MyModelChangeLog entries:

```
2012-10-16 22:20:19+00:00 | User 1001 | MyModel 5 | favorite_color: blue -> purple
2012-10-16 22:20:19+00:00 | User 1001 | MyModel 5 | favorite_number: 3 -> 7
```

That's the \_\_unicode\_\_ output. The actual ChangeLog keeps all the data separated out to make it easy to run queries against it later. Here's the ChangeLog structure:

```python
class ChangeLog(models.Model):
    VALUE_MAX_LENGTH = 1024
    
    date_created = CreationDateTimeField()
    user = models.ForeignKey(User)
    model = models.CharField(max_length=128)
    obj_id = models.IntegerField()
    field_name = models.CharField(max_length=128)
    original_value = models.CharField(max_length=VALUE_MAX_LENGTH)
    updated_value = models.CharField(max_length=VALUE_MAX_LENGTH)
```

And obviously the ChangeLog will only log the fields that have changed. Unchanged fields are ignored and won't appear in the log.


### Customization ###
Let's say your model has a field that always changes but you don't want to track it. No prob, just override the ignore_list:

```python
class MyModel(models.Model, ChangeLoggerMixin):
	favorite_color = models.CharField(max_length=128)
	favorite_number = models.IntegerField()
	date_updated = models.DateTimeField()
	
    # Overrides from ChangeLoggerMixin
    _change_logger_mixin__ignore_list = ['date_updated',]
    _change_logger_mixin__change_log_class = MyModelChangeLog
```

Now any changes to the date_updated field will not be logged. 


### Acknowledgments ###
The ChangeLoggerMixin was adapted from Armin's original suggestion at: http://stackoverflow.com/a/111364/1639020
