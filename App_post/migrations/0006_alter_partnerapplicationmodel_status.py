# Generated by Django 4.0.5 on 2022-06-18 07:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App_post', '0005_alter_jobapplicationmodel_status_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='partnerapplicationmodel',
            name='status',
            field=models.BooleanField(default=False),
        ),
    ]
