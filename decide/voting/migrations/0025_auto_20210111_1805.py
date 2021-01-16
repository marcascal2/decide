# Generated by Django 2.0 on 2021-01-11 18:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('voting', '0024_auto_20210111_1740'),
    ]

    operations = [
        migrations.CreateModel(
            name='Party',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('abreviatura', models.TextField(max_length=10)),
                ('nombre', models.TextField()),
            ],
        ),
        migrations.AlterField(
            model_name='candidate',
            name='auto_community',
            field=models.TextField(choices=[('AN', 'Andalucia'), ('AR', 'Aragon'), ('AS', 'Asturias'), ('BA', 'Baleares'), ('CA', 'Canarias'), ('CT', 'Cantabria'), ('CAM', 'Castilla-Mancha'), ('CAL', 'Castilla-Leon'), ('CAT', 'Cataluña'), ('CE', 'Ceuta'), ('EX', 'Extremadura'), ('GA', 'Galicia'), ('LR', 'La-Rioja'), ('MA', 'Madrid'), ('ME', 'Melilla'), ('MU', 'Murcia'), ('NA', 'Navarra'), ('PV', 'País-Vasco'), ('VA', 'Valencia')], default='AN'),
        ),
        migrations.AlterField(
            model_name='candidate',
            name='political_party',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='candidate', to='voting.Party'),
        ),
        migrations.DeleteModel(
            name='Community',
        ),
    ]