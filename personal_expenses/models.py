from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import User

# Create your models here.
class Expense(models.Model):
    
    amount=models.FloatField()  # Amount spent for the expense

    date=models.DateField(default=now) # Date of the expense, defaulting to the current date and time
    description=models.TextField()       # Description of the expense
    owner=models.ForeignKey(to=User, on_delete=models.CASCADE)       # Owner of the expense, linked to a User model through a ForeignKey
    category=models.CharField(max_length=255)

    def __str__(self):
        return self.category
    
    class Meta:
        ordering:['-date']

class Category(models.Model):
    name=models.CharField(max_length=255)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural='Categories'