# Generated by Django 4.0.6 on 2022-08-17 06:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dataservice', '0010_alter_questions_course'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='course',
            name='teacher',
        ),
        migrations.RemoveField(
            model_name='enrollmet',
            name='course',
        ),
        migrations.RemoveField(
            model_name='enrollmet',
            name='student',
        ),
        migrations.RemoveField(
            model_name='exam',
            name='course',
        ),
        migrations.RemoveField(
            model_name='questions',
            name='course',
        ),
        migrations.DeleteModel(
            name='Attendance',
        ),
        migrations.DeleteModel(
            name='Course',
        ),
        migrations.DeleteModel(
            name='Enrollmet',
        ),
        migrations.DeleteModel(
            name='Exam',
        ),
        migrations.DeleteModel(
            name='Questions',
        ),
        migrations.DeleteModel(
            name='Quiz',
        ),
        migrations.DeleteModel(
            name='Student',
        ),
        migrations.DeleteModel(
            name='Teacher',
        ),
    ]
