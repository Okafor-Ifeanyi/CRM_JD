# Generated by Django 4.1.1 on 2022-10-10 23:08

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('leads', '0010_alter_lead_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='lead',
            name='date_added',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='lead',
            name='phone_number',
            field=models.CharField(default=234, max_length=14),
            preserve_default=False,
        ),
    ]