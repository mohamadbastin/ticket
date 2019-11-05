# Generated by Django 2.2.2 on 2019-11-05 16:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ticketapp', '0015_merge_20191104_1755'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reservation',
            name='profile',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reservation_owned', to='ticketapp.Profile'),
        ),
        migrations.AlterField(
            model_name='reservation',
            name='seat',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ticketapp.Seat'),
        ),
    ]
