from django.db import models

# Create your models here.

class Device(models.Model):
    hdid = models.CharField(max_length=8)

    def __unicode__(self):
        return self.hdid

