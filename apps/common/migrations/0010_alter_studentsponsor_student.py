# Generated by Django 5.0.6 on 2024-07-05 06:45

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0009_alter_studentsponsor_amount'),
    ]

    operations = [
        migrations.AlterField(
            model_name='studentsponsor',
            name='student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='sponsors', to='common.student'),
        ),
    ]
