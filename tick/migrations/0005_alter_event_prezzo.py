# Generated by Django 3.2.7 on 2021-10-04 16:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tick', '0004_alter_event_prezzo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='prezzo',
            field=models.DecimalField(decimal_places=2, max_digits=5),
        ),
    ]
