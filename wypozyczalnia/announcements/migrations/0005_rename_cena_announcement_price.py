# Generated by Django 4.1.2 on 2023-04-05 16:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('announcements', '0004_alter_rating_comment'),
    ]

    operations = [
        migrations.RenameField(
            model_name='announcement',
            old_name='cena',
            new_name='price',
        ),
    ]
