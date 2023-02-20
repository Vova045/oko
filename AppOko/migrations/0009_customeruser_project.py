# Generated by Django 4.1.4 on 2023-02-19 23:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("AppOko", "0008_alter_projects_options_alter_customuser_user_type_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="customeruser",
            name="project",
            field=models.OneToOneField(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="AppOko.projects",
            ),
        ),
    ]