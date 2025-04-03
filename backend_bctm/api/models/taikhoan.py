from django.db import models
from .giangvien import GiangVien

class TaiKhoan(models.Model):
    maTaiKhoan = models.AutoField(primary_key=True)
    taiKhoan = models.CharField(max_length=50, unique=True)
    matKhau = models.CharField(max_length=255)
    trangThai = models.CharField(
        max_length=1, choices=[("1", "Active"), ("0", "Inactive")], default="1"
    )
    maGiangVien = models.ForeignKey(
        "GiangVien", on_delete=models.CASCADE, db_column="maGiangVien"
    )
    vaiTro = models.CharField(
        max_length=5, choices=[("GV", "GV"), ("TKDV", "TKDV"), ("TDV", "TDV"), ("TKHT", "TKHT")]
    )
    token = models.TextField(null=True, blank=True)

    @property
    def id(self):
        return self.maTaiKhoan
    class Meta:
        db_table = "taikhoan"
        managed = False