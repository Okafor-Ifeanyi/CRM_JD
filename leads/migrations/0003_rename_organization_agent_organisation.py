# Generated by Django 4.1.1 on 2022-10-04 19:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('leads', '0002_alter_lead_age_userprofile_agent_organization'),
    ]

    operations = [
        migrations.RenameField(
            model_name='agent',
            old_name='organization',
            new_name='organisation',
        ),
    ]