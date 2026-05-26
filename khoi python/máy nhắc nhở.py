import time
viec_can_lam = input("Bạn cần nhắc nhở việc gì? ")
phut = int(input("Sau bao nhiêu phút thì nhắc một lần? "))

giay = phut * 60 

print(f"--- Đã bắt đầu! Mình sẽ nhắc bạn '{viec_can_lam}' sau mỗi {phut} phút ---")

while True:
    time.sleep(giay) # Máy sẽ đợi ở đây
    print(f"🔔 TỚI GIỜ RỒI: {viec_can_lam} !!!")
