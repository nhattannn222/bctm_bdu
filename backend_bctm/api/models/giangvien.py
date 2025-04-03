from django.db import models
from .donvi import DonVi

class GiangVien (models.Model):
    maGiangVien = models.AutoField(primary_key=True)
    tenGiangVien = models.CharField(max_length=255)
    chucVu = models.CharField(max_length=255)
    maDonVi = models.ForeignKey(DonVi, on_delete=models.CASCADE)

    class Meta:
        db_table = "giangvien"