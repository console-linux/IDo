# Generated by Django 5.0.7 on 2024-08-17 08:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('IDo_API', '0002_subtopic_task_topic_delete_user_subtopic_topic'),
    ]

    operations = [
        migrations.RenameField(
            model_name='subtopic',
            old_name='Topic',
            new_name='topic',
        ),
        migrations.RenameField(
            model_name='task',
            old_name='SubTopic',
            new_name='subtopic',
        ),
    ]
