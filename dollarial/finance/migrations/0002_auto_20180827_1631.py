# Generated by Django 2.0.4 on 2018-08-27 12:01

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('finance', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='deleted',
            field=models.BooleanField(db_index=True, default=False, verbose_name='Deleted'),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='time',
            field=models.DateTimeField(db_index=True, default=django.utils.timezone.now, verbose_name='Time'),
        ),
    ]
