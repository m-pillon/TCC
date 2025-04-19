from django.db import models

# Create your models here.
class Form(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField
    sleepQuality = models.IntegerField
    sleepDuration = models.IntegerField
