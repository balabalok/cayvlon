# Generated by Django 3.0.5 on 2020-04-17 09:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rateit', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='ip_rate',
            name='his_vote',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
