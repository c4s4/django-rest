# encoding: UTF-8

from django.db import models


class Customer(models.Model):

    email = models.CharField(max_length=100)
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=50)
    birth_date = models.DateField()
    modification_time = models.DateTimeField(auto_now=True)
    creation_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email
