from django.db import models
from standard.models import Standard

class Exam(models.Model):
    name = models.CharField(max_length=100)
    date = models.DateField()
    course = models.CharField(max_length=100)
    total_marks = models.IntegerField(default=0)
    standard = models.ForeignKey(Standard, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} - {self.standard.name}"