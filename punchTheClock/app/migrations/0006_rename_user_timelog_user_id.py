# Generated by Django 4.0.4 on 2022-06-02 15:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_timelog_user'),
    ]

    operations = [
        migrations.RenameField(
            model_name='timelog',
            old_name='user',
            new_name='user_id',
        ),
    ]
