# Generated by Django 4.0.4 on 2022-05-30 20:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='timelog',
            name='end_date',
            field=models.DateTimeField(default=None, null=True),
        ),
    ]
