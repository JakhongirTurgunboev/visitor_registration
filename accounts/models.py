import datetime

from django.contrib.auth.models import User
from django.core import validators
from django.db import models


# Create your models here.


class Building(models.Model):
    name = models.CharField(max_length=100, unique=True)
    address = models.TextField()

    def __str__(self):
        return self.name


class Reservation(models.Model):
    STATUS_CHOICES = [
        (1, "accept"),
        (0, "in progress"),
        (-1, "rejected")
    ]
    building = models.ForeignKey(Building, on_delete=models.CASCADE)
    planned_date = models.DateField()
    status = models.IntegerField(choices=STATUS_CHOICES, default=0)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)

