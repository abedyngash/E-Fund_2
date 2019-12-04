# Generated by Django 2.2.1 on 2019-06-22 09:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounting', '0002_allocationdetail'),
        ('applications', '0002_auto_20190620_1146'),
    ]

    operations = [
        migrations.CreateModel(
            name='Applicant',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=200)),
                ('last_name', models.CharField(max_length=200)),
                ('gender', models.CharField(choices=[('male', 'Male'), ('female', 'Female')], max_length=200)),
                ('family_status', models.CharField(choices=[('orphan', 'Total Orphan'), ('single_parent', 'Single Parent (Without Source of Income)'), ('partial_orphan', 'Partial Orphan (Mother/Father Alive) Without Source of Income'), ('both_parents', 'Both Parents Alive Without Source of Income')], max_length=200)),
                ('name_of_gurdian', models.CharField(max_length=150)),
                ('contact_of_gurdian', models.CharField(max_length=150)),
                ('disability_status', models.BooleanField(default=False)),
                ('disability_desc', models.CharField(blank=True, max_length=250, null=True)),
                ('school_name', models.CharField(max_length=250)),
                ('school_email', models.EmailField(max_length=254)),
                ('adm_number', models.CharField(max_length=100)),
                ('class_of_study', models.IntegerField()),
                ('award_status', models.CharField(choices=[('not_set', 'Not Set'), ('awarded', 'Awarded'), ('not_awarded', 'Not Awarded')], default='not_set', max_length=200)),
                ('discipline', models.CharField(choices=[('excellent', 'Excellent'), ('very_good', 'Very Good'), ('good', 'Good'), ('poor', 'Poor'), ('very_poor', 'Very Poor')], max_length=250, null=True)),
                ('financial_year', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounting.FinancialYear')),
                ('school_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='applications.SchoolType')),
                ('subcounty', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='applicants', to='applications.Subcounty')),
                ('sublocation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='applicants', to='applications.Sublocation')),
                ('ward', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='applicants', to='applications.Ward')),
            ],
        ),
    ]
