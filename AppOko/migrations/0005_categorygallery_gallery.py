# Generated by Django 4.0.3 on 2022-10-31 19:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('AppOko', '0004_remove_chapters_created_ad'),
    ]

    operations = [
        migrations.CreateModel(
            name='CategoryGallery',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=255)),
                ('is_active', models.IntegerField(default=1)),
            ],
        ),
        migrations.CreateModel(
            name='Gallery',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=255)),
                ('media_content', models.FileField(upload_to='')),
                ('description', models.CharField(blank=True, max_length=255, null=True)),
                ('customer', models.CharField(blank=True, max_length=255, null=True)),
                ('order_number', models.CharField(blank=True, max_length=255, null=True)),
                ('is_active', models.IntegerField(default=1)),
                ('type_of_product', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='AppOko.categorygallery')),
            ],
        ),
    ]
