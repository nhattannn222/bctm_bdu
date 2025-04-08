from .models import BaoCaoHangTuan, DonVi
from datetime import date, time,  timedelta, datetime
def tao_bao_cao_tuan():
    try:
        danh_sach_don_vi = DonVi.objects.all()

        if not danh_sach_don_vi.exists():
            return {"error": "Không có đơn vị nào trong hệ thống"}

        bao_cao_list = []
        for don_vi in danh_sach_don_vi:
            bao_cao = BaoCaoHangTuan.objects.create(
                ngayTao=date.today(),
                gioBatDau=time(8, 0, 0),  
                gioKetThuc=time(22, 0, 0),  
                trangThai="Đang thực hiện",
                maDonVi=don_vi,
            )
            bao_cao_list.append(bao_cao.maBaoCao)  # Trả về danh sách ID thay vì object

        return {"message": f"Đã tạo {len(bao_cao_list)} báo cáo thành công", "ids": bao_cao_list}
    except Exception as e:
        print(f"Lỗi trong tao_bao_cao_tuan: {e}")
        return {"error": str(e)}
    
def cap_nhat_bao_cao_qua_han():
    try:
        # Lấy ngày hiện tại và xác định thứ 2 đầu tuần
        hom_nay = datetime.today().date()
        thu_hai = hom_nay - timedelta(days=hom_nay.weekday())

        # Lọc báo cáo trong tuần hiện tại
        bao_cao_trong_tuan = BaoCaoHangTuan.objects.filter(
            ngayTao__gte=thu_hai,
            ngayTao__lte=hom_nay
        ).exclude(trangThai__in=["Hoàn thành", "Quá hạn"])

        # Cập nhật trạng thái
        so_luong = bao_cao_trong_tuan.update(trangThai="Quá hạn")

        print(f"Đã cập nhật {so_luong} báo cáo thành 'Quá hạn'")
        return {"message": f"Đã cập nhật {so_luong} báo cáo thành 'Quá hạn'"}
    except Exception as e:
        print(f"Lỗi trong cap_nhat_bao_cao_qua_han: {e}")
        return {"error": str(e)}