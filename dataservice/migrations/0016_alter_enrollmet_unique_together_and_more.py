# Generated by Django 4.0.6 on 2022-08-18 12:09

import datetime
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('dataservice', '0015_alter_enrollmet_unique_together'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='enrollmet',
            unique_together=set(),
        ),
        migrations.RemoveField(
            model_name='questions',
            name='Total_mark',
        ),
        migrations.AddField(
            model_name='attendance',
            name='attend',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='course',
            name='exam_date',
            field=models.DateField(default=datetime.datetime(2022, 8, 18, 12, 9, 29, 898733, tzinfo=utc)),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='attendance',
            name='student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dataservice.student'),
        ),
        migrations.AlterField(
            model_name='enrollmet',
            name='course',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='enrollment', to='dataservice.course'),
        ),
        migrations.DeleteModel(
            name='Exam',
        ),
    ]
