
from django.contrib import admin
from django.urls import path
from myProject.views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',signupPage,name='signupPage'),
    path('logoutPage/',logoutPage,name='logoutPage'),
    path('signinPage/',signinPage,name='signinPage'),
    path('dashboardPage/',dashboardPage,name='dashboardPage'),
    path('viewjobPage/',viewjobPage,name='viewjobPage'),
    path('add_job_Page/',add_job_Page,name='add_job_Page'),
    path('deletePage/<str:myid>',deletePage,name='deletePage'),
    path('editPage/<str:myid>',editPage,name='editPage'),
    path('updatePage/',updatePage,name='updatePage'),
    path('applyPage/<str:myid>',applyPage,name='applyPage'),
    path('ProfilePage/',ProfilePage,name='ProfilePage'),
    path('EditProfilePage/',EditProfilePage,name='EditProfilePage'),
    path('changePasswordPage/',changePasswordPage,name='changePasswordPage'),
    path('Post_or_Applied_Job_Page/',Post_or_Applied_Job_Page,name='Post_or_Applied_Job_Page'),
    path('Applied_Job_By_Applicants_Page/',Applied_Job_By_Applicants_Page,name='Applied_Job_By_Applicants_Page'),
    path('applicant_list/<str:myid>',applicant_list,name='applicant_list'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
