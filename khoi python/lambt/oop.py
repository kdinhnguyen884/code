class vu_khi:
  def __init__ (self , ten_vk, sat_thuong):
    self.ten_vk = ten_vk
    self.sat_thuong = sat_thuong
  def gioi_thieu(self):
    return f"Vũ khí {self.ten_vk} có sát thương {self.sat_thuong}."
class CungTen(vu_khi):
    def __init__(self, ten_vk, sat_thuong, tam_xa):
        super().__init__(ten_vk, sat_thuong)
        self.tam_xa = tam_xa
    def ban(self):
        return f"{self.ten_vk} đánh trúng mục tiêu ở khoảng cách {self.tam_xa}m!"
class he_vk1(CungTen):
    def __init__(self, ten_vk, sat_thuong, tam_xa, he):
        super().__init__(ten_vk, sat_thuong, tam_xa) 
        self.he_vk = he
    def nguyen_to(self):
        return f"Vũ khí {self.ten_vk} thuộc hệ {self.he_vk}!"
ten_vk, st, kc, h = input().split()
my_weapon = he_vk1(ten_vk, int(st), int(kc), h)
print(my_weapon.gioi_thieu())
print(my_weapon.ban())
print(my_weapon.nguyen_to())
