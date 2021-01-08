from django.db import models

# Create your models here.

class Person(models.Model):
    class Meta:
        db_table = 'person'
    name = models.CharField(max_length = 128)
    sex = models.CharField(max_length = 4)
    idn = models.CharField(max_length = 18, unique = True)
    photo = models.CharField(max_length = 128, null = True)
    acquire = models.CharField(max_length = 8)
    encode = models.CharField(max_length = 2048)
