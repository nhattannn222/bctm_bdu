from django.urls import path
from .views import danh_sach_tai_khoan, get_danh_sach_danh_muc
from .views import DangNhap, DangXuat, CheckToken, TaoBaoCaoTuan
from .views import BaoCaoTuanAPIView, ThemDanhMucBaoCao, ThemNoiDung

urlpatterns = [
    path('api/login/', DangNhap.as_view(), name='dang-nhap'),
    path('api/tai-khoan/', danh_sach_tai_khoan, name='danh-sach-tai-khoan'),
    path('api/logout/<int:id>/', DangXuat.as_view(), name='dang-xuat'),
    path('api/token/<int:id>/', CheckToken.as_view(), name='kiem-tra-token'),
    path("api/taobaocaotuan/", TaoBaoCaoTuan.as_view(), name="tao-bao-cao-tuan"),
    path("api/baocaotuan/<int:id>/", BaoCaoTuanAPIView.as_view(), name="bao-cao-tuan"),
    path('api/danhmucbaocao/', get_danh_sach_danh_muc, name='danh-sach-danh-muc'),
    path("api/danhmucbaocao/<int:maBaoCao>/<int:maDanhMuc>/", ThemDanhMucBaoCao.as_view(), name="them-danh-muc-bao-cao"),
    path("api/noidung/them/", ThemNoiDung.as_view(), name="them-noi-dung"),
]