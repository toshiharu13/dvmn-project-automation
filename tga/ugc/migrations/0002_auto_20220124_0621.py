# Generated by Django 2.2.7 on 2022-01-24 06:21

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ugc', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='students',
            name='student_level',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='students', to='ugc.StudentLevels', verbose_name='Уровень ученика'),
        ),
    ]