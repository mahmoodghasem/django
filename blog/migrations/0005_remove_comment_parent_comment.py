# Generated by Django 4.2.7 on 2023-11-18 19:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_comment_parent_comment'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='parent_comment',
        ),
    ]