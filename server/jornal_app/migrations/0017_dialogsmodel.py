# Generated by Django 4.0 on 2021-12-19 17:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('jornal_app', '0016_rename_author_room_sender'),
    ]

    operations = [
        migrations.CreateModel(
            name='DialogsModel',
            fields=[
                ('created', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('user1', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='jornal_app.user')),
                ('user2', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='jornal_app.user')),
            ],
            options={
                'unique_together': {('user1', 'user2'), ('user2', 'user1')},
            },
        ),
    ]