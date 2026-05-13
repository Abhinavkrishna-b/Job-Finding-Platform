from django.contrib import admin
from .models import *

# Register your models here.
@admin.register(UserProfile)  #model name
class userProfileAdmin(admin.ModelAdmin):
    list_display =['user','profile_photo','gender','date_of_birth','location','tenth_percentage','twelfth_percentage','diploma_status','ug_cgpa','pg_status','backlogs_history','current_backlogs','about_me','resume']