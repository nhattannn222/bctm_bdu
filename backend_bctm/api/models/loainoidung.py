from django.db import models

class LoaiNoiDung(models.Model):
    maLoaiNoiDung = models.AutoField(primary_key=True)
    tenLoaiNoiDung = models.CharField(max_length=255)

    class Meta:
        db_table = "loainoidung"