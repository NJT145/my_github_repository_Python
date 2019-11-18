# Generated by Django 2.0.6 on 2018-06-13 19:56

import django.contrib.postgres.fields.jsonb
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('server', '0003_auto_20180613_2253'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usergroup',
            name='prefered_books',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='usergroup',
            name='similar_books',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True),
        ),
    ]