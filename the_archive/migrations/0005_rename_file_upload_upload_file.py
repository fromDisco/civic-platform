# Generated by Django 4.1.7 on 2023-05-05 18:50

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("the_archive", "0004_alter_upload_file"),
    ]

    operations = [
        migrations.RenameField(
            model_name="upload",
            old_name="file",
            new_name="upload_file",
        ),
    ]
