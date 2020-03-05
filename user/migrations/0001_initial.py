# Generated by Django 3.0.3 on 2020-03-05 02:30

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='HxUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('email', models.EmailField(max_length=255, unique=True, verbose_name='email address')),
                ('name', models.CharField(blank=True, default='', max_length=255)),
                ('is_active', models.BooleanField(default=True)),
                ('is_admin', models.BooleanField(default=False)),
                ('date_of_enter', models.DateField()),
                ('date_of_leave', models.DateField(default=None, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
