from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column
import re
from django.core.exceptions import ValidationError
from .models import Resume, Experience, Education, Skill, ResumeSkill, Certification, Project
from django.forms import modelformset_factory, BaseModelFormSet
import datetime

class ResumeForm(forms.ModelForm):
	class Meta:
		model = Resume
		fields = ['title', 'summary', 'contact_email', 'contact_phone', 'contact_address']
		widgets = {
			'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Resume Title'}),
			'summary': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Brief professional summary...'}),
			'contact_email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
			'contact_phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone', 'pattern': r'^\\+?1?\\d{9,15}$', 'title': 'Enter a valid phone number (9-15 digits, may start with +)'}),
			'contact_address': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Address'}),
		}
		help_texts = {
			'contact_phone': 'Enter a valid phone number (9-15 digits, may start with +).',
			'contact_email': 'Enter a valid email address.',
		}

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.form_method = 'post'
		self.helper.layout = Layout(
			Row(
				Column('title', css_class='form-group col-md-6 mb-0'),
				Column('contact_email', css_class='form-group col-md-6 mb-0'),
			),
			Row(
				Column('contact_phone', css_class='form-group col-md-6 mb-0'),
				Column('contact_address', css_class='form-group col-md-6 mb-0'),
			),
			'summary',
			Submit('submit', 'Save Resume', css_class='btn-success')
		)

	def clean_contact_phone(self):
		phone = self.cleaned_data['contact_phone']
		if not re.match(r'^\+?1?\d{9,15}$', phone):
			raise ValidationError("Enter a valid phone number (9-15 digits, may start with +).")
		return phone

	def clean_contact_email(self):
		email = self.cleaned_data['contact_email']
		if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
			raise ValidationError("Enter a valid email address.")
		return email

class ExperienceForm(forms.ModelForm):
    class Meta:
        model = Experience
        fields = ['job_title', 'company', 'start_date', 'end_date', 'description']
        widgets = {
            'job_title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., Software Engineer'}),
            'company': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., Google'}),
            'start_date': forms.DateInput(attrs={'type': 'text', 'class': 'form-control flatpickr', 'placeholder': 'YYYY-MM-DD'}),
            'end_date': forms.DateInput(attrs={'type': 'text', 'class': 'form-control flatpickr', 'placeholder': 'YYYY-MM-DD'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Describe your responsibilities and achievements...'}),
        }
        help_texts = {
            'job_title': 'Enter your job title (e.g., Software Engineer).',
            'company': 'Enter the company name where you worked.',
            'start_date': 'Enter the start date in YYYY-MM-DD format (e.g., 2023-01-15).',
            'end_date': 'Enter the end date in YYYY-MM-DD format (e.g., 2024-05-30), or leave blank if still employed.',
            'description': 'Describe your responsibilities and achievements in this role.',
        }

    def clean(self):
        cleaned_data = super().clean()
        if self.cleaned_data.get('DELETE', False):
            return cleaned_data
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')
        if start_date and end_date and end_date < start_date:
            raise ValidationError('End date cannot be before start date.')
        for field in ['job_title', 'company', 'description']:
            value = cleaned_data.get(field, '').strip()
            if not value:
                raise ValidationError(f'{field.replace("_", " ").capitalize()} is required.')
        return cleaned_data

class EducationForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.fields['start_year'].initial:
            self.fields['start_year'].initial = 2015
        if not self.fields['end_year'].initial:
            self.fields['end_year'].initial = 2016

    class Meta:
        model = Education
        fields = ['school', 'degree', 'start_year', 'end_year', 'score']
        widgets = {
            'school': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., MIT'}),
            'degree': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., BSc Computer Science'}),
            'start_year': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Start Year', 'min': 1900, 'max': 2100}),
            'end_year': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'End Year', 'min': 1900, 'max': 2100}),
            'score': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., 3.8/4.0 or 85%'}),
        }
        help_texts = {
            'school': 'Enter the name of your school or university.',
            'degree': 'Enter your degree (e.g., BSc Computer Science).',
            'start_year': 'Enter the start year (e.g., 2018).',
            'end_year': 'Enter the end year (e.g., 2022).',
            'score': 'Enter your score, GPA, or percentage (optional).',
        }

    def clean(self):
        cleaned_data = super().clean()
        if self.cleaned_data.get('DELETE', False):
            return cleaned_data
        start_year = cleaned_data.get('start_year')
        end_year = cleaned_data.get('end_year')
        if start_year and end_year and end_year < start_year:
            raise ValidationError('End year cannot be before start year.')
        for field in ['school', 'degree']:
            value = cleaned_data.get(field, '').strip()
            if not value:
                raise ValidationError(f'{field.replace("_", " ").capitalize()} is required.')
        return cleaned_data

