# Generated by Django 2.2.1 on 2019-07-13 10:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('applications', '0008_remove_schooltype_amount_allocated'),
    ]

    operations = [
        migrations.AddField(
            model_name='schooltype',
            name='amount_allocated',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
