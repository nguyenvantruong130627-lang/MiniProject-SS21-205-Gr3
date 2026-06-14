import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

def activate_overload_warning(devices: list) -> None:
    """
    Nhập mã thiết bị từ bàn phím để duyệt cảnh báo quá tải.
    - Không tìm thấy mã thiết bị -> Báo lỗi ERR-E01
    - Đã ở trạng thái Overload từ trước -> Báo lỗi ERR-E04
    - Tiêu thụ > 5,000 kWh -> Chuyển sang Overload & Log WARNING
    - Tiêu thụ <= 5,000 kWh -> Không đủ điều kiện kích hoạt
    """
    print("\n--- KÍCH HOẠT TRẠNG THÁI CẢNH BÁO QUÁ TẢI ---")
    device_id = input("Nhập mã thiết bị cần duyệt cảnh báo: ").strip()
    
    # Tìm kiếm thiết bị trong danh sách
    target_device = None
    for device in devices:
        if device['id'] == device_id:
            target_device = device
            break
            
    # Trường hợp không tìm thấy mã thiết bị
    if not target_device:
        print(f"[ERR-E01] Mã thiết bị '{device_id}' không tồn tại trên hệ thống!")
        return

    # Trường hợp thiết bị tìm thấy đã ở trạng thái Overload từ trước
    if target_device['status'] == 'Overload':
        print(f"[ERR-E04] Thiết bị '{device_id}' đã ở trạng thái Overload từ trước.")
        return

    # Tính toán lượng điện tiêu thụ thực tế
    consumption = target_device['new_index'] - target_device['old_index']
    print(f"Lượng điện tiêu thụ thực tế của thiết bị {device_id}: {consumption:,} kWh")

    # Kiểm tra điều kiện vượt mức 5,000 kWh
    if consumption > 5000:
        target_device['status'] = 'Overload'
        print("=> Kết quả duyệt: ĐỦ ĐIỀU KIỆN KÍCH HOẠT")
        
        # Phát ra thông báo log mức WARNING theo đúng yêu cầu
        logging.warning(
            f"Thiết bị {device_id} tại {target_device['location']} tiêu thụ {consumption:,} kWh -> Đã kích hoạt trạng thái Overload!"
        )
    else:
        print("=> Kết quả duyệt: Không đủ điều kiện kích hoạt (Tiêu thụ chưa vượt quá 5,000 kWh).")

def show_menu():
    print("\n" + "="*50)
    print("      SMART ENERGY MONITOR - PHÒNG CƠ ĐIỆN      ")
    print("="*50)
    print("1. Xem danh sách thiết bị giám sát")
    print("2. Cập nhật chỉ số điện tiêu thụ (Check-in)")
    print("3. Kích hoạt trạng thái cảnh báo quá tải")
    print("4. Tính tổng lượng điện & Chi phí năng lượng")
    print("5. Thoát chương trình")
    print("="*50)

def main():
    devices = [
        {'id': 'M01', 'location': 'Mechanical Shop A', 'old_index': 1200, 'new_index': 4500, 'status': 'Normal'},
        {'id': 'M02', 'location': 'Assembly Line B', 'old_index': 2300, 'new_index': 8500, 'status': 'Overload'}
    ]
    
    while True:
        show_menu()
        
        try:
            choice = int(input("Mời chọn chức năng (1-5): "))
        except ValueError:
            print("[LỖI] Vui lòng chỉ nhập số nguyên từ 1 đến 5!")
            continue
            
        if choice == 1:
            print("\n--> Bạn đã chọn Chức năng 1: Xem danh sách thiết bị.")
            
        elif choice == 2:
            print("\n--> Bạn đã chọn Chức năng 2: Cập nhật chỉ số điện tiêu thụ.")
            
        elif choice == 3:
            print("\n--> Bạn đã chọn Chức năng 3: Kích hoạt trạng thái cảnh báo quá tải.")
            activate_overload_warning(devices)
            
            
        elif choice == 4:
            print("\n--> Bạn đã chọn Chức năng 4: Tính tổng lượng điện & Chi phí năng lượng.")
            
        elif choice == 5:
            print("\nCảm ơn bạn đã sử dụng hệ thống. Tạm biệt!")
            break
            
        else:
            print("[LỖI] Lựa chọn không hợp lệ! Vui lòng chọn lại từ 1 đến 5.")

main()