class SkillForm(forms.ModelForm):
    class Meta:
        model = Skill
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., Python'}),
        }
        help_texts = {
            'name': 'Enter a skill (e.g., Python, Project Management).',
        }

    def clean_name(self):
        name = self.cleaned_data['name'].strip()
        if not name:
            raise ValidationError('Skill name is required.')
        return name

class CertificationForm(forms.ModelForm):
    class Meta:
        model = Certification
        fields = ['name', 'authority', 'license_number', 'url', 'date_obtained']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., AWS Certified Solutions Architect'}),
            'authority': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., Amazon'}),
            'license_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., 123456'}),
            'url': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'Certification URL (optional)'}),
            'date_obtained': forms.DateInput(attrs={'type': 'text', 'class': 'form-control flatpickr', 'placeholder': 'YYYY-MM-DD'}),
        }
        help_texts = {
            'name': 'Enter the name of the certification (e.g., AWS Certified Solutions Architect).',
            'authority': 'Enter the issuing authority (e.g., Amazon).',
            'license_number': 'Enter the license number (optional).',
            'url': 'Enter the certification URL (optional).',
            'date_obtained': 'Enter the date you obtained the certification (YYYY-MM-DD).',
        }

    def clean(self):
        cleaned_data = super().clean()
        if self.cleaned_data.get('DELETE', False):
            return cleaned_data
        for field in ['name', 'authority', 'date_obtained']:
            value = cleaned_data.get(field, '').strip() if isinstance(cleaned_data.get(field), str) else cleaned_data.get(field)
            if not value:
                raise ValidationError(f'{field.replace("_", " ").capitalize()} is required.')
        return cleaned_data

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['title', 'description', 'link', 'technologies', 'start_date', 'end_date']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., Portfolio Website'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Describe the project, your role, and achievements...'}),
            'link': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'Project URL (optional)'}),
            'technologies': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., Django, React, AWS'}),
            'start_date': forms.DateInput(attrs={'type': 'text', 'class': 'form-control flatpickr', 'placeholder': 'YYYY-MM-DD'}),
            'end_date': forms.DateInput(attrs={'type': 'text', 'class': 'form-control flatpickr', 'placeholder': 'YYYY-MM-DD'}),
        }
        help_texts = {
            'title': 'Enter the project title (e.g., Portfolio Website).',
            'description': 'Describe the project, your role, and achievements.',
            'link': 'Enter the project URL (optional).',
            'technologies': 'List technologies used (comma-separated).',
            'start_date': 'Enter the project start date (YYYY-MM-DD).',
            'end_date': 'Enter the project end date (YYYY-MM-DD), or leave blank if ongoing.',
        }

    def clean(self):
        cleaned_data = super().clean()
        if self.cleaned_data.get('DELETE', False):
            return cleaned_data
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')
        if start_date and end_date and end_date < start_date:
            raise ValidationError('End date cannot be before start date.')
        for field in ['title', 'description', 'start_date']:
            value = cleaned_data.get(field, '').strip() if isinstance(cleaned_data.get(field), str) else cleaned_data.get(field)
            if not value:
                raise ValidationError(f'{field.replace("_", " ").capitalize()} is required.')
        return cleaned_data

# Custom BaseModelFormSet to skip validation for forms marked for deletion
class BaseSkipDeleteFormSet(BaseModelFormSet):
	def clean(self):
		if any(self.errors):
			return
		for form in self.forms:
			if self.can_delete and self._should_delete_form(form):
				continue
			if hasattr(form, 'clean'):
				form.clean()

ExperienceFormSet = modelformset_factory(
	Experience, form=ExperienceForm, extra=0, can_delete=True,
	formset=BaseSkipDeleteFormSet,
	widgets={'DELETE': forms.CheckboxInput(attrs={'class': 'form-check-input'})},
)
EducationFormSet = modelformset_factory(
	Education, form=EducationForm, extra=0, can_delete=True,
	formset=BaseSkipDeleteFormSet,
	widgets={'DELETE': forms.CheckboxInput(attrs={'class': 'form-check-input'})},
)
SkillFormSet = modelformset_factory(
	Skill, form=SkillForm, extra=0, can_delete=True,
	formset=BaseSkipDeleteFormSet,
	widgets={'DELETE': forms.CheckboxInput(attrs={'class': 'form-check-input'})},
)
CertificationFormSet = modelformset_factory(
    Certification, form=CertificationForm, extra=0, can_delete=True,
    formset=BaseSkipDeleteFormSet,
)
ProjectFormSet = modelformset_factory(
    Project, form=ProjectForm, extra=0, can_delete=True,
    formset=BaseSkipDeleteFormSet,
)
# CertificationFormSet can be added similarly if you have a Certification model