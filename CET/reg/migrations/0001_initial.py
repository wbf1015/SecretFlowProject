# Generated by Django 4.1 on 2023-08-01 10:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('exam', '0001_initial'),
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ExamReg',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('is_commit', models.BooleanField(default=False)),
                ('exam_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='exam.exam')),
                ('student_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='user.student')),
            ],
        ),
    ]
