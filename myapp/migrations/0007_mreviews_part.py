# Generated by Django 3.2 on 2021-07-02 09:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0006_auto_20210702_1700'),
    ]

    operations = [
        migrations.AddField(
            model_name='mreviews',
            name='part',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
