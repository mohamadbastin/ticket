# Generated by Django 2.2.2 on 2019-10-31 12:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ticketapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='email',
            field=models.EmailField(default='a@b.c', max_length=254),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='ticket',
            name='buyer',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.DO_NOTHING, related_name='ticket_bought', to='ticketapp.Profile'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='ticket',
            name='profile',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='ticket_owned', to='ticketapp.Profile'),
        ),
    ]
