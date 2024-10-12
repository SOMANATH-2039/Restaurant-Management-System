from django.db import models

# Create your models here.

class Booking(models.Model):
    name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)
    email = models.EmailField()
    persons = models.IntegerField()
    date = models.DateField()

    def __str__(self):
        return f"Booking by {self.name} for {self.persons} persons on {self.date}"
