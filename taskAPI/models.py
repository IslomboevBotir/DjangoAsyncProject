from django.db import models


class Project(models.Model):
    cid = models.IntegerField()
    unit = models.CharField(max_length=255)
    w_id = models.IntegerField(unique=True)
    utype = models.CharField(max_length=255)
    beds = models.IntegerField()
    area = models.FloatField()
    price = models.IntegerField()
    date = models.DateField()
    is_mode = models.BooleanField()
    is_del = models.BooleanField()

    class Meta:
        db_table = 'project'

