# Generated by Django 2.2.2 on 2019-11-02 19:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ticketapp', '0007_auto_20191102_1644'),
    ]

    operations = [
        migrations.AlterField(
            model_name='seat',
            name='status',
            field=models.CharField(choices=[('A', 'Available'), ('S', 'Sold'), ('M', 'Mine'), ('N', 'Not_Visible')], default='A', max_length=2),
        ),
    ]
