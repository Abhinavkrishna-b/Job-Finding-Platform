from django.db import models
from django.core.validators import RegexValidator

# Create your models here.

class CompanyRegister(models.Model):   
    email = models.EmailField(null=True, blank=True)
    company_name = models.CharField(max_length=400, null=True, blank=True)
    location = models.CharField(max_length=1000, null=True, blank=True)
    password = models.CharField(max_length=150, null=True, blank=True)

    def __str__(self):
        return self.company_name
    


class UserRegister(models.Model):
    username = models.CharField(max_length=400, null=True, blank=True)
    email = models.EmailField(unique=True, null=False, blank=False)
    phone_number = models.CharField(max_length=12,unique=True, null=False, blank=False,validators=[
        RegexValidator(
            regex=r'^\d{10,12}$',
            message='Enter a valid phone number with 10 to 12 digits.'
        )
    ])
    password = models.CharField(max_length=150, null=True, blank=True)

    def __str__(self):
        return self.username