# Generated by Django 2.2 on 2021-06-10 01:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('testapp', '0004_like'),
    ]

    operations = [
        migrations.AddField(
            model_name='stock',
            name='user_likes',
            field=models.ManyToManyField(related_name='liked_stocks', to='testapp.User'),
        ),
        migrations.DeleteModel(
            name='Like',
        ),
    ]
