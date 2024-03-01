# Generated by Django 5.0.2 on 2024-03-01 17:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_rename_text_application_comment'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sitepreferences',
            name='allow_only_listed_emails',
        ),
        migrations.AddField(
            model_name='event',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default='2024-03-01 13:22:03.971677'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='event',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
