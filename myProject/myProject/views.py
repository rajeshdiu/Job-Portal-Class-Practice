from urllib import request
from django.shortcuts import redirect,render
from django.http import HttpResponse
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash

from django.contrib.auth.hashers import check_password

from django.contrib import messages
from django.contrib.auth.hashers import make_password
from django.contrib import messages

from myApp.models import *


def signupPage(request):
    if request.method == "POST":
        user_name = request.POST.get('username')
        displayname = request.POST.get('display_name')
        mail = request.POST.get('email')
        pass_word = request.POST.get('password')
        usertype = request.POST.get('user_type')

        user = Custom_User.objects.create_user(username=user_name, password=pass_word)
        user.display_name = displayname
        user.email = mail
        user.user_type = usertype
        user.save()

        # Create corresponding profile
        if usertype == 'recruiter':
            RecruiterProfile.objects.create(user=user)
        elif usertype == 'jobseeker':
            JobSeekerProfile.objects.create(user=user)

        messages.success(request, "Account created successfully.")
        return redirect("signinPage")

    return render(request, 'signup.html')

def changePasswordPage(request):
    if request.method == 'POST':
        old_password = request.POST.get('old_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        if check_password(old_password, request.user.password):
            if new_password == confirm_password:
                # Perform your custom logic for changing the password here
                request.user.set_password(new_password)
                request.user.save()

                # Update the user's session to prevent them from being logged out
                update_session_auth_hash(request, request.user)

                messages.success(request, 'Password changed successfully!')
                return redirect('ProfilePage')
            else:
                messages.error(request, 'New Password and Confirm Password do not match.')
        else:
            messages.error(request, 'Old Password is incorrect.')

    return render(request, 'changepassword.html')

def logoutPage(request):

    logout(request)

    return redirect('signinPage')

def signinPage(request):

    if request.method == "POST":

        user_name= request.POST.get('username')
        password= request.POST.get('password')

        user = authenticate(username=user_name, password=password)

        print(user)

        if user:
            login(request,user)
            return redirect("dashboardPage")


    return render(request,'login.html')

@login_required
def dashboardPage(request):

    return render(request,"dashboard.html")

@login_required
def viewjobPage(request):

    job=job_model.objects.all()

    context={
        'job':job
    }
    return render(request,"viewjob.html",context)

@login_required
def add_job_Page(request):

    user = request.user

    if request.method == 'POST':

        jobTitle=request.POST.get('jobTitle')
        companyName=request.POST.get('companyName')
        location=request.POST.get('location')
        description=request.POST.get('description')

        job=job_model(
            job_title=jobTitle,
            company_name=companyName,
            location=location,
            description=description,
            job_creator=user,
        )
        job.save()

        return redirect("viewjobPage")
    

    return render(request,'Recruiter/Addjob.html')

@login_required
def deletePage(request,myid):

    job=job_model.objects.filter(id=myid)
    job.delete()

    return redirect("viewjobPage")

@login_required
def editPage(request,myid):

    job=job_model.objects.filter(id=myid)

    return render(request,'Recruiter/editJob.html',{'job':job})

from django.shortcuts import get_object_or_404

@login_required
def updatePage(request):
    user = request.user

    if request.method == 'POST':
        job_id = request.POST.get('jobid')
        job_title = request.POST.get('jobTitle')
        company_name = request.POST.get('companyName')
        location = request.POST.get('location')
        description = request.POST.get('description')

        # Retrieve the existing job instance
        job = get_object_or_404(job_model, id=job_id, job_creator=user)

        # Update the job fields
        job.job_title = job_title
        job.company_name = company_name
        job.location = location
        job.description = description

        # Save the changes
        job.save()

        return redirect("viewjobPage")

    return render(request, 'Recruiter/updateJob.html')


@login_required
def applyPage(request,myid):

    job=job_model.objects.filter(id=myid)
    

    return render(request,'JobSeeker/applyjob.html')


@login_required
def ProfilePage(request):
    
    user=request.user
    
    context = {
        'user': user
    }
    return render(request, 'profile.html', context)


@login_required

def EditProfilePage(request):
    context={
        'password_not_matched':"Password Not Matched",
        'Success_Message' : "Update Successfully"
    }
    user = request.user

    # Check if the user is authenticated
    if not user.is_authenticated:
        # Redirect or handle the situation appropriately
        return redirect('loginPage')
    if request.method == 'POST':
        user_id = request.POST.get("user_id")
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        username = request.POST.get("username")
        display_name = request.POST.get("display_name")
        email = request.POST.get("email")
        about = request.POST.get("about")
        image = request.FILES.get("image")
        skills = request.POST.get("skills")
        resume = request.FILES.get("resume")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        print(user_id, first_name, last_name, display_name, username, email, image, password, confirm_password,about)

        if password != confirm_password:
            messages.error(request, 'Password and Confirm Password Not Match')
            return redirect('EditProfilePage')
        
        if not check_password(password, user.password):
            messages.error(request, 'Wrong Password')
            return redirect('EditProfilePage')

        user.first_name = first_name
        user.last_name = last_name
        user.display_name = display_name
        user.email = email
        user.about=about

        # Update profile picture if provided
        if image:
            user.profile_pic = image

        user.save()

        messages.success(request, "Update Successfully")
        return redirect('ProfilePage')

    return render(request, 'Editprofile.html',context)

def Post_or_Applied_Job_Page(request):
    
    current_user=request.user
    
    if current_user.user_type == 'recruiter':
        
        posted_job = job_model.objects.filter(job_creator=current_user)
        
    context={
        'posted_job':posted_job
    }
    
    return render(request,'Recruiter/postedJob.html',context)



def Applied_Job_By_Applicants_Page(request):



    return render(request,'JobSeeker/AppliedJob.html')


