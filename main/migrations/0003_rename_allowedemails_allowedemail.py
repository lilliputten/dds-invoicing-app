# Generated by Django 5.0.2 on 2024-02-29 12:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_allowedemails'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='AllowedEmails',
            new_name='AllowedEmail',
        ),
    ]