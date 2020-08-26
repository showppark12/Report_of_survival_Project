# Generated by Django 3.1 on 2020-08-26 06:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0003_auto_20200820_1339'),
        ('chat', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ChatRoom',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('req_channel_name', models.CharField(max_length=300)),
                ('res_channel_name', models.CharField(max_length=300)),
                ('req_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='req_chatroom', to='account.account')),
                ('res_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='res_chatroom', to='account.account')),
            ],
        ),
    ]
