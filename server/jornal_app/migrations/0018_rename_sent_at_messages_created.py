# Generated by Django 4.0 on 2021-12-21 17:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('jornal_app', '0017_dialogsmodel'),
    ]

    operations = [
        migrations.RenameField(
            model_name='messages',
            old_name='sent_at',
            new_name='created',
        ),
    ]
