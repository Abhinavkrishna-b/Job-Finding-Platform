from django.db import models
from accounts.models import *

# Create your models here.
 
class Joblist(models.Model):
    company = models.ForeignKey(CompanyRegister, on_delete=models.CASCADE, null=True, blank=True)
    job_role = models.CharField(max_length=300, null=True, blank=True)
    job_type = models.CharField(max_length=300, null=True, blank=True)  # e.g. Full-time, Part-time, Internship
    location = models.CharField(max_length=1000, null=True, blank=True)
    CGPA = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)  # Usually CGPA is numeric (you can also use DecimalField)
    LPA = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)  # Salary in LPA (Lakhs per Annum) — consider DecimalField too
    required_skill = models.CharField(max_length=5000, null=True, blank=True)  # Skills like "Python, Django, React"
    qualification = models.CharField(max_length=500, null=True, blank=True)  # Degree: B.Tech / BCA etc.
    experience = models.CharField(max_length=100, null=True, blank=True)  # ✨ Added: e.g. "0-2 years" or "Fresher allowed"
    description = models.TextField(default="No description provided", null=True, blank=True)
    application_deadline = models.DateField(null=True, blank=True)
    register_count = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)  # ✨ Added: allow company to deactivate old jobs without deleting.
    posted_at = models.DateTimeField(auto_now_add=True)  # ✨ Added: so you can show "Posted X days ago"

    def __str__(self):
        company_name = self.company.company_name if self.company else "Unknown Company"
        return f"{self.job_role or 'Job Role'} at {company_name}"
    


class JobApplication(models.Model):
    APPLICATION_STATUS = [
        ('Applied', 'Applied'),  # Default status when user applies
        ('Under Review', 'Under Review'),
        ('Accepted', 'Accepted'),
        ('Rejected', 'Rejected'),
    ]
    
    user = models.ForeignKey(UserRegister, on_delete=models.CASCADE, related_name='job_applications',null=True, blank=True)
    job = models.ForeignKey(Joblist, on_delete=models.CASCADE, related_name='applications',null=True, blank=True)
    company = models.ForeignKey(CompanyRegister, on_delete=models.CASCADE, related_name='received_applications',null=True, blank=True)
    
    # Application details
    application_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=APPLICATION_STATUS, default='Applied')
    status_changed_date = models.DateTimeField(auto_now=True)

    resume = models.FileField(upload_to='application_resumes/', blank=True, null=True)
    
    # Company feedback
    feedback = models.TextField(blank=True, null=True)
    
    class Meta:
        unique_together = ('user', 'job')  # Prevent duplicate applications
        ordering = ['-application_date']
    
    def __str__(self):
        username = self.user.username if self.user else "Unknown User"
        job_role = self.job.job_role if self.job else "Unknown Role"
        company_name = self.company.company_name if self.company else "Unknown Company"
        return f"{username}'s application for {job_role} at {company_name}"
