# Generated by Django 3.2.9 on 2023-02-08 10:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0005_alter_article_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='photo',
            field=models.CharField(default='', max_length=200),
        ),
    ]
