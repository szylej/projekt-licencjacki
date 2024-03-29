# Generated by Django 4.1.2 on 2023-05-14 12:10

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('announcements', '0012_alter_announcement_photo'),
    ]

    operations = [
        migrations.AddField(
            model_name='announcement',
            name='available',
            field=models.BooleanField(default=False),
        ),
        migrations.CreateModel(
            name='Borrowing',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('borrow_date', models.DateTimeField()),
                ('return_date', models.DateTimeField(blank=True, null=True)),
                ('announcement', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='borrowings', to='announcements.announcement')),
                ('borrower', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='borrowings', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
