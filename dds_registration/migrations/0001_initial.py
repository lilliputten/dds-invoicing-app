# Generated by Django 5.0.3 on 2024-03-12 21:26

import dds_registration.models
import django.db.models.deletion
import functools
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.TextField(default=dds_registration.models.random_code, unique=True)),
                ('title', models.TextField(unique=True)),
                ('description', models.TextField(blank=True)),
                ('registration_open', models.DateField(auto_now=True, help_text='Date registration opens')),
                ('registration_close', models.DateField(blank=True, help_text='Date registration closes', null=True)),
                ('max_participants', models.PositiveIntegerField(default=0, help_text='Maximum number of participants to this event (0 = no limit)')),
                ('currency', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='DiscountCode',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.TextField(default=functools.partial(dds_registration.models.random_code, *(), **{'length': 4}))),
                ('only_registration', models.BooleanField(default=True)),
                ('percentage', models.IntegerField(blank=True, help_text='Value as a percentage, like 10', null=True)),
                ('absolute', models.FloatField(blank=True, help_text='Absolute amount of discount', null=True)),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dds_registration.event')),
            ],
        ),
        migrations.CreateModel(
            name='GroupDiscount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('only_registration', models.BooleanField(default=True)),
                ('percentage', models.IntegerField(blank=True, help_text='Value as a percentage, like 10', null=True)),
                ('absolute', models.FloatField(blank=True, help_text='Absolute amount of discount', null=True)),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dds_registration.event')),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='auth.group')),
            ],
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.TextField()),
                ('emailed', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dds_registration.event')),
            ],
        ),
        migrations.CreateModel(
            name='RegistrationOption',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item', models.TextField()),
                ('price', models.FloatField(default=0)),
                ('add_on', models.BooleanField(default=False)),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dds_registration.event')),
            ],
        ),
        migrations.CreateModel(
            name='Registration',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('paid', models.BooleanField(default=False)),
                ('paid_date', models.DateTimeField(blank=True, null=True)),
                ('payment_method', models.TextField(choices=[('STRIPE', 'Stripe'), ('INVOICE', 'Invoice')], default='STRIPE')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='registrations', to='dds_registration.event')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='registrations', to=settings.AUTH_USER_MODEL)),
                ('options', models.ManyToManyField(to='dds_registration.registrationoption')),
            ],
        ),
        migrations.AddConstraint(
            model_name='registration',
            constraint=models.UniqueConstraint(fields=('event', 'user'), name='Single registration'),
        ),
    ]
