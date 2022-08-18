from django.db import models
# from django.contrib.auth.models import User
from App_auth.models import *
from datetime import date

group_regex = RegexValidator(regex=r"^[A-Za-z][A-Za-z0-9_]{7,29}$",
                             message=gettext_lazy('Need to be connected every word.'))


# Create your models here.
class PartnerRequestModel(models.Model):
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='activity_post_author')
    title = models.CharField(max_length=500, unique=True)
    groupName = models.CharField(validators=[group_regex], max_length=30, unique=True)
    type = models.CharField(max_length=100)
    total_participants = models.PositiveIntegerField(blank=False)
    project_duration = models.PositiveIntegerField(blank=False)
    location = models.CharField(max_length=500, blank=False)
    required_skills = models.CharField(max_length=800, blank=False)
    related_file = models.FileField(upload_to='project_info_files/', blank=True, null=True)
    description = models.TextField()
    application_deadline = models.DateTimeField()
    created_on = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=True)

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return f"{self.title}-{self.status}"


class PartnerApplicationModel(models.Model):
    activity = models.ForeignKey(PartnerRequestModel, on_delete=models.CASCADE, related_name='task')
    participant = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='participant')
    reason_of_participation = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return f"{self.activity.title}-{self.status}"


genders = (
    ('Male', 'Male'),
    ('Female', 'Female'),
    ('Third Gender', 'Third Gender'),
    ('Not Specified', 'Not Specified'),
)


class JobPostModel(models.Model):
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='job_post_author')
    job_title = models.CharField(max_length=500)
    company_name = models.CharField(max_length=500)
    position = models.CharField(max_length=400)
    category = models.CharField(max_length=500)
    work_type = models.CharField(max_length=100)
    total_vacancies = models.PositiveIntegerField(blank=False)
    location = models.CharField(max_length=500, blank=False)
    required_skills = models.CharField(max_length=800, blank=False)
    job_description = models.TextField()
    job_responsibilities = models.TextField()
    experience = models.CharField(max_length=100)
    gender_specification = models.CharField(choices=gender, max_length=100, default="Not Specified")
    application_deadline = models.DateTimeField()
    created_on = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=True)

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return f"{self.job_title}-{self.status}"


class JobApplicationModel(models.Model):
    applied_job = models.ForeignKey(JobPostModel, on_delete=models.CASCADE, related_name='job')
    candidate = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='job_candidate')
    reason_of_application = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=True)

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return f"{self.applied_job.job_title}-{self.status}"


class CircularModel(models.Model):
    circular_title = models.CharField(max_length=500)
    provider = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='circular_provider')
    circular = models.ImageField(upload_to='circulars')
    created_on = models.DateTimeField(auto_now_add=True)
    
    
class ResearchPaperModel(models.Model):
    title = models.CharField(max_length=500)
    author = models.CharField(max_length=500)
    preview = models.TextField()
    file = models.FileField(upload_to='research_papers')
    created_on = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=True)
