# Generated by Django 2.1.2 on 2018-11-07 17:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wadmin', '0010_auto_20181107_1619'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='choice',
            name='question',
        ),
        migrations.DeleteModel(
            name='Choice',
        ),
        migrations.DeleteModel(
            name='Question',
        ),
    ]
