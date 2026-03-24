from django.db import models

from django.db.models.signals import post_save
from django.dispatch import receiver

class Student(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    standard = models.ForeignKey('standard.Standard', on_delete=models.CASCADE)
    admission_date = models.DateField(auto_now_add=True)
    discount = models.IntegerField(default=0)   # ✅ added discount field
    image = models.ImageField(upload_to='student_images/', null=True, blank=True)

    def __str__(self):
        return self.name

@receiver(post_save, sender=Student)
def create_fees(sender, instance, created, **kwargs):
    if created:
        from fees.models import Fees
        
        Fees.objects.create(
            student=instance,
            total_fees=instance.standard.total_fees,
            discount=instance.discount
        )
