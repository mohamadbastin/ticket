# Generated by Django 2.2.2 on 2019-11-05 17:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ticketapp', '0016_auto_20191105_1715'),
    ]

    operations = [
        migrations.AddField(
            model_name='invoice',
            name='profile',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='ticketapp.Profile'),
        ),
    ]
