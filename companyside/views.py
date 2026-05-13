from django.shortcuts import render , redirect, get_object_or_404
from django.http import JsonResponse
from accounts.models import *
from .models import *
from django.contrib import messages
from rest_framework.decorators import api_view
from rest_framework.response import Response


# Create your views here.

def companyDashboard(request):
    company_id = request.session.get('company_id')
    if not company_id:
        return redirect('com-login')

    try:
        company = CompanyRegister.objects.get(id=company_id)
        print(f"company : {company}")
        job = Joblist.objects.filter(company=company) 
        print(job)
        applications = JobApplication.objects.filter(company=company)
        context = {'user_logged_in': True, 'company': company, 'jobs': job , 'applications': applications}
        return render(request, 'comDashboard.html', context)
    except CompanyRegister.DoesNotExist:
        return redirect('com-login')
    

def logoutCompany(request): 
    if 'company_id' in request.session:
        del request.session['company_id']  # Only remove company session
    return redirect('com-login')






@api_view(["GET", "POST"])
def add_job(request):
    company_id = request.session.get('company_id')
    if not company_id:
        return redirect('com-login')  # Redirect to login if no company session

    company = CompanyRegister.objects.get(id=company_id)  # Get the company instance

    if request.method == "POST":
        job_role = request.POST.get('job_role')
        job_type = request.POST.get('job_type')
        location = request.POST.get('location')
        CGPA = request.POST.get('CGPA')
        LPA = request.POST.get('LPA')
        required_skill = request.POST.get('required_skill')
        qualification = request.POST.get('qualification')
        experience = request.POST.get('experience')
        description = request.POST.get('description')
        application_deadline = request.POST.get('application_deadline')
        register_count = request.POST.get('register_count')
        status = request.POST.get('status')

        job = Joblist(
            company=company,
            job_role=job_role,
            job_type=job_type,
            location=location,
            CGPA=CGPA,
            LPA=LPA,
            required_skill=required_skill,
            qualification=qualification,
            experience=experience,
            description=description,
            application_deadline=application_deadline,
            register_count = register_count,
            is_active = status,
        )
        
        job.save()
        messages.success(request, 'Job posted successfully!')
        return redirect('company_dashboard')
    
    return redirect('company_dashboard')



# def viewJobDetails(request,job_id):

#     job = get_object_or_404(Joblist, id=job_id)
    
#     data = {
#         'job_role': job.job_role,
#         'job_type': job.job_type,
#         'location': job.location,
#         'CGPA': str(job.CGPA),
#         'LPA': str(job.LPA),
#         'required_skill': job.required_skill,
#         'qualification': job.qualification,
#         'experience': job.experience,
#         'description': job.description,
#         'application_deadline': job.application_deadline.strftime('%Y-%m-%d'),
#         'register_count': job.register_count,
#         'status': job.is_active,
#     }
#     # print(data)
    
#     return JsonResponse(data)


@api_view(["GET", "POST"])
def editJobDetails(request, job_id):

    company_id = request.session.get('company_id')
    if not company_id:
        return redirect('com-login')  # Redirect to login if no company session

    job = get_object_or_404(Joblist, id=job_id)  # Ensure the job belongs to the logged-in company
    # print("hi")

    if request.method == 'POST':

        job.job_role = request.POST.get('edit_job_role',job.job_role)
        job.job_type = request.POST.get('edit_job_type',job.job_type)
        job.location = request.POST.get('edit_location',job.location)
        job.CGPA = request.POST.get('edit_CGPA',job.CGPA)
        job.LPA = request.POST.get('edit_LPA',job.LPA)
        job.required_skill = request.POST.get('edit_required_skill',job.required_skill)
        job.qualification = request.POST.get('edit_qualification',job.qualification)
        job.experience = request.POST.get('edit_experience',job.experience)
        job.description = request.POST.get('edit_description',job.description)
        job.application_deadline = request.POST.get('edit_application_deadline',job.application_deadline)
        job.register_count = request.POST.get('edit_register_count',job.register_count)
        job.is_active = request.POST.get('edit_is_active',job.is_active)

        print("Post method")

        job.save()
        return JsonResponse({'success': 'Job updated successfully'})
    
    elif request.method == 'GET':
        data = {

        'job_role': job.job_role,
        'job_type': job.job_type,
        'location': job.location,
        'CGPA': str(job.CGPA),
        'LPA': str(job.LPA),
        'required_skill': job.required_skill,
        'qualification': job.qualification,
        'experience': job.experience,
        'description': job.description,
        'application_deadline': job.application_deadline.strftime('%Y-%m-%d'),
        'register_count': job.register_count,
        'status': job.is_active,
        }

        # print(data)
        return JsonResponse(data)
    
    return JsonResponse({'error': 'Invalid request method'}, status=405)



def updateApplication(request,Id):

    if request.method == 'POST':

        application = get_object_or_404(JobApplication, id=Id)
 
        application.status = request.POST.get('status')
        application.feedback = request.POST.get('feedback')
        application.save()

        return redirect('company_dashboard')
    
    return redirect('company_dashboard')
