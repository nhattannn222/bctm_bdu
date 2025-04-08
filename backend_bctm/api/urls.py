from django.urls import path
from .views import danh_sach_tai_khoan, get_danh_sach_danh_muc
from .views import DangNhap, DangXuat, CheckToken, TaoBaoCaoTuan
from .views import BaoCaoTuanAPIView, ThemNoiDungBaoCao

urlpatterns = [
    path('api/login/', DangNhap.as_view(), name='dang-nhap'),
    path('api/taikhoan/', danh_sach_tai_khoan, name='danh-sach-tai-khoan'),
    path('api/logout/<str:token>/', DangXuat.as_view(), name='dang-xuat'),
    path('api/token/<int:id>/', CheckToken.as_view(), name='kiem-tra-token'),
    path("api/taobaocaotuan/", TaoBaoCaoTuan.as_view(), name="tao-bao-cao-tuan"),
    
    path("api/baocaotuan/<int:id>/", BaoCaoTuanAPIView.as_view(), name="bao-cao-tuan"),
    path('api/danhmucbaocao/', get_danh_sach_danh_muc, name='danh-sach-danh-muc'),
    path("api/themnoidungbaocao/<int:maBaoCao>/", ThemNoiDungBaoCao.as_view(), name="noi-dung-bao-cao-tuan"),
]