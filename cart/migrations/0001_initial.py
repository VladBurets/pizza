# Generated by Django 4.2.2 on 2023-06-16 17:47

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('catalog', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.AutoField(db_index=True, primary_key=True, serialize=False)),
                ('count', models.PositiveIntegerField(default=1, verbose_name='количество')),
                ('pizza', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catalog.pizza', verbose_name='пицца')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='пользователь')),
            ],
        ),
    ]
