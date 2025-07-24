from django.urls import path
from . import views
from django.shortcuts import redirect

urlpatterns = [
    path('resume/', views.home, name="home"),
    path('', lambda request: redirect('resumes/')),

    # Resume CRUD URLs
    path('resumes/', views.ResumeListView.as_view(), name='resume-list'),
    path('resumes/create/', views.ResumeCreateView.as_view(), name='resume-create'),
    path('resumes/<int:pk>/', views.ResumeDetailView.as_view(), name='resume-detail'),
    path('resumes/<int:pk>/update/', views.ResumeUpdateView.as_view(), name='resume-update'),
    path('resumes/<int:pk>/delete/', views.ResumeDeleteView.as_view(), name='resume-delete'),
    path('resumes/<int:pk>/upload-drive/', views.resume_upload_drive, name='resume-upload-drive'),
    path('resumes/<int:pk>/email/', views.email_resume, name='resume-email'),

    # Education CRUD URLs (nested under Resume)
    path('resumes/<int:resume_id>/education/add/', views.EducationCreateView.as_view(), name='education-add'),
    path('resumes/<int:resume_id>/education/<int:pk>/edit/', views.EducationUpdateView.as_view(), name='education-edit'),
    path('resumes/<int:resume_id>/education/<int:pk>/delete/', views.EducationDeleteView.as_view(), name='education-delete'),

    # Experience CRUD URLs (nested under Resume)
    path('resumes/<int:resume_id>/experience/add/', views.ExperienceCreateView.as_view(), name='experience-add'),
    path('resumes/<int:resume_id>/experience/<int:pk>/edit/', views.ExperienceUpdateView.as_view(), name='experience-edit'),
    path('resumes/<int:resume_id>/experience/<int:pk>/delete/', views.ExperienceDeleteView.as_view(), name='experience-delete'),
]
