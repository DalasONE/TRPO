from django.db import models

# Create your models here.
class Person_D(models.Model):
    User = models.CharField(max_length=100)
    Disease = models.CharField(max_length=100)