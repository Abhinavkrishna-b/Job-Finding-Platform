from django.contrib import admin
from .models import *

# Register your models here.
@admin.register(Joblist)  #model name
class Joblist(admin.ModelAdmin):
    list_display =['company','job_role','job_type','location','CGPA','LPA','required_skill','qualification','experience','description','application_deadline','register_count','is_active','posted_at']

@admin.register(JobApplication)
class JobApplied(admin.ModelAdmin):
    list_display = ['user','job','company','application_date','status','status_changed_date','resume','feedback']