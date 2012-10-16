# microdev #

A collection of reusable Django utility modules.

This is mostly for my own uses as I build more projects in Django. Whenever I create a bit of functionality that I'll probably need to re-use later, I'll add it here.


## ChangeLoggerMixin ##
The microdev.models.ChangeLoggerMixin provides per-field change logging for any Django model. Here's a simple Django model:

```python
class MyModel(models.Model):
	favorite_color = models.CharField(max_length=128)
	favorite_number = models.IntegerField()
```

Next we define a ChangeLog implementation class and add ChangeLoggerMixin to our model:

```python
from microdev.models import ChangeLoggerMixin
from microdev.models import ChangeLog
	
class MyModelChangeLog(ChangeLog):
	pass

class MyModel(models.Model, ChangeLoggerMixin):
	favorite_color = models.CharField(max_length=128)
	favorite_number = models.IntegerField()
	
    # Overrides from ChangeLoggerMixin
    _change_logger_mixin__change_log_class = MyModelChangeLog
```

The MyModelChangeLog class is a trivial implementation class for the abstract ChangeLog base class.

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

You'll see two new MyModelChangeLog entries:

```
2012-10-16 22:20:19+00:00 | User 1001 | MyModel 5 | favorite_color: blue -> purple
2012-10-16 22:20:19+00:00 | User 1001 | MyModel 5 | favorite_number: 3 -> 7
```


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
