from django.db import models
from hdhomerun.models import Device

# Create your models here.

class Channel(models.Model):
    device = models.ForeignKey(Device)
    channel = models.IntegerField()
    program = models.IntegerField()
    desc = models.CharField(max_length=50)

    def __unicode__(self):
        return self.desc
