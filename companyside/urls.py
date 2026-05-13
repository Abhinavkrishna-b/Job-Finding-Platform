from django.contrib import admin
from django.urls import path , include
from .views import *

urlpatterns = [
    path('',companyDashboard,name='company_dashboard'),
    path('logout/', logoutCompany, name='company_logout'),

    path('add-job/', add_job, name='add_job'),
    # path('view-job-details/<int:job_id>/', viewJobDetails, name='view-job-details'),
    path('edit-job-details/<int:job_id>/', editJobDetails, name='edit-job-details'),

    path('update-application/<int:Id>',updateApplication,name='update_application'),
]
