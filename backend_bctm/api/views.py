from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework import status
from datetime import date, time, timedelta
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import TaiKhoanSerializer, BaoCaoHangTuanSerializer, DanhMucBaoCaoSerializer, NoiDungSerializer, DanhMucSerializer, GiangVienSerializer, DonViSerializer
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
            return Response({"error": "Tài khoản không tồn tại"}, status=status.HTTP_400_BAD_REQUEST)

        # Kiểm tra mật khẩu
        if mat_khau != user.matKhau:
            return Response({"error": "Sai mật khẩu"}, status=status.HTTP_400_BAD_REQUEST)

        # Tạo token mới cho người dùng
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)

        # Lưu token vào trường 'token' của người dùng
        user.token = access_token
        user.save()
        nguoidung = TaiKhoanSerializer(user)

        giang_vien = None
        don_vi = None

        if user.maGiangVien:
            giang_vien = GiangVienSerializer(user.maGiangVien).data
        return Response({
            "message": "Đăng nhập thành công!",
            "refresh": str(refresh),
            "access": access_token,
            "user": nguoidung.data,
            "giangVien": giang_vien,  
        }, status=status.HTTP_200_OK)

class DangXuat(APIView):
    def post(self, request, token):
        try:
            user = TaiKhoan.objects.get(token=token)
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

class ThemNoiDungBaoCao(APIView):
    def post(self, request, maBaoCao):
        data = request.data
        try:
            # Kiểm tra xem báo cáo có tồn tại không
            baocao = BaoCaoHangTuan.objects.get(maBaoCao=maBaoCao)
        except BaoCaoHangTuan.DoesNotExist:
            return Response({"error": "maBaoCao không tồn tại"}, status=status.HTTP_400_BAD_REQUEST)

        baocao.trangThai = 'Chờ duyệt'  # Giả sử 'CHO_DUYET' là giá trị trạng thái 'chờ duyệt'
        baocao.save()
        # Khởi tạo danh sách để chứa các bản ghi DanhMucBaoCao và NoiDung
        ds_danhmuc_baocao = []
        ds_noidung = []

        # Lặp qua mỗi phần tử trong dữ liệu
        for item in data:
            maDanhMuc = item.get("maDanhMuc")
            noiDungList = item.get("noiDung")
            
            # Kiểm tra xem danh mục có tồn tại không
            try:
                danhmuc = DanhMuc.objects.get(maDanhMuc=maDanhMuc)
            except DanhMuc.DoesNotExist:
                return Response({"error": f"maDanhMuc {maDanhMuc} không tồn tại"}, status=status.HTTP_400_BAD_REQUEST)

            # Thêm bản ghi vào bảng DanhMucBaoCao
            danhmuc_baocao = DanhMucBaoCao.objects.create(maBaoCao=baocao, maDanhMuc=danhmuc)
            ds_danhmuc_baocao.append(danhmuc_baocao)

            # Tạo các bản ghi vào bảng NoiDung từ danh sách "noiDung"
            for noiDungItem in noiDungList:
                ketQua = noiDungItem.get("ketQua")
                noiDungTuanSau = noiDungItem.get("noiDungTuanSau")
                deXuatKienNghi = noiDungItem.get("deXuatKienNghi")

                # Tạo các bản ghi vào bảng NoiDung cho từng loại nội dung
                for maLoaiNoiDung, noiDung in zip([1, 2, 3], [ketQua, noiDungTuanSau, deXuatKienNghi]):
                    if noiDung:  # Chỉ thêm nếu có nội dung
                        noidung = NoiDung.objects.create(
                            noiDung=noiDung,
                            maLoaiNoiDung_id=maLoaiNoiDung,
                            maDMBC=danhmuc_baocao
                        )
                        ds_noidung.append(noidung)

        # Gửi phản hồi với dữ liệu đã thêm vào bảng DanhMucBaoCao và NoiDung
        danhmuc_serializer = DanhMucBaoCaoSerializer(ds_danhmuc_baocao, many=True)
        noidung_serializer = NoiDungSerializer(ds_noidung, many=True)

        return Response({
            "message": "Thêm thành công",
            "danhmuc_baocao": danhmuc_serializer.data,
            "noidung": noidung_serializer.data
        }, status=status.HTTP_201_CREATED)

