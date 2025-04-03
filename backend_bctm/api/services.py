
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework import status
from .models import BaoCaoHangTuan, DonVi
from datetime import date, time, timedelta
from .serializers import BaoCaoHangTuanSerializer

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