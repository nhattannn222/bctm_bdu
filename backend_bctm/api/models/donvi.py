from django.db import models

class DonVi (models.Model):
    maDonVi = models.AutoField(primary_key=True)
    tenDonVi = models.CharField(max_length=255)

    class Meta:
        db_table = "donvi"
    