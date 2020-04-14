# Generated by Django 3.0.3 on 2020-04-14 04:45

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0010_auto_20200412_2059'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='year',
            field=models.IntegerField(null=True, validators=[django.core.validators.MaxValueValidator(2020), django.core.validators.MinValueValidator(1900)]),
        ),
    ]