# Generated by Django 4.0.3 on 2023-02-16 19:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('AppOko', '0007_projects_alter_customeruser_profile_pic'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='projects',
            options={'ordering': ['-number']},
        ),
    ]
