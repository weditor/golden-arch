# Generated by Django 3.0.3 on 2020-03-14 03:15

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('conference', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='conference',
            name='claim_user',
        ),
        migrations.AddField(
            model_name='conferencetopic',
            name='claim_time',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='conferencetopic',
            name='claim_user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='claim_conference_topics', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='conferencetopic',
            name='conference',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='conference.Conference'),
        ),
        migrations.AddField(
            model_name='conferencetopic',
            name='like_user',
            field=models.ManyToManyField(related_name='like_conference_topics', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='conferencetopic',
            name='creator',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
