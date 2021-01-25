"""techademics URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from myapp import views
from django.urls import include
from django.contrib.auth import views as authviews
from django.conf import settings
from django.conf.urls.static import static

# include is used to include the other url files from various applications.
# django.contrib.auth.views provides us with the prebuilt login and the logout views and they are really handy while using
# the login and logout features of the websites.
# django.conf.settings is used to import the settings file from the website main folder. We need access over these to import
# the MEDIA_URL and MEDIA_ROOT files.
# django.conf.urls.static is used to add the media files into this page.


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.indexView.as_view(), name='index'),
    path('accounts/login/', authviews.LoginView.as_view(template_name='registration/login.html'), name='login'),    #The page is redirected to as mentioned in login_redirect_url.
    path('accounts/logout/', authviews.LogoutView.as_view(template_name='myapp/index.html'), name='logout', kwargs={'next_page':'/'}),
    path('viewteam/', views.teamView.as_view(), name='team'),
    path('team/', include('myapp.urls')),
    path('allcourses/', views.coursesView.as_view(), name='courses'),
    path('allcourses/<int:pk>/', views.courseDetailView.as_view(), name='course_detail'),
    path('register/', views.register, name='register'),
    path('register/confirm/<int:pk>', views.registration_successful.as_view(), name='registration_successful'),
    path('contactus/', views.contactView.as_view(), name='contact'),
    path('courses/', include('myapp.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# The + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) is used to access the content of the MEDIA directory
# into the templates files.

