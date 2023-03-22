# Generated by Django 4.1.4 on 2023-03-22 00:09

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("AppOko", "0019_remove_products_added_by_staff"),
    ]

    operations = [
        migrations.AddField(
            model_name="products",
            name="added_by_staff",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
