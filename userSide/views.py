from django.shortcuts import render, redirect, get_object_or_404
from accounts.models import *
from .models import *
from companyside.models import *
from accounts.models import *
from django.contrib import messages
from rest_framework.decorators import api_view
from rest_framework.response import Response
import os
from django.http import JsonResponse
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import google.generativeai as genai
import json
import PyPDF2
import docx2txt
import io


# Create your views here.
def userDashboard(request):

    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('user-login')
    
    try:
        user = UserRegister.objects.get(id=user_id)
        user_profile,  created = UserProfile.objects.get_or_create(user=user)
        applied_jobs = JobApplication.objects.filter(user=user)
        joblist = Joblist.objects.all()
        print(joblist)

        context = {'user_logged_in' : True,'user':user, 'job_list' : joblist, "user_profile":user_profile, 'resume_uploaded': bool(user_profile.resume),'applied_jobs':applied_jobs}
        return render(request, 'userDashboard.html', context)
    
    except UserRegister.DoesNotExist:
        return redirect('user-login')
    

def logoutUser(request): 
    if 'user_id' in request.session:
        del request.session['user_id']  # Only remove user session
    return redirect('user-login')


@api_view(["GET", "POST"])
def profile_view(request, username):

    if not username:
        return redirect('user-login')
    
    # # try:
    # user = get_object_or_404(UserRegister, username=username)
    # print(f'name : {user}')
    # user_profile = UserProfile.objects.get(user=user)
    # print(f"User : {user_profile}")
    # context = {'user': user_profile}
    # return render(request, 'profile.html', context)
    
    # # except UserProfile.DoesNotExist:
    # #     return redirect('user-login')
    
    user = get_object_or_404(UserRegister, username=username)
    user_profile, created = UserProfile.objects.get_or_create(user=user)
    applied_jobs = JobApplication.objects.filter(user=user)
    # print(user_profile)

    return render(request, 'profile.html', {'user': user, 'user_profile':user_profile,'resume_uploaded': bool(user_profile.resume), 'applied_jobs':applied_jobs})



@api_view(["GET", "POST"])
def edit_personal(request, username):
    
    # Fetch the user and their profile
    user = get_object_or_404(UserRegister, username=username)
    user_profile, created = UserProfile.objects.get_or_create(user=user)

    if request.method == "POST":
        # Updating UserRegister fields
        user.username = request.POST.get('editName', user.username)
        user.email = request.POST.get('editEmail', user.email)
        user.phone_number = request.POST.get('editPhone', user.phone_number)
        user.save()
    
        # Updating UserProfile fields
        user_profile.gender = request.POST.get('editGender', user_profile.gender)
        
        date_of_birth = request.POST.get('editDob')

        print(f'date {date_of_birth}')
        if date_of_birth:  # If there's a value, update it
            user_profile.date_of_birth = date_of_birth
        else:
            # If no date provided, retain the current value (or you can set a default)
            user_profile.date_of_birth = user_profile.date_of_birth or None

        user_profile.location = request.POST.get('editlocation', user_profile.location)
        user_profile.about_me = request.POST.get('editabout_me', user_profile.about_me)
        user_profile.save()

        print(user_profile.about_me)

        messages.success(request, 'Personal information updated successfully!')
        return redirect('profile_view', username=user.username)

    return Response({"message": "Use POST method to update data."})



@api_view(["GET", "POST"])
def edit_academic(request,username):

    user = get_object_or_404(UserRegister, username = username)
    user_profile, created= UserProfile.objects.get_or_create(user = user)
    print("edit acedamic")

    if request.method == "POST":

        user_profile.tenth_percentage = request.POST.get('editTenthPercentage', user_profile.tenth_percentage)
        user_profile.twelfth_percentage = request.POST.get('editTwelfthPercentage', user_profile.twelfth_percentage)
        user_profile.diploma_status = request.POST.get('editdiplomaStatus', user_profile.diploma_status)
        user_profile.ug_cgpa = request.POST.get('editUgCgpa', user_profile.ug_cgpa)
        user_profile.pg_status = request.POST.get('editpgStatus', user_profile.pg_status)
        user_profile.backlogs_history = request.POST.get('editBacklogsHistory', user_profile.backlogs_history)
        user_profile.current_backlogs = request.POST.get('editCurrentBacklogs', user_profile.current_backlogs)
        user_profile.save()

        print("edit acedamic i if")

        messages.success(request, 'Personal information updated successfully!')
        return redirect('profile_view', username=user.username)
    
    return Response({"message": "Use POST method to update data."})


