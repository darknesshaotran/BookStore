# Generated by Django 4.1.2 on 2022-11-04 17:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0004_book_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='price',
            field=models.IntegerField(),
        ),
    ]
