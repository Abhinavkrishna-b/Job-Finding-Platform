from django.shortcuts import render , redirect
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import *
from companyside.models import *
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.hashers import check_password
from django.contrib.auth.hashers import make_password



# Create your views here.
def Home(request):

    if request.method == 'GET':
        joblist = Joblist.objects.all()
        print(joblist)
        return render(request , 'home.html' ,{'job_list':joblist})
    
    return render(request, 'home.html')

def LandPage(request):
    return render(request,'landingpage.html')


@api_view(["GET","POST"])
def comanyRegister(request):  

    # print("iam mathav")
    if request.method == 'POST':
        email = request.POST.get('Email')
        company_name = request.POST.get('Company_name')
        location = request.POST.get('Company_location')
        password = request.POST.get('Password') 

        hashed_password = make_password(password) 

        #create and save the employee object
        CompanyRegister.objects.create(
                email = email,
                company_name = company_name,
                location = location,
                password = hashed_password,

        )
        print(f"New Company {company_name} add successfully")
        return render(request,'com_auth.html') 
                               
    return render(request,'com_auth.html') 


# @api_view(["GET","POST"])
# def companyLogin(request): 
    
#     print("iam mathav")
#     if request.method == 'POST':
#         email = request.POST.get('Email')
#         password = request.POST.get('password')

#         try:
#             user = CompanyRegister.objects.get(email=email, password=password)

#             request.session['company_id'] = user.id  # Storing company ID in session
#             company_name = user.company_name
#             print(company_name)
#             # joblist = Joblist.objects.get(company=company)
#             context = {'user_logged_in': True,'user': user,'company_name': company_name}
        
#             # return render(request, 'comDashboard.html',context)
#             return redirect('company_dashboard')

#         except CompanyRegister.DoesNotExist:
#             return render(request, 'com_auth.html', {'error': 'Invalid user credentials'})

#     return render(request, 'com_auth.html')



@api_view(["GET", "POST"])
def companyLogin(request):

    if request.method == 'POST':
        email = request.POST.get('Email')
        password = request.POST.get('password')
        try:
            user = CompanyRegister.objects.get(email=email)

            # Check if the password matches the stored hashed password
            if check_password(password, user.password):
                request.session['company_id'] = user.id  # Store company ID in session
                # company_name = user.company_name

                # context = {'user_logged_in': True, 'user': user, 'company_name': company_name}
                return redirect('company_dashboard')

            else:
                return render(request, 'com_auth.html', {'error': 'Invalid credentials'})

        except CompanyRegister.DoesNotExist:
            return render(request, 'com_auth.html', {'error': 'Invalid email or password'})

    return render(request, 'com_auth.html')



@api_view(['GET','POST'])
def userRegister(request):

    print("user register")
    if request.method == 'POST':
        username = request.POST.get('user_name')
        email = request.POST.get('Email')
        ph_number = request.POST.get('ph_number')
        password = request.POST.get('Password')
        
        hashed_password = make_password(password) 

        UserRegister.objects.create(
            username = username,
            email = email,
            phone_number = ph_number,
            password = hashed_password,
        )
        print(f"New User {username} add successfully")
        return render(request,'user_auth.html')

    return render(request,'user_auth.html') 



@api_view(['GET','POST'])
def userLogin(request):

    print("user login")
    if request.method == 'POST':
        email = request.POST.get('Email')
        password = request.POST.get('password')
        try:
            user = UserRegister.objects.get(email=email)

            if check_password(password, user.password):
                request.session['user_id'] = user.id

                return redirect('user_dashboard')
            
            else:
                return render(request, 'user_auth.html', {'error': 'Invalid credentials'})
            
        except UserRegister.DoesNotExist:
            return render(request, 'user_auth.html', {'error': 'Invalid email or password'})
        
    return render(request, 'user_auth.html')