# Generated by Django 4.0.5 on 2022-06-19 02:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App_post', '0006_alter_partnerapplicationmodel_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='jobpostmodel',
            name='gender_specification',
            field=models.CharField(choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')], default='Not Specified', max_length=100),
        ),
    ]