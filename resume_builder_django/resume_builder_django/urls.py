from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', lambda request: redirect('accounts/login/')),  # Redirect root to login
    path('resumes/', include('resumesite.urls')),
    # Use allauth for accounts (login, signup, social login, etc.)
    path('accounts/', include('allauth.urls')),
    path('accounts/profile/', lambda request: redirect('/resumes/')),
]