# Generated by Django 2.2.1 on 2020-01-11 12:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounting', '0011_allocationdetail_award_period'),
    ]

    operations = [
        migrations.AlterField(
            model_name='financialyear',
            name='end_date',
            field=models.IntegerField(default=2021),
        ),
        migrations.AlterField(
            model_name='financialyear',
            name='start_date',
            field=models.IntegerField(default=2020),
        ),
    ]
