from django.db import models

class DanhMuc(models.Model):
    maDanhMuc = models.AutoField(primary_key=True)
    tenDanhMuc = models.CharField(max_length=255)

    class Meta:
        db_table = "danhmuc"
