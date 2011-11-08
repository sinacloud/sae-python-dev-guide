from django.db import models

# Create your models here.
class Demo(models.Model):
    text = models.CharField(max_length=256)

