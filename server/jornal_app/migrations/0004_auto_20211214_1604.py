# Generated by Django 3.2.9 on 2021-12-14 14:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('jornal_app', '0003_alter_userpageinfo_page_history'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userpage',
            name='external_info',
        ),
        migrations.DeleteModel(
            name='UserPageInfo',
        ),
    ]
