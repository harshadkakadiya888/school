from django.db import models
from students.models import Student


class Fees(models.Model):
    student = models.OneToOneField(Student, on_delete=models.CASCADE)
    total_fees = models.IntegerField()
    discount = models.IntegerField(default=0)
    paid_fees = models.IntegerField(default=0)

    def __str__(self):
        return self.student.name

    @property
    def pending(self):
        payments_total = sum(p.amount for p in self.student.feepayment_set.all())
        return self.total_fees - (payments_total + self.discount)


class FeePayment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    amount = models.IntegerField()
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.name} - {self.amount}"