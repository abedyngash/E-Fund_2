# Generated by Django 2.2.1 on 2020-01-21 10:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('applications', '0020_auto_20200114_1133'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='school',
            name='email',
        )
    ]
