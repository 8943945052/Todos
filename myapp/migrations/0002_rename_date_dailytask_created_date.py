# Generated by Django 5.0.6 on 2024-08-15 20:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='dailytask',
            old_name='date',
            new_name='created_date',
        ),
    ]
