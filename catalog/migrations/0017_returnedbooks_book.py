# Generated by Django 3.0.3 on 2020-04-15 03:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0016_auto_20200415_1121'),
    ]

    operations = [
        migrations.AddField(
            model_name='returnedbooks',
            name='book',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='catalog.Book'),
        ),
    ]
