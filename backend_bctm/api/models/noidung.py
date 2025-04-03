from django.db import models
from .danhmucbaocao import DanhMucBaoCao 

class NoiDung(models.Model):
    maNoiDung = models.AutoField(primary_key=True)
    noiDung = models.TextField()
    maLoaiNoiDung = models.ForeignKey(
        "LoaiNoiDung", on_delete=models.CASCADE, db_column="maLoaiNoiDung"
    )
    maDMBC = models.ForeignKey(DanhMucBaoCao, on_delete=models.CASCADE, db_column="maDMBC")

    class Meta:
        db_table = "noidung"
