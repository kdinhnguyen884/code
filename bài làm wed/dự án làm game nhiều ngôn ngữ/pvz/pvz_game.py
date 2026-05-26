import pygame
import random
import math

# --- KHỞI TẠO ---
pygame.init()
WIDTH, HEIGHT = 900, 660 # Tăng nhẹ chiều cao để UI thoáng hơn
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("PvZ - ULTIMATE UPGRADE")
clock = pygame.time.Clock()

# --- BẢNG MÀU ---
WHITE = (255, 255, 255); YELLOW = (255, 255, 50); GOLD = (218, 165, 32)
GREEN_L = (76, 187, 23); GREEN_D = (50, 120, 20); RED = (220, 20, 60)
BROWN = (101, 67, 33); DARK_BG = (15, 30, 15); CYAN = (0, 255, 255)
SILVER = (192, 192, 192); ICE_BLUE = (150, 220, 255)

font = pygame.font.SysFont("Arial", 18, True)
ui_font = pygame.font.SysFont("Arial", 26, True)
msg_font = pygame.font.SysFont("Verdana", 50, True)

# --- CLASSES ---
class Sun:
    def __init__(self, x=None, y=None):
        self.rect = pygame.Rect(x if x else random.randint(200, 800), y if y else -50, 35, 35)
        self.target_y = y if y else random.randint(200, 500)
        self.life = 350
    def update(self):
        if self.rect.y < self.target_y: self.rect.y += 2
        self.life -= 1
    def draw(self):
        pygame.draw.circle(screen, GOLD, self.rect.center, 18)
        pygame.draw.circle(screen, YELLOW, self.rect.center, 14)

class Bullet:
    def __init__(self, x, y, b_type="NORMAL"):
        self.rect = pygame.Rect(x + 40, y + 22, 12, 12)
        self.type = b_type
    def update(self): self.rect.x += 7
    def draw(self):
        color = ICE_BLUE if self.type == "ICE" else (150, 255, 150)
        pygame.draw.circle(screen, color, self.rect.center, 8)
        if self.type == "ICE": pygame.draw.circle(screen, WHITE, self.rect.center, 4)

class Plant:
    def __init__(self, x, y, p_type):
        self.rect = pygame.Rect(x, y, 60, 60)
        self.type = p_type
        # Máu: Wall (hạt dẻ) cực trâu, các cây khác trung bình
        self.hp = 1200 if p_type == "WALL" else 100
        self.max_hp = self.hp
        self.timer = 0
    def draw(self, alpha=255):
        s = pygame.Surface((60, 60), pygame.SRCALPHA)
        color = YELLOW if self.type == "SUN" else GREEN_L if self.type == "SHOOTER" else \
                GREEN_D if self.type == "REPEATER" else BROWN if self.type == "WALL" else \
                RED if self.type == "BOMB" else ICE_BLUE
        
        if self.type == "WALL": 
            pygame.draw.rect(s, (*color, alpha), (8, 5, 44, 52), border_radius=15)
        else:
            pygame.draw.circle(s, (*color, alpha), (30, 30), 22)
            if self.type in ["SHOOTER", "REPEATER", "ICE"]:
                pygame.draw.circle(s, (30, 80, 30, alpha), (45, 30), 8)
        
        screen.blit(s, self.rect.topleft)
        if alpha == 255 and self.hp < self.max_hp and self.type != "BOMB":
            pygame.draw.rect(screen, (50, 50, 50), (self.rect.x, self.rect.y-10, 60, 6))
            pygame.draw.rect(screen, (0, 255, 100), (self.rect.x, self.rect.y-10, (self.hp/self.max_hp)*60, 6))

class Zombie:
    def __init__(self, z_type="NORMAL"):
        self.rect = pygame.Rect(WIDTH, random.randint(1, 5)*80 + 120 + 10, 45, 55)
        self.type = z_type
        self.hp = 12 if z_type == "NORMAL" else 45
        self.max_hp = self.hp
        self.base_speed = 0.6
        self.speed = self.base_speed
        self.x = float(self.rect.x)
        self.slow_timer = 0
        self.is_eating = False

    def update(self, plants):
        self.is_eating = False
        self.speed = self.base_speed * 0.5 if self.slow_timer > 0 else self.base_speed
        if self.slow_timer > 0: self.slow_timer -= 1

        for p in plants:
            if self.rect.colliderect(p.rect):
                p.hp -= 0.6
                self.is_eating = True
                break
        
        if not self.is_eating:
            self.x -= self.speed
            self.rect.x = int(self.x)

    def draw(self):
        # Màu zombie chuyển sang xanh nhạt nếu bị làm chậm
        body_color = (100, 150, 255) if self.slow_timer > 0 else (80, 80, 80)
        pygame.draw.rect(screen, body_color, self.rect, border_radius=5)
        if self.is_eating: # Hiệu ứng rung khi ăn
            self.rect.x += random.randint(-1, 1)
        
        if self.type == "BUCKET":
            pygame.draw.rect(screen, SILVER, (self.rect.x+5, self.rect.y-15, 35, 22), border_radius=3)
        
        # Thanh máu nhỏ trên đầu
        pygame.draw.rect(screen, (255, 0, 0), (self.rect.x, self.rect.y-8, 45, 4))
        pygame.draw.rect(screen, (0, 255, 0), (self.rect.x, self.rect.y-8, (self.hp/self.max_hp)*45, 4))

