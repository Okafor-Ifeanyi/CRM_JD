# Generated by Django 4.1.1 on 2022-10-10 23:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('leads', '0011_lead_date_added_lead_phone_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='lead',
            name='description',
            field=models.TextField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='lead',
            name='email',
            field=models.EmailField(default=1, max_length=254),
            preserve_default=False,
        ),
    ]
