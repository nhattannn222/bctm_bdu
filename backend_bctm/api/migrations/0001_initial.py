# Generated by Django 5.1.7 on 2025-03-17 07:17

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BaoCaoHangTuan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ngayTao', models.DateField()),
                ('gioBatDau', models.TimeField()),
                ('gioKetThuc', models.TimeField()),
                ('trangThai', models.CharField(max_length=255)),
                ('maDonVi', models.IntegerField()),
            ],
        ),
    ]
