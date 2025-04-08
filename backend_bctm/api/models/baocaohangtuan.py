from django.db import models 
from .donvi import DonVi  

class BaoCaoHangTuan(models.Model):
    maBaoCao = models.AutoField(primary_key=True)
    ngayTao = models.DateField()
    gioBatDau = models.TimeField()
    gioKetThuc = models.TimeField()
    trangThai = models.CharField(
        max_length=20,
        choices=[
            ("Đang thực hiện", "Đang thực hiện"),
            ("Chờ duyệt", "Chờ duyệt"),
            ("Từ chối", "Từ chối"),
            ("Hoàn thành", "Hoàn thành"),
            ("Quá hạn", "Quá hạn"),
        ],
    )
    maDonVi = models.ForeignKey(DonVi, on_delete=models.CASCADE, db_column="maDonVi")

    class Meta:
        db_table = "baocaohangtuan"
