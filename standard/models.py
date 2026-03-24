from django.db import models


class Standard(models.Model):
    name = models.CharField(max_length=100)
    total_fees = models.IntegerField(default=0)

    def __str__(self):
        return self.name