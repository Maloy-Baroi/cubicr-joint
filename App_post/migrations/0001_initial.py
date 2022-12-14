# Generated by Django 4.0.5 on 2022-06-17 15:06

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='PartnerRequestModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=500, unique=True)),
                ('type', models.CharField(max_length=100)),
                ('total_participants', models.PositiveIntegerField()),
                ('project_duration', models.PositiveIntegerField()),
                ('location', models.CharField(max_length=500)),
                ('required_skills', models.CharField(max_length=800)),
                ('related_file', models.FileField(blank=True, null=True, upload_to='project_info_files')),
                ('description', models.TextField()),
                ('application_deadline', models.DateTimeField()),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('status', models.BooleanField(default=False)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='activity_post_author', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-created_on'],
            },
        ),
        migrations.CreateModel(
            name='PartnerApplicationModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reason_of_participation', models.TextField()),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('status', models.BooleanField(default=False)),
                ('activity', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='task', to='App_post.partnerrequestmodel')),
                ('participant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='participant', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-created_on'],
            },
        ),
        migrations.CreateModel(
            name='JobPostModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('job_title', models.CharField(max_length=500)),
                ('company_name', models.CharField(max_length=500)),
                ('position', models.CharField(max_length=400)),
                ('category', models.CharField(max_length=500)),
                ('work_type', models.CharField(max_length=100)),
                ('total_vacancies', models.PositiveIntegerField()),
                ('location', models.CharField(max_length=500)),
                ('required_skills', models.CharField(max_length=800)),
                ('job_description', models.TextField()),
                ('job_responsibilities', models.TextField()),
                ('experience', models.CharField(max_length=100)),
                ('gender_specification', models.CharField(default='Not Specified', max_length=100)),
                ('application_deadline', models.DateTimeField()),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('status', models.BooleanField(default=False)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='job_post_author', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-created_on'],
            },
        ),
        migrations.CreateModel(
            name='JobApplicationModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reason_of_application', models.TextField()),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('status', models.BooleanField(default=False)),
                ('applied_job', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='job', to='App_post.jobpostmodel')),
                ('candidate', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='job_candidate', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-created_on'],
            },
        ),
        migrations.CreateModel(
            name='CircularModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('circular_title', models.CharField(max_length=500)),
                ('circular', models.ImageField(upload_to='circulars')),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('provider', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='circular_provider', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
