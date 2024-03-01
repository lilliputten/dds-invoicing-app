# Generated by Django 5.0.2 on 2024-03-01 13:12

import django.db.models.deletion
import django.db.models.manager
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('preferences', '0003_alter_preferences_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='AllowedEmail',
            fields=[
                ('email', models.EmailField(max_length=80, primary_key=True, serialize=False)),
                ('allow_participation', models.BooleanField(default=False)),
                ('free_participation', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='EventOption',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=80)),
                ('active', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='SitePreferences',
            fields=[
                ('preferences_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='preferences.preferences')),
                ('site_title', models.CharField(default='DDS Invoicing', max_length=80)),
                ('allow_only_listed_emails', models.BooleanField(default=False)),
            ],
            bases=('preferences.preferences',),
            managers=[
                ('singleton', django.db.models.manager.Manager()),
            ],
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=80)),
                ('description', models.TextField(blank=True, max_length=600)),
                ('status', models.CharField(choices=[('WAITING', 'Waiting'), ('ACTIVE', 'Active'), ('CLOSED', 'Closed')], default='WAITING', max_length=15)),
                ('allowed_emails', models.TextField(blank=True, default='', max_length=600)),
                ('no_payment_emails', models.TextField(blank=True, default='', max_length=600)),
                ('options', models.ManyToManyField(related_name='event', to='main.eventoption')),
            ],
        ),
        migrations.CreateModel(
            name='Application',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('secret_code', models.UUIDField(default=uuid.uuid4)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=80)),
                ('email', models.EmailField(max_length=80)),
                ('text', models.TextField(blank=True, max_length=400)),
                ('payment_method', models.CharField(choices=[('STRIPE', 'Stripe'), ('INVOICE', 'Invoice')], default='STRIPE', max_length=15)),
                ('status', models.CharField(choices=[('WAITING', 'Waiting'), ('FINISHED', 'Finished')], default='WAITING', max_length=15)),
                ('payment_status', models.CharField(choices=[('WAITING', 'Waiting'), ('FINISHED', 'Finished')], default='WAITING', max_length=15)),
                ('event', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='application', to='main.event')),
                ('options', models.ManyToManyField(related_name='application', to='main.eventoption')),
            ],
        ),
    ]
