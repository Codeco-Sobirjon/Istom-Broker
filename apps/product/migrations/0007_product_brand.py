# Generated by Django 5.1.2 on 2024-11-03 19:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0006_alter_comment_options_alter_review_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='brand',
            field=models.CharField(blank=True, max_length=250, null=True, verbose_name='Бренд продукции'),
        ),
    ]
