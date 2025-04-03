from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework import status
from datetime import date, time, timedelta
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import TaiKhoanSerializer, BaoCaoHangTuanSerializer, DanhMucBaoCaoSerializer, NoiDungSerializer, DanhMucSerializer
from .models import TaiKhoan, BaoCaoHangTuan, DonVi, DanhMucBaoCao, DanhMuc, NoiDung, LoaiNoiDung
from rest_framework.exceptions import NotFound

@api_view(['GET'])
def danh_sach_tai_khoan(request):
    tai_khoans = TaiKhoan.objects.all()
    serializer = TaiKhoanSerializer(tai_khoans, many=True)
    return Response(serializer.data)

    
class DangNhap(APIView):
    def post(self, request):
        data = request.data
        tai_khoan = data.get("taiKhoan")
        mat_khau = data.get("matKhau")

        if not all([tai_khoan, mat_khau]):
            return Response({"error": "Vui lòng nhập tài khoản và mật khẩu!"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = TaiKhoan.objects.get(taiKhoan=tai_khoan)
        except TaiKhoan.DoesNotExist:
            return Response({"error": "Tài khoản không tồn tại"}, status=status.HTTP_404_NOT_FOUND)

        # Kiểm tra mật khẩu
        if mat_khau != user.matKhau:
            return Response({"error": "Sai mật khẩu"}, status=status.HTTP_400_BAD_REQUEST)

        # Tạo token mới cho người dùng
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)

        # Lưu token vào trường 'token' của người dùng
        user.token = access_token
        user.save()

        return Response({
            "message": "Đăng nhập thành công!",
            "refresh": str(refresh),
            "access": access_token,
            "maTaiKhoan": user.maTaiKhoan,
        }, status=status.HTTP_200_OK)

class DangXuat(APIView):
    def post(self, request, id):
        try:
            user = TaiKhoan.objects.get(maTaiKhoan=id)
        except TaiKhoan.DoesNotExist:
            raise NotFound(detail="Tài khoản không tồn tại.")

        user.token = None
        user.save()
        return Response({"message": "Đăng xuất thành công!"}, status=status.HTTP_200_OK)
    
class CheckToken(APIView):
    def get(self, request, id):
        try:
            tai_khoan_obj = TaiKhoan.objects.get(maTaiKhoan=id)
            serializer = TaiKhoanSerializer(tai_khoan_obj)
            return Response({'token': serializer.data['token']}, status=status.HTTP_200_OK)
        except TaiKhoan.DoesNotExist:
            return Response({'error': 'Tài khoản không tồn tại.'}, status=status.HTTP_404_NOT_FOUND)
        
class TaoBaoCaoTuan(APIView):
    def post(self, request):
        danh_sach_don_vi = DonVi.objects.all()

        if not danh_sach_don_vi.exists():
            return Response({"error": "Không có đơn vị nào trong hệ thống"}, status=status.HTTP_400_BAD_REQUEST)

        bao_cao_list = []
        for don_vi in danh_sach_don_vi:
            bao_cao = BaoCaoHangTuan.objects.create(
                ngayTao=date.today(),
                gioBatDau=time(8, 0, 0),  
                gioKetThuc=time(22, 0, 0),  
                trangThai="Đang thực hiện",
                maDonVi=don_vi,
            )
            bao_cao_list.append(bao_cao)

        serializer = BaoCaoHangTuanSerializer(bao_cao_list, many=True)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
class BaoCaoTuanAPIView(APIView):
    def get(self, request, id):
        try:
            ma_don_vi = int(id)
        except ValueError:
            return Response({"error": "Mã đơn vị phải là số nguyên"}, status=status.HTTP_400_BAD_REQUEST)

        # Xác định khoảng thời gian trong tuần hiện tại
        today = date.today()
        start_of_week = today - timedelta(days=today.weekday())  # Thứ hai của tuần hiện tại
        end_of_week = start_of_week + timedelta(days=6)  # Chủ nhật của tuần hiện tại

        # Truy vấn báo cáo trong tuần của mã đơn vị
        bao_cao_list = BaoCaoHangTuan.objects.filter(
            maDonVi=ma_don_vi,
            ngayTao__range=[start_of_week, end_of_week]
        )

        # Serialize dữ liệu
        serializer = BaoCaoHangTuanSerializer(bao_cao_list, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def get_danh_sach_danh_muc(request):
    danh_muc_bao_cao = DanhMuc.objects.all()
    serializer = DanhMucSerializer(danh_muc_bao_cao, many=True)
    return Response(serializer.data)

class ThemDanhMucBaoCao(APIView):
    def post(self, request, maBaoCao, maDanhMuc):
        # Kiểm tra xem maBaoCao có tồn tại không
        try:
            baocao = BaoCaoHangTuan.objects.get(maBaoCao=maBaoCao)
        except BaoCaoHangTuan.DoesNotExist:
            return Response({"error": "maBaoCao không tồn tại"}, status=status.HTTP_400_BAD_REQUEST)

        # Kiểm tra xem maDanhMuc có tồn tại không
        try:
            danhmuc = DanhMuc.objects.get(maDanhMuc=maDanhMuc)
        except DanhMuc.DoesNotExist:
            return Response({"error": "maDanhMuc không tồn tại"}, status=status.HTTP_400_BAD_REQUEST)

        # Tạo bản ghi mới trong danhmucbaocao
        danhmuc_baocao = DanhMucBaoCao.objects.create(maBaoCao=baocao, maDanhMuc=danhmuc)
        serializer = DanhMucBaoCaoSerializer(danhmuc_baocao)

        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
class ThemNoiDung(APIView):
    def post(self, request):
        maDMBC = request.data.get("maDMBC")
        noiDung1 = request.data.get("noiDung1")
        noiDung2 = request.data.get("noiDung2")
        noiDung3 = request.data.get("noiDung3")

        # Kiểm tra maDMBC có tồn tại không
        try:
            danh_muc_bao_cao = DanhMucBaoCao.objects.get(maDMBC=maDMBC)
        except DanhMucBaoCao.DoesNotExist:
            return Response({"error": "maDMBC không tồn tại"}, status=status.HTTP_400_BAD_REQUEST)

        # Tạo 3 bản ghi nội dung
        ds_noidung = []
        for maLoaiNoiDung, noiDung in zip([1, 2, 3], [noiDung1, noiDung2, noiDung3]):
            if noiDung:  # Chỉ thêm nếu có nội dung
                noidung = NoiDung.objects.create(
                    noiDung=noiDung,
                    maLoaiNoiDung_id=maLoaiNoiDung,
                    maDMBC=danh_muc_bao_cao
                )
                ds_noidung.append(noidung)

        serializer = NoiDungSerializer(ds_noidung, many=True)
        return Response(serializer.data, status=status.HTTP_201_CREATED)