def upload_resume(request,username):
    try:
        if 'resume' not in request.FILES:
            return JsonResponse({'status': 'error', 'message': 'No file provided'}, status=400)
        
        resume_file = request.FILES['resume']
        
        # Validate file type
        allowed_extensions = ['.pdf', '.doc', '.docx']
        file_ext = os.path.splitext(resume_file.name)[1].lower()
        if file_ext not in allowed_extensions:
            return JsonResponse({
                'status': 'error',
                'message': 'Invalid file type. Only PDF, DOC, and DOCX files are allowed.'
            }, status=400)
        
        # Validate file size (5MB limit)
        if resume_file.size > 5 * 1024 * 1024:
            return JsonResponse({
                'status': 'error',
                'message': 'File too large. Maximum size is 5MB.'
            }, status=400)
        
        # Get or create user profile
        user = get_object_or_404(UserRegister, username = username)
        profile, created = UserProfile.objects.get_or_create(user=user)
        
        # Delete old resume if exists
        if profile.resume:
            old_resume_path = os.path.join(settings.MEDIA_ROOT, str(profile.resume))
            if os.path.exists(old_resume_path):
                os.remove(old_resume_path)
        
        # Save new resume
        profile.resume = resume_file
        profile.save()
        
        return JsonResponse({'status': 'success','message': 'Resume uploaded successfully','filename': resume_file.name})
    
        
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': f'An error occurred: {str(e)}'
        }, status=500)
    


def registercount(job_id):

        job = Joblist.objects.get(id=job_id)

        if job.register_count < 5:
            job.register_count += 1
        else:
            job.is_active = False
        
        job.save()


def applyingJob(request):

    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('user-login')
    
    if request.method == "POST":
        
        job_id = request.POST.get('job_id')
        job = Joblist.objects.get(id=job_id)  # ✅ Always unique

        company_name = job.company

        try:
            user = UserRegister.objects.get(id=user_id)
            user_profile = UserProfile.objects.get(user=user)
        except (UserRegister.DoesNotExist, UserProfile.DoesNotExist):
            return redirect('user-login')  # or handle error gracefully

        user_resume = user_profile.resume

        application = JobApplication.objects.create(
            user=user,  
            job=job,  # ✅ Proper ForeignKey object
            company=company_name,
            resume=user_resume
        )
        application.save()

        registercount(job_id)


        return redirect('user_dashboard')  # or wherever you want after applying

    return redirect('user_dashboard')
def edit_certifications(request, username):
    user = get_object_or_404(UserRegister, username=username)
    user_profile = get_object_or_404(UserProfile, user=user)

    if request.method == 'POST':
        # Get data from the textarea and save it
        user_profile.certifications = request.POST.get('certifications')
        user_profile.save()
        messages.success(request, 'Certifications updated successfully!')
        return redirect('profile_view', username=username)

    return redirect('profile_view', username=username)


def edit_links(request, username):
    user = get_object_or_404(UserRegister, username=username)
    user_profile = get_object_or_404(UserProfile, user=user)

    if request.method == 'POST':
        # Get data from the submitted form and update the user_profile object
        user_profile.linkedin_url = request.POST.get('linkedin_url')
        user_profile.github_url = request.POST.get('github_url')
        user_profile.portfolio_url = request.POST.get('portfolio_url')
        user_profile.save()
        messages.success(request, 'Professional links updated successfully!')
        return redirect('profile_view', username=username) # Redirect back to the profile page

    return redirect('profile_view', username=username)

def ats_checker_page(request):
    """
    Renders the ATS Resume Scan page.
    """
    user_id = request.session.get('user_id')
    if not user_id:
        # Redirect to login if user is not authenticated
        return redirect('user-login') 
    
    try:
        # We fetch the user object to pass to the template for the navbar
        user = UserRegister.objects.get(id=user_id)
        context = {'user': user}
        return render(request, 'ats_checker.html', context)
    except UserRegister.DoesNotExist:
        # Handle case where user_id in session is invalid
        return redirect('user-login')
    
@csrf_exempt # Temporarily disable CSRF for easier testing
def analyze_resume_api(request):
    if request.method == 'POST':
        resume_file = request.FILES.get('resume')
        job_description = request.POST.get('job_description')

        if not resume_file or not job_description:
            return JsonResponse({'error': 'Missing resume or job description.'}, status=400)

        mock_results = {
            "score": 87,
            "summary": "A strong match! Your resume aligns well with key requirements.",
            "strengths": [
                "Excellent alignment with 'Project Management' and 'Agile Methodologies'.",
                "Strong technical skills in Python and SQL are well-represented."
            ],
            "improvements": [
                "Consider adding specific metrics to your accomplishments (e.g., 'Increased efficiency by 20%').",
                "Tailor the summary section to more closely mirror the language of the job posting."
            ],
            "keywords": {
                "matched": ["Python", "SQL", "Agile", "Project Management"],
                "missing": ["WireShark", "Stakeholder Communication", "Budgeting"]
            }
        }
        
        return JsonResponse(mock_results)
    
    return JsonResponse({'error': 'This endpoint only supports POST requests.'}, status=405)

def extract_text_from_resume(resume_file):
    text = ""
    file_stream = io.BytesIO(resume_file.read())
    
    if resume_file.name.endswith('.pdf'):
        try:
            pdf_reader = PyPDF2.PdfReader(file_stream)
            for page in pdf_reader.pages:
                text += page.extract_text()
        except Exception as e:
            print(f"Error reading PDF: {e}")
            return None
            
    elif resume_file.name.endswith('.docx'):
        try:
            text = docx2txt.process(file_stream)
        except Exception as e:
            print(f"Error reading DOCX: {e}")
            return None
            
    else:
        try:
            text = file_stream.read().decode('utf-8')
        except Exception as e:
            print(f"Error reading file as text: {e}")
            return None

    return text
