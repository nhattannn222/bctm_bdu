from rest_framework import serializers
from .models import BaoCaoHangTuan, TaiKhoan, DanhMucBaoCao, NoiDung, DanhMuc

    
class TaiKhoanSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaiKhoan
        fields = ['maTaiKhoan','taiKhoan', 'trangThai', 'vaiTro', 'token']

class BaoCaoHangTuanSerializer(serializers.ModelSerializer):
    class Meta:
        model = BaoCaoHangTuan
        fields = "__all__"

class DanhMucSerializer(serializers.ModelSerializer):
    class Meta:
        model = DanhMuc
        fields = "__all__"

class DanhMucBaoCaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = DanhMucBaoCao
        fields = ["maBaoCao", "maDanhMuc"]

class NoiDungSerializer(serializers.ModelSerializer):
    class Meta:
        model = NoiDung
        fields = "__all__"