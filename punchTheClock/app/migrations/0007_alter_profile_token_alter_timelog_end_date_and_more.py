# Generated by Django 4.0.4 on 2022-06-21 22:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_rename_user_timelog_user_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='token',
            field=models.BinaryField(blank=True, unique=True, verbose_name='API Token'),
        ),
        migrations.AlterField(
            model_name='timelog',
            name='end_date',
            field=models.DateTimeField(default=None, null=True, verbose_name='End Date'),
        ),
        migrations.AlterField(
            model_name='timelog',
            name='start_date',
            field=models.DateTimeField(verbose_name='Start Date'),
        ),
    ]
