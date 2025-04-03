from django.db import models
from .danhmuc import DanhMuc
from .baocaohangtuan import BaoCaoHangTuan 

class DanhMucBaoCao(models.Model):
    maDMBC = models.AutoField(primary_key=True)
    maBaoCao = models.ForeignKey(BaoCaoHangTuan, on_delete=models.CASCADE, db_column="maBaoCao")
    maDanhMuc = models.ForeignKey(DanhMuc, on_delete=models.CASCADE, db_column="maDanhMuc")

    class Meta:
        db_table = "danhmucbaocao"
