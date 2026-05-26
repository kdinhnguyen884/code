# Danh sách chứa các dictionary
# Cấu trúc: {"ten": str, "hoan_thanh": bool}
tasks = []

def show_menu():
    print("\n" + "="*30)
    print("   QUẢN LÝ CÔNG VIỆC v2.0")
    print("="*30)
    print("1. Xem danh sách")
    print("2. Thêm công việc mới")
    print("3. Đánh dấu hoàn thành")
    print("4. Xóa công việc")
    print("5. Thoát")

while True:
    show_menu()
    choice = input("Mời bạn chọn (1-5): ")

    if choice == '1':
        print("\n--- DANH SÁCH VIỆC CẦN LÀM ---")
        if not tasks:
            print("Hiện tại không có công việc nào.")
        else:
            for i, task in enumerate(tasks, 1):
                # Hiển thị dấu [x] nếu đã xong, [ ] nếu chưa xong
                status = "[x]" if task["hoan_thanh"] else "[ ]"
                print(f"{i}. {status} {task['ten']}")
    
    elif choice == '2':
        name = input("Nhập tên công việc: ")
        # Mặc định công việc mới là chưa hoàn thành (False)
        tasks.append({"ten": name, "hoan_thanh": False})
        print("Đã thêm thành công!")

    elif choice == '3':
        idx = int(input("Nhập số thứ tự đã làm xong: ")) - 1
        if 0 <= idx < len(tasks):
            tasks[idx]["hoan_thanh"] = True
            print(f"Chúc mừng bạn đã hoàn thành: {tasks[idx]['ten']}!")
        else:
            print("Số thứ tự không đúng.")

    elif choice == '4':
        idx = int(input("Nhập số thứ tự muốn xóa: ")) - 1
        if 0 <= idx < len(tasks):
            removed = tasks.pop(idx)
            print(f"Đã xóa: {removed['ten']}")
        else:
            print("Số thứ tự không đúng.")

    elif choice == '5':
        print("Cảm ơn bạn đã sử dụng phần mềm. Chào tạm biệt!")
        break