from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Resume(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='resumes')
    title = models.CharField(max_length=100)
    summary = models.TextField()
    contact_email = models.EmailField()
    contact_phone = models.CharField(max_length=20)
    contact_address = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({getattr(self.user, 'username', str(self.user))})"

class Education(models.Model):
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE, related_name='educations')
    school = models.CharField(max_length=100)
    degree = models.CharField(max_length=100)
    start_year = models.PositiveIntegerField()
    end_year = models.PositiveIntegerField()
    score = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return f"{self.degree} at {self.school}"

class Experience(models.Model):
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE, related_name='experiences')
    job_title = models.CharField(max_length=100)
    company = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    description = models.TextField()

    def __str__(self):
        return f"{self.job_title} at {self.company}"

class Skill(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class ResumeSkill(models.Model):
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE, related_name='resume_skills')
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE, related_name='resume_skills')
    proficiency = models.CharField(max_length=50, blank=True)  # e.g., Beginner, Intermediate, Expert

    class Meta:
        unique_together = ('resume', 'skill')

class Certification(models.Model):
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE, related_name='certifications')
    name = models.CharField(max_length=100)
    authority = models.CharField(max_length=100)
    license_number = models.CharField(max_length=100, blank=True)
    url = models.URLField(blank=True)
    date_obtained = models.DateField()

    def __str__(self):
        return f"{self.name} ({self.authority})"

class Project(models.Model):
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE, related_name='projects')
    title = models.CharField(max_length=100)
    description = models.TextField()
    link = models.URLField(blank=True)
    technologies = models.CharField(max_length=200, blank=True)
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.title
