# Generated by Django 2.0 on 2021-01-14 18:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('voting', '0029_merge_20210114_1420'),
    ]

    operations = [
        migrations.AlterField(
            model_name='plank',
            name='program',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='planks', to='voting.Program'),
        ),
    ]