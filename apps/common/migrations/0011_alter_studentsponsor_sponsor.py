# Generated by Django 5.0.6 on 2024-07-05 10:41

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0010_alter_studentsponsor_student'),
    ]

    operations = [
        migrations.AlterField(
            model_name='studentsponsor',
            name='sponsor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='students', to='common.sponsor'),
        ),
    ]
