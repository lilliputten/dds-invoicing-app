# Generated by Django 5.0.2 on 2024-02-29 12:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AllowedEmails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=80)),
                ('allow_apply', models.BooleanField(default=False)),
                ('omit_payment', models.BooleanField(default=False)),
            ],
        ),
    ]