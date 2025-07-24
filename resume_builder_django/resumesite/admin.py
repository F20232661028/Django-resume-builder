from django.contrib import admin
from .models import Resume, Education, Experience, Skill, ResumeSkill

admin.site.register(Resume)
admin.site.register(Education)
admin.site.register(Experience)
admin.site.register(Skill)
admin.site.register(ResumeSkill)
