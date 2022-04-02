# Generated by Django 4.0.3 on 2022-03-29 22:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('LaunchDataTracker', '0008_alter_payload_model_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='payload',
            name='connected',
            field=models.BooleanField(default=False, verbose_name='Connected'),
        ),
        migrations.AddField(
            model_name='peripheralstatus',
            name='connected',
            field=models.BooleanField(default=False),
        ),
    ]
