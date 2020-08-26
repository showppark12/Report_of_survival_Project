# Generated by Django 3.1 on 2020-08-26 08:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0002_chatroom'),
    ]

    operations = [
        migrations.CreateModel(
            name='Chat_Message',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=1000)),
                ('sender', models.CharField(max_length=20)),
                ('room_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='chat_message', to='chat.chatroom')),
            ],
        ),
    ]
