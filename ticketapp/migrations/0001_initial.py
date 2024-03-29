# Generated by Django 2.2.1 on 2019-10-29 09:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Ad',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('text', models.CharField(max_length=10000)),
                ('pic', models.ImageField(upload_to='')),
            ],
        ),
        migrations.CreateModel(
            name='Block',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=127)),
                ('gender', models.CharField(choices=[('f', 'female'), ('m', 'male')], max_length=2)),
            ],
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
            ],
        ),
        migrations.CreateModel(
            name='Hall',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
            ],
        ),
        migrations.CreateModel(
            name='Major',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=127)),
            ],
        ),
        migrations.CreateModel(
            name='Price',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=127)),
                ('price', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('picture', models.ImageField(blank=True, null=True, upload_to='')),
                ('student_id', models.CharField(max_length=10)),
                ('national_id', models.CharField(max_length=25)),
                ('gender', models.CharField(choices=[('m', 'male'), ('f', 'female')], max_length=2)),
                ('phone', models.CharField(max_length=15)),
                ('name', models.CharField(max_length=200)),
                ('qr', models.ImageField(blank=True, null=True, upload_to='')),
                ('major', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='ticketapp.Major')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Row',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.IntegerField()),
                ('block', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='row', to='ticketapp.Block')),
            ],
            options={
                'ordering': ['block', 'number'],
                'unique_together': {('number', 'block')},
            },
        ),
        migrations.CreateModel(
            name='Seat',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.IntegerField()),
                ('title', models.CharField(max_length=128)),
                ('description', models.CharField(blank=True, max_length=2048, null=True)),
                ('reserved', models.BooleanField(default=False)),
                ('ad', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='seat', to='ticketapp.Ad')),
            ],
            options={
                'ordering': ['row', 'number'],
            },
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256)),
            ],
        ),
        migrations.CreateModel(
            name='Terminal',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('api_key', models.CharField(max_length=1000)),
            ],
        ),
        migrations.CreateModel(
            name='UserService',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.BooleanField(default=False)),
                ('service', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='ticketapp.Service')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='ticketapp.Profile')),
            ],
        ),
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('profile', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='ticketapp.Profile')),
                ('seat', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='ticketapp.Seat')),
            ],
            options={
                'unique_together': {('seat', 'profile')},
            },
        ),
        migrations.AddField(
            model_name='seat',
            name='owner',
            field=models.ManyToManyField(through='ticketapp.Ticket', to='ticketapp.Profile'),
        ),
        migrations.AddField(
            model_name='seat',
            name='price',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='seat', to='ticketapp.Price'),
        ),
        migrations.AddField(
            model_name='seat',
            name='row',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='seat', to='ticketapp.Row'),
        ),
        migrations.CreateModel(
            name='PaymentLinks',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('link', models.CharField(max_length=1000)),
                ('terminal', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='ticketapp.Terminal')),
            ],
        ),
        migrations.CreateModel(
            name='Invoice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.PositiveIntegerField()),
                ('key', models.CharField(blank=True, max_length=1000, null=True)),
                ('status', models.CharField(blank=True, choices=[('f', 'false'), ('w', 'waiting'), ('t', 'true')], max_length=100, null=True)),
                ('payment_id', models.CharField(blank=True, max_length=1000, null=True)),
                ('error', models.CharField(blank=True, max_length=100, null=True)),
                ('terminal', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='ticketapp.Terminal')),
            ],
        ),
        migrations.CreateModel(
            name='HallEvent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='ticketapp.Event')),
                ('hall', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='ticketapp.Hall')),
            ],
        ),
        migrations.AddField(
            model_name='block',
            name='hall',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='block', to='ticketapp.Hall'),
        ),
        migrations.AlterUniqueTogether(
            name='seat',
            unique_together={('number', 'row')},
        ),
        migrations.AlterUniqueTogether(
            name='block',
            unique_together={('name', 'gender', 'hall')},
        ),
    ]
