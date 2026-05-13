from django.db import models
from accounts.models import UserRegister

class UserProfile(models.Model):
    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    ]
    
    YES_NO_CHOICES = [
        ('Yes', 'Yes'),
        ('No', 'No'),
    ]
    
    # One-to-one link to UserRegister
    user = models.OneToOneField(UserRegister, on_delete=models.CASCADE, related_name='user_profile')
    
    # Personal Information (only fields not in UserRegister)
    profile_photo = models.ImageField(upload_to='profile_photos/', blank=True, null=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    location = models.CharField(max_length=100, blank=True, null=True)
    
    # Academic Information
    tenth_percentage = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True) # Increased max_digits to 5
    twelfth_percentage = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True) # Increased max_digits to 5
    diploma_status = models.CharField(max_length=100, blank=True, null=True)
    ug_cgpa = models.DecimalField(max_digits=4, decimal_places=2, blank=True, null=True)
    pg_status = models.CharField(max_length=100, blank=True, null=True)
    backlogs_history = models.CharField(max_length=3, choices=YES_NO_CHOICES, blank=True, null=True)
    current_backlogs = models.PositiveIntegerField(default=0, blank=True, null=True)
    
    # Additional Information
    about_me = models.TextField(blank=True, null=True)
    resume = models.FileField(upload_to='resumes/', blank=True, null=True)
    
    # 👇 ADD THESE NEW FIELDS FOR PROFESSIONAL INFO 👇
    linkedin_url = models.URLField(max_length=255, blank=True, null=True)
    github_url = models.URLField(max_length=255, blank=True, null=True)
    portfolio_url = models.URLField(max_length=255, blank=True, null=True)
    certifications = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.user.username}'s Profile"
    
    # Convenience properties to access UserRegister fields
    @property
    def email(self):
        return self.user.email
    
    @property
    def phone_number(self):
        return self.user.phone_number
    
    @property
    def username(self):
        return self.user.username