# --- MAIN GAME ---
def run_game():
    plants, zombies, bullets, suns, explosions = [], [], [], [], []
    total_sun = 200
    dragging = None
    using_shovel = False
    
    # Hệ thống Wave
    wave = 1
    wave_timer = 0
    is_huge_wave = False
    msg_timer = 0

    mowers = [{"rect": pygame.Rect(30, (r+1)*80+135, 45, 40), "active": False, "gone": False} for r in range(5)]

    cards = [
        {"type": "SUN", "cost": 50, "cd": 5000, "last": -5000, "color": YELLOW},
        {"type": "SHOOTER", "cost": 100, "cd": 7500, "last": -7500, "color": GREEN_L},
        {"type": "ICE", "cost": 175, "cd": 10000, "last": -10000, "color": ICE_BLUE},
        {"type": "REPEATER", "cost": 200, "cd": 12000, "last": -12000, "color": GREEN_D},
        {"type": "WALL", "cost": 50, "cd": 15000, "last": -15000, "color": BROWN},
        {"type": "BOMB", "cost": 150, "cd": 25000, "last": -25000, "color": RED}
    ]
    shovel_rect = pygame.Rect(720, 20, 70, 80)

    while True:
        now = pygame.time.get_ticks()
        screen.fill(DARK_BG)
        mx, my = pygame.mouse.get_pos()

        # 1. LOGIC WAVE (ĐỘ KHÓ TĂNG DẦN)
        wave_timer += 1
        if wave_timer % 10000 == 0: # Mỗi khoảng thời gian sẽ tăng Wave
            wave += 1
            is_huge_wave = True
            msg_timer = 120
        
        # Spawn Zombie dựa trên Wave
        current_spawn_rate = max(60, 250 - (wave * 12))
        if not is_huge_wave:
            if random.randint(1, current_spawn_rate) == 1:
                z_type = "BUCKET" if random.random() < (0.05 + wave*0.03) else "NORMAL"
                zombies.append(Zombie(z_type))
        else: 
            # Huge Wave chỉ spawn tối đa 3-4 con ngẫu nhiên thay vì phủ kín 5 hàng ngay lập tức
            num_zombies = min(wave + 2, 5)
            for r in range(1, 6):
                zombies.append(Zombie("NORMAL" if random.random() > 0.3 else "BUCKET"))
            is_huge_wave = False

        # Vẽ Sân Cỏ
        for r in range(1, 6):
            for c in range(9):
                color = (35, 90, 35) if (r+c)%2==0 else (30, 80, 30)
                pygame.draw.rect(screen, color, (c*80+100, r*80+120, 80, 80))

        # Events
        for e in pygame.event.get():
            if e.type == pygame.QUIT: return False
            if e.type == pygame.MOUSEBUTTONDOWN:
                if shovel_rect.collidepoint(mx, my):
                    using_shovel = not using_shovel; dragging = None
                else:
                    for s in suns[:]:
                        if s.rect.collidepoint(mx, my):
                            total_sun += 25; suns.remove(s); break
                    else:
                        for c in cards:
                            if c["rect"].collidepoint(mx, my) and total_sun >= c["cost"] and now - c["last"] >= c["cd"]:
                                dragging = c; using_shovel = False
                        if using_shovel:
                            for p in plants[:]:
                                if p.rect.collidepoint(mx, my): plants.remove(p); using_shovel = False; break

            if e.type == pygame.MOUSEBUTTONUP and dragging:
                if 100 < mx < 820 and 200 < my < 600:
                    gx, gy = ((mx-100)//80)*80+110, ((my-120)//80)*80+130
                    if not any(p.rect.topleft == (gx, gy) for p in plants):
                        plants.append(Plant(gx, gy, dragging["type"]))
                        total_sun -= dragging["cost"]; dragging["last"] = now
                dragging = None

        if random.randint(1, 350) == 1: suns.append(Sun())

        # Update Cây & Đạn
        for p in plants[:]:
            p.timer += 1
            if p.type == "BOMB" and p.timer > 80:
                explosions.append([p.rect.center, 30]) # Nổ to hơn
                for z in zombies[:]:
                    # Tính khoảng cách nổ (phạm vi 3x3 ô)
                    dist = math.hypot(p.rect.centerx - z.rect.centerx, p.rect.centery - z.rect.centery)
                    if dist < 150: zombies.remove(z)
                plants.remove(p); continue
            
            if p.hp <= 0: plants.remove(p); continue
            
            if p.type == "SUN" and p.timer >= 500:
                suns.append(Sun(p.rect.centerx, p.rect.centery)); p.timer = 0
            elif p.type in ["SHOOTER", "REPEATER", "ICE"]:
                if any(z.rect.y == p.rect.y for z in zombies if z.rect.x > p.rect.x):
                    cd = 45 if p.type == "REPEATER" else 90
                    if p.timer >= cd:
                        b_type = "ICE" if p.type == "ICE" else "NORMAL"
                        bullets.append(Bullet(p.rect.x, p.rect.y, b_type)); p.timer = 0
            p.draw()

        # Update Đạn & Zombie va chạm
        for b in bullets[:]:
            b.update(); b.draw()
            if b.rect.x > WIDTH: bullets.remove(b); continue
            for z in zombies[:]:
                if b.rect.colliderect(z.rect):
                    z.hp -= 2
                    if b.type == "ICE": z.slow_timer = 180 # Làm chậm 3 giây
                    if b in bullets: bullets.remove(b)
                    if z.hp <= 0: zombies.remove(z)
                    break

        # Máy cắt cỏ
        for m in mowers:
            if m["gone"]: continue 
            pygame.draw.rect(screen, (100, 100, 100), m["rect"], border_radius=5)
            if m["active"]:
                m["rect"].x += 12
                for z in zombies[:]:
                    if m["rect"].colliderect(z.rect): zombies.remove(z)
                if m["rect"].x > WIDTH: m["gone"] = True 
            else:
                for z in zombies:
                    if m["rect"].colliderect(z.rect): m["active"] = True

        for z in zombies:
            z.update(plants); z.draw()
            if z.rect.x < 15: return True 

        for s in suns[:]:
            s.update(); s.draw()
            if s.life <= 0: suns.remove(s)

        # UI & HUD
        pygame.draw.rect(screen, (25, 25, 25), (0, 0, WIDTH, 120))
        sun_box = pygame.Rect(20, 20, 110, 80); pygame.draw.rect(screen, (45, 45, 45), sun_box, border_radius=10)
        sun_val = ui_font.render(str(total_sun), True, YELLOW); screen.blit(sun_val, (sun_box.centerx - sun_val.get_width()//2, 45))
        screen.blit(font.render("WAVE: " + str(wave), True, WHITE), (30, 100))

        for i, c in enumerate(cards):
            r = pygame.Rect(140 + i*90, 15, 80, 95); c["rect"] = r
            cd_p = min(1, (now - c["last"]) / c["cd"])
            pygame.draw.rect(screen, (50, 50, 50), r, border_radius=8)
            pygame.draw.circle(screen, c["color"], (r.centerx, r.y+30), 20)
            if cd_p < 1: pygame.draw.rect(screen, (0,0,0,200), (r.x, r.y, 80, 95*(1-cd_p)), border_radius=8)
            cost_txt = font.render(str(c["cost"]), True, WHITE if total_sun >= c["cost"] else RED)
            screen.blit(cost_txt, (r.centerx - cost_txt.get_width()//2, r.y+70))

        # Xẻng
        pygame.draw.rect(screen, (80, 50, 30) if using_shovel else (40, 40, 40), shovel_rect, border_radius=10)
        pygame.draw.rect(screen, SILVER, (shovel_rect.x+25, shovel_rect.y+10, 20, 30))
        if using_shovel: pygame.draw.rect(screen, YELLOW, shovel_rect, 3, border_radius=10)

        # Hiệu ứng nổ & Thông báo
        for exp in explosions[:]:
            pygame.draw.circle(screen, (255, 100, 0), exp[0], (30-exp[1])*10, 5)
            exp[1] -= 1
            if exp[1] <= 0: explosions.remove(exp)

        if msg_timer > 0:
            txt = msg_font.render("A HUGE WAVE!", True, RED)
            screen.blit(txt, (WIDTH//2 - txt.get_width()//2, HEIGHT//2))
            msg_timer -= 1

        if dragging:
            gx, gy = ((mx-100)//80)*80+110, ((my-120)//80)*80+130
            Plant(gx, gy, dragging["type"]).draw(alpha=120)

        pygame.display.flip()
        clock.tick(60)

while run_game(): pass
pygame.quit()