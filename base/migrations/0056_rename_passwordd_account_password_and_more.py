# Generated by Django 4.0.1 on 2022-01-31 18:32

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0055_rename_password_account_passwordd_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='account',
            old_name='passwordd',
            new_name='password',
        ),
        migrations.AlterField(
            model_name='comment',
            name='comment_date',
            field=models.DateTimeField(default=datetime.datetime(2022, 1, 31, 22, 2, 5, 194657)),
        ),
    ]