from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Resume, Education, Experience, Skill, ResumeSkill, Certification, Project
from .forms import ResumeForm, ExperienceFormSet, EducationFormSet, SkillFormSet, CertificationFormSet, ProjectFormSet
from django.views.generic.edit import FormView
from django.db import transaction
from django.contrib import messages
from django.http import HttpResponseRedirect
from .google_drive_utils import upload_resume_to_drive
import os
from django.core.mail import EmailMessage
from django import forms

# --- Existing function-based views ---
def home(request):
	return render(request, 'home.html', {})

# --- Class-based CRUD views for Resume ---
class ResumeListView(LoginRequiredMixin, ListView):
    model = Resume
    template_name = 'resume_list.html'
    context_object_name = 'resumes'

    def get_queryset(self):
        return Resume.objects.filter(user=self.request.user)  # type: ignore

class ResumeDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Resume
    template_name = 'resume_detail.html'
    context_object_name = 'resume'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        resume = self.get_object()
        context['experiences'] = resume.experiences.all().order_by('-start_date')
        context['educations'] = resume.educations.all().order_by('-end_year')
        context['skills'] = [rs.skill.name for rs in resume.resume_skills.all()]
        return context

    def test_func(self):
        resume = self.get_object()
        return resume.user == self.request.user

class ResumeCreateView(LoginRequiredMixin, FormView):
    template_name = 'resume_form.html'
    form_class = ResumeForm
    success_url = reverse_lazy('resume-list')

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        experience_formset = ExperienceFormSet(queryset=Experience.objects.none(), prefix='experience')
        education_formset = EducationFormSet(queryset=Education.objects.none(), prefix='education')
        skill_formset = SkillFormSet(queryset=Skill.objects.none(), prefix='skill')
        certification_formset = CertificationFormSet(queryset=Certification.objects.none(), prefix='certification')
        project_formset = ProjectFormSet(queryset=Project.objects.none(), prefix='project')
        # Ensure at least one form for each formset
        if experience_formset.total_form_count() == 0:
            experience_formset = ExperienceFormSet(queryset=Experience.objects.none(), prefix='experience', initial=[{}])
        if education_formset.total_form_count() == 0:
            education_formset = EducationFormSet(queryset=Education.objects.none(), prefix='education', initial=[{}])
        if skill_formset.total_form_count() == 0:
            skill_formset = SkillFormSet(queryset=Skill.objects.none(), prefix='skill', initial=[{}])
        if certification_formset.total_form_count() == 0:
            certification_formset = CertificationFormSet(queryset=Certification.objects.none(), prefix='certification', initial=[{}])
        if project_formset.total_form_count() == 0:
            project_formset = ProjectFormSet(queryset=Project.objects.none(), prefix='project', initial=[{}])
        return render(request, self.template_name, {
            'form': form,
            'experience_formset': experience_formset,
            'education_formset': education_formset,
            'skill_formset': skill_formset,
            'certification_formset': certification_formset,
            'project_formset': project_formset,
        })

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        experience_formset = ExperienceFormSet(request.POST, queryset=Experience.objects.none(), prefix='experience')
        education_formset = EducationFormSet(request.POST, queryset=Education.objects.none(), prefix='education')
        skill_formset = SkillFormSet(request.POST, queryset=Skill.objects.none(), prefix='skill')
        certification_formset = CertificationFormSet(request.POST, queryset=Certification.objects.none(), prefix='certification')
        project_formset = ProjectFormSet(request.POST, queryset=Project.objects.none(), prefix='project')
        if (form.is_valid() and experience_formset.is_valid() and education_formset.is_valid() and
            skill_formset.is_valid() and certification_formset.is_valid() and project_formset.is_valid()):
            with transaction.atomic():
                resume = form.save(commit=False)
                resume.user = request.user
                resume.save()
                # Save experiences
                for exp_form in experience_formset:
                    if exp_form.cleaned_data and not exp_form.cleaned_data.get('DELETE', False):
                        exp = exp_form.save(commit=False)
                        exp.resume = resume
                        exp.save()
                # Save educations
                for edu_form in education_formset:
                    if edu_form.cleaned_data and not edu_form.cleaned_data.get('DELETE', False):
                        edu = edu_form.save(commit=False)
                        edu.resume = resume
                        edu.save()
                # Save skills
                for skill_form in skill_formset:
                    if skill_form.cleaned_data and not skill_form.cleaned_data.get('DELETE', False):
                        skill_name = skill_form.cleaned_data['name']
                        skill, created = Skill.objects.get_or_create(name=skill_name)
                        ResumeSkill.objects.get_or_create(resume=resume, skill=skill)
                # Save certifications
                for cert_form in certification_formset:
                    if cert_form.cleaned_data and not cert_form.cleaned_data.get('DELETE', False):
                        cert = cert_form.save(commit=False)
                        cert.resume = resume
                        cert.save()
                # Save projects
                for proj_form in project_formset:
                    if proj_form.cleaned_data and not proj_form.cleaned_data.get('DELETE', False):
                        proj = proj_form.save(commit=False)
                        proj.resume = resume
                        proj.save()
            return redirect(self.success_url)
        return render(request, self.template_name, {
            'form': form,
            'experience_formset': experience_formset,
            'education_formset': education_formset,
            'skill_formset': skill_formset,
            'certification_formset': certification_formset,
            'project_formset': project_formset,
        })

class ResumeUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Resume
    fields = ['title', 'summary', 'contact_email', 'contact_phone', 'contact_address']
    template_name = 'resume_form.html'
    success_url = reverse_lazy('resume-list')

    def test_func(self):
        resume = self.get_object()
        return resume.user == self.request.user

class ResumeDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Resume
    template_name = 'resume_confirm_delete.html'
    success_url = reverse_lazy('resume-list')

    def test_func(self):
        resume = self.get_object()
        return resume.user == self.request.user

# --- Education CRUD views ---
class EducationCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Education
    fields = ['school', 'degree', 'start_year', 'end_year', 'score']
    template_name = 'education_form.html'

    def form_valid(self, form):
        resume = get_object_or_404(Resume, pk=self.kwargs['resume_id'])
        form.instance.resume = resume
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('resume-detail', kwargs={'pk': self.kwargs['resume_id']})

    def test_func(self):
        resume = get_object_or_404(Resume, pk=self.kwargs['resume_id'])
        return resume.user == self.request.user

class EducationUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Education
    fields = ['school', 'degree', 'start_year', 'end_year', 'score']
    template_name = 'education_form.html'

    def get_success_url(self):
        return reverse_lazy('resume-detail', kwargs={'pk': self.object.resume.pk})

    def test_func(self):
        return self.get_object().resume.user == self.request.user

class EducationDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Education
    template_name = 'education_confirm_delete.html'

    def get_success_url(self):
        return reverse_lazy('resume-detail', kwargs={'pk': self.object.resume.pk})

    def test_func(self):
        return self.get_object().resume.user == self.request.user

# --- Experience CRUD views ---
class ExperienceCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Experience
    fields = ['job_title', 'company', 'start_date', 'end_date', 'description']
    template_name = 'experience_form.html'

    def form_valid(self, form):
        resume = get_object_or_404(Resume, pk=self.kwargs['resume_id'])
        form.instance.resume = resume
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('resume-detail', kwargs={'pk': self.kwargs['resume_id']})

    def test_func(self):
        resume = get_object_or_404(Resume, pk=self.kwargs['resume_id'])
        return resume.user == self.request.user

class ExperienceUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Experience
    fields = ['job_title', 'company', 'start_date', 'end_date', 'description']
    template_name = 'experience_form.html'

    def get_success_url(self):
        return reverse_lazy('resume-detail', kwargs={'pk': self.object.resume.pk})

    def test_func(self):
        return self.get_object().resume.user == self.request.user

class ExperienceDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Experience
    template_name = 'experience_confirm_delete.html'

    def get_success_url(self):
        return reverse_lazy('resume-detail', kwargs={'pk': self.object.resume.pk})

    def test_func(self):
        return self.get_object().resume.user == self.request.user

def resume_upload_drive(request, pk):
    resume = get_object_or_404(Resume, pk=pk, user=request.user)
    # Assume the PDF is generated and saved as output_resume.pdf in the project directory
    pdf_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'output_resume.pdf')
    if not os.path.exists(pdf_path):
        messages.error(request, 'Resume PDF not found. Please generate or download your resume first.')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    success, result = upload_resume_to_drive(request.user, pdf_path, filename=f'{resume.title}.pdf')
    if success:
        messages.success(request, f'Resume uploaded to Google Drive! <a href="{result}" target="_blank">View in Drive</a>')
    else:
        messages.error(request, f'Failed to upload to Google Drive: {result}')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

class EmailResumeForm(forms.Form):
    recipient = forms.EmailField(label='Recipient Email', widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Recipient email'}))

def email_resume(request, pk):
    resume = get_object_or_404(Resume, pk=pk, user=request.user)
    pdf_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'output_resume.pdf')
    if request.method == 'POST':
        form = EmailResumeForm(request.POST)
        if form.is_valid():
            recipient = form.cleaned_data['recipient']
            email = EmailMessage(
                subject=f"Your Resume from ProResume Builder",
                body=f"Hi,\n\nPlease find attached the resume generated using ProResume Builder.\n\nBest regards,\nThe ProResume Builder Team",
                from_email=request.user.email,
                to=[recipient],
            )
            if os.path.exists(pdf_path):
                email.attach(f'{resume.title}.pdf', open(pdf_path, 'rb').read(), 'application/pdf')
                email.send()
                messages.success(request, f'Resume sent to {recipient}!')
            else:
                messages.error(request, 'Resume PDF not found. Please generate or download your resume first.')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    else:
        form = EmailResumeForm()
    return render(request, 'email_resume.html', {'form': form, 'resume': resume})
