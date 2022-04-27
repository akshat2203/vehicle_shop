from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser

# Create your models here.


class User(AbstractUser):
    mobile = models.CharField(max_length=10, null=True)


class Car(models.Model):
    condition_status = (
        ('poor', 'Poor'),
        ('fair', 'Fair'),
        ('good', 'Good'),
        ('excellent', 'Excellent'),
    )

    modal = models.CharField(max_length=150)
    make = models.CharField(max_length=150)
    condition = models.CharField(max_length=10, choices=condition_status)
    price = models.IntegerField()
    seller = models.ForeignKey(User, null=True, on_delete=models.CASCADE, related_name='seller_user')
    buyer = models.ForeignKey(User, null=True, on_delete=models.CASCADE, related_name='buyer_user')
    description = models.CharField(max_length=255)
    year = models.DateTimeField()
    is_sold = models.BooleanField(default=False)

    def __str__(self):
        return self.modal
