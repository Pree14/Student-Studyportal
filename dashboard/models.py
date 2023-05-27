from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Notes(models.Model): # inherit the class to this parent Model class
    user = models.ForeignKey(User, on_delete=models.CASCADE) #when the user will be deleted then this notes also get deleted from db
    title = models.CharField(max_length=200)
    description = models.TextField()

    class Meta:
        verbose_name = "notes"  # is used to remove the extra s in the db adding s is a default behaviour is dj
        verbose_name_plural = "notes"

    def __str__(self):
        return self.title  # to return the notes title on the db

class Homework(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.CharField(max_length=50)
    title = models.CharField(max_length=100)
    description = models.TextField()
    due = models.DateTimeField()
    is_finished = models.BooleanField(default=False)

    def __str__(self):
        return self.title 

class Todo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    is_finished = models.BooleanField(default=False)

    def __str__(self):
        return self.title 

