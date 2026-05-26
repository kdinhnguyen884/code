import pygame
import random
import os
import math

# --- Cài Đặt Ban Đầu ---
pygame.init()
pygame.mixer.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Bảo vệ Trái đất")

# Cài đặt FPS
FPS = 60
clock = pygame.time.Clock()

# --- Định nghĩa Màu sắc ---
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
GOLD = (255, 215, 0)
ORANGE = (255, 165, 0)
YELLOW = (255, 255, 0)
BROWN = (139, 69, 19)
CYAN = (0, 255, 255)
GRAY = (150, 150, 150)
PURPLE = (128, 0, 128)
DARK_RED = (139, 0, 0)
DARK_GREEN = (0, 100, 0)

# --- Tắt âm thanh ---
sound_enabled = False # Bạn có thể đổi thành True nếu có file âm thanh
# --- Thiết Lập Biến Toàn Cục ---
# Phi thuyền của người chơi
player_width = 50
player_height = 50
player_color = BLUE
player_rect = pygame.Rect(SCREEN_WIDTH // 2 - player_width // 2, SCREEN_HEIGHT - player_height, player_width, player_height)
player_speed = 5
base_player_speed = 5
player_health = 100
player_max_health = 100
game_over = False
game_win = False
waiting_for_next_level = False
game_state = "menu"
last_update_time = 0

# Kỹ năng Rapid Fire
rapid_fire_active = False
rapid_fire_duration = 5000
rapid_fire_cooldown = 10000
rapid_fire_start_time = 0
last_rapid_fire_use = 0

# Kỹ năng Spread Shot
spread_shot_active = False
spread_shot_duration = 3000
spread_shot_cooldown = 15000
spread_shot_start_time = 0
last_spread_shot_use = 0

# Đạn của người chơi
bullet_width = 5
bullet_height = 15
bullet_color = WHITE
bullet_speed = -10
bullets = []
base_fire_rate = 250
rapid_fire_rate = 50
last_shot = pygame.time.get_ticks()
bullet_damage = 10

# Vật phẩm hồi máu
health_pack_width = 20
health_pack_height = 20
health_pack_color = GREEN
health_packs = []
health_restore_amount = 25
health_pack_speed = 2
health_pack_drop_rate = 300

# Mìn sát thương
damage_mines = []
mine_width = 20
mine_height = 20
mine_color = PURPLE
mine_speed = 2
mine_effect_duration = 5000
is_slowed = False
slowed_start_time = 0

# Kẻ địch thông thường
enemy_width = 50
enemy_height = 50
enemy_speed = 3
enemies = []

# Thiên thạch
meteors = []
meteor_speed_min = 2
meteor_speed_max = 5
meteor_size_min = 15
meteor_size_max = 40
meteor_damage = 20

# Boss
BOSS_LEVEL = 5
boss_width = 200
boss_height = 80
boss_color = ORANGE
boss_speed_x = 2
boss_speed_y = 0.5
boss_max_health = 200
boss_health = boss_max_health
boss_rect = None
boss_fire_rate = 1000
last_boss_shot = pygame.time.get_ticks()

# Đạn của boss
boss_bullet_width = 10
boss_bullet_height = 10
boss_bullet_color = YELLOW
boss_bullet_speed = 5
boss_bullets = []

# Hộp quà
gift_boxes = []
gift_box_width = 20
gift_box_height = 20
gift_box_color = GOLD
gift_box_speed = 2
max_gift_boxes = 10

# Điểm số và Font chữ
score = 0
high_score = 0
current_level = 1
level_up_score = 10
upgrade_points = 0
# Màn hình nâng cấp
upgrade_buttons = {
       "speed": {"level": 0, "max_level": 5, "cost": 20, "rect": pygame.Rect(0, 0, 300, 50)},
    "fire_rate": {"level": 0, "max_level": 5, "cost": 25, "rect": pygame.Rect(0, 0, 300, 50)},
    "bullet_power": {"level": 0, "max_level": 5, "cost": 30, "rect": pygame.Rect(0, 0, 300, 50)},
    "health_boost": {"level": 0, "max_level": 5, "cost": 35, "rect": pygame.Rect(0, 0, 300, 50)},
}

shop_items = {
    "armor": {"cost": 50},
    "damage_boost": {"cost": 40}
}

# --- Định nghĩa Font chữ (Đã sửa) ---
# Thử dùng Times New Roman. Nếu Times New Roman không có sẵn hoặc không hỗ trợ tiếng Việt,
# sẽ fallback về font Arial.
try:
    font_large = pygame.font.SysFont("timesnewroman", 72)
    font_medium = pygame.font.SysFont("timesnewroman", 36)
    font_small = pygame.font.SysFont("timesnewroman", 24)
    font_tiny = pygame.font.SysFont("timesnewroman", 18)
    
    # Thử render một ký tự tiếng Việt để kiểm tra font
    test_surface = font_medium.render("Đ", True, WHITE)
    if test_surface.get_width() == 0 or test_surface.get_height() == 0:
        raise ValueError("Font Times New Roman không hỗ trợ ký tự tiếng Việt hoặc lỗi.")
except Exception as e:
    print(f"Lỗi tải hoặc hiển thị font Times New Roman: {e}. Chuyển sang font Arial.")
    font_large = pygame.font.SysFont("arial", 72)
    font_medium = pygame.font.SysFont("arial", 36)
    font_small = pygame.font.SysFont("arial", 24)
    font_tiny = pygame.font.SysFont("arial", 18)

# --- Cốt truyện ---
story_data = {
    "start": "Trong một tương lai không xa, nhân loại đối mặt với mối đe dọa từ Liên Minh Zergons. "
             "Bạn là hy vọng cuối cùng của Trái đất. "
             "Hãy lái chiếc phi thuyền Thiên Long và tiêu diệt hạm đội kẻ thù!",
    5: "Màn 5: Thủ lĩnh Tiền tuyến xuất hiện! Con tàu này được trang bị vũ khí mạnh mẽ, hãy cẩn thận!",
    10: "Màn 10: Đại soái Zergons, chỉ huy tối cao của hạm đội xâm lăng, đã xuất hiện. "
        "Hắn là mục tiêu cuối cùng của chúng ta. Chúc may mắn!",
}

# --- Định Nghĩa Các Hàm và Class ---

class Enemy(pygame.Rect):
    def __init__(self, x, y, width, height, speed, health, color, score_value):
        super().__init__(x, y, width, height)
        self.speed = speed
        self.health = health
        self.max_health = health
        self.color = color
        self.score_value = score_value

class FastEnemy(Enemy):
    def __init__(self):
        super().__init__(random.randint(0, SCREEN_WIDTH - 40), -40, 40, 40, 5, 5, YELLOW, 3)

class TankEnemy(Enemy):
    def __init__(self):
        super().__init__(random.randint(0, SCREEN_WIDTH - 60), -60, 60, 60, 2, 20, DARK_RED, 5)

class SpecialEnemy(Enemy):
    def __init__(self):
        super().__init__(random.randint(0, SCREEN_WIDTH - 50), -50, 50, 50, 3, 10, PURPLE, 10)
        self.has_boss_bullet = True

class Meteor(pygame.Rect):
    def __init__(self):
        size = random.randint(meteor_size_min, meteor_size_max)
        super().__init__(random.randint(0, SCREEN_WIDTH - size), -size, size, size)
        self.speed = random.randint(meteor_speed_min, meteor_speed_max)
        self.color = BROWN

class GiftBox(pygame.Rect):
    def __init__(self):
        super().__init__(random.randint(0, SCREEN_WIDTH - gift_box_width), -gift_box_height, gift_box_width, gift_box_height)
        self.speed = gift_box_speed
        self.color = gift_box_color
        self.score_value = random.randint(5, 10)

class DamageMine(pygame.Rect):
    def __init__(self):
        super().__init__(random.randint(0, SCREEN_WIDTH - mine_width), -mine_height, mine_width, mine_height)
        self.speed = mine_speed
        self.color = mine_color

def create_enemy():
    """Tạo một kẻ địch mới với vị trí ngẫu nhiên."""
    enemy_type = random.randint(1, 10)
    if enemy_type <= 5:
        return Enemy(random.randint(0, SCREEN_WIDTH - enemy_width), -enemy_height, enemy_width, enemy_height, enemy_speed, 10, RED, 1)
    elif enemy_type <= 8:
        return FastEnemy()
    elif enemy_type <= 9:
        return TankEnemy()
    else:
        return SpecialEnemy()

def create_bullet():
    """Tạo một viên đạn mới tại vị trí của phi thuyền."""
    return pygame.Rect(player_rect.centerx - bullet_width // 2, player_rect.top, bullet_width, bullet_height)

def create_health_pack():
    """Tạo một vật phẩm hồi máu mới."""
    x = random.randint(0, SCREEN_WIDTH - health_pack_width)
    y = -health_pack_height
    return pygame.Rect(x, y, health_pack_width, health_pack_height)

def create_spread_shot():
    """Tạo nhiều viên đạn theo hình quạt cho kỹ năng Spread Shot."""
    bullets = []
    angle_step = math.pi / 8
    start_angle = -math.pi / 4
    for i in range(5):
        angle = start_angle + i * angle_step
        velocity_x = math.sin(angle) * -bullet_speed
        velocity_y = math.cos(angle) * bullet_speed
        
        bullets.append({
            'rect': pygame.Rect(player_rect.centerx - bullet_width // 2, player_rect.top, bullet_width, bullet_height),
            'velocity_x': velocity_x,
            'velocity_y': velocity_y
        })
    return bullets

def create_boss():
    """Tạo boss."""
    global boss_rect, boss_health, boss_max_health
    boss_rect = pygame.Rect(SCREEN_WIDTH // 2 - boss_width // 2, -boss_height, boss_width, boss_height)
    if current_level == 10:
        boss_max_health = 400
    boss_health = boss_max_health
    
def create_boss_bullet():
    """Tạo một viên đạn của boss."""
    return pygame.Rect(boss_rect.centerx - boss_bullet_width // 2, boss_rect.bottom, boss_bullet_width, boss_bullet_height)

def create_triple_shot():
    """Tạo 3 viên đạn của boss bắn ra 3 hướng khác nhau."""
    bullets = []
    angle_offset = math.radians(15)
    for i in range(-1, 2):
        angle = math.pi / 2 + (i * angle_offset)
        vx = math.cos(angle) * -boss_bullet_speed
        vy = math.sin(angle) * boss_bullet_speed
        bullets.append({
            'rect': pygame.Rect(boss_rect.centerx - boss_bullet_width // 2, boss_rect.bottom, boss_bullet_width, boss_bullet_height),
            'velocity_x': -vx,
            'velocity_y': -vy
        })
    return bullets

def load_high_score():
    """Đọc điểm số cao nhất từ file."""
    global high_score
    try:
        with open("high_score.txt", "r") as file:
            high_score = int(file.read())
    except (FileNotFoundError, ValueError):
        high_score = 0

def save_high_score():
    """Lưu điểm số cao nhất vào file."""
    global high_score
    if score > high_score:
        high_score = score
        with open("high_score.txt", "w") as file:
            file.write(str(high_score))

def reset_game_state():
    """Thiết lập lại trạng thái game về ban đầu."""
    global enemies, bullets, health_packs, player_health, game_win, game_over, boss_rect, boss_health, boss_bullets, score, current_level, player_speed, bullet_speed, enemy_speed, player_rect, last_boss_shot, boss_bullet_speed, boss_max_health, meteors, rapid_fire_active, last_rapid_fire_use, bullet_damage, gift_boxes, damage_mines, is_slowed, base_player_speed, spread_shot_active, last_spread_shot_use, player_max_health, level_up_score, upgrade_points, upgrade_buttons, shop_items
    
    enemies.clear()
    bullets.clear()
    health_packs.clear()
    boss_bullets.clear()
    meteors.clear()
    gift_boxes.clear()
    damage_mines.clear()
    
    player_max_health = 100
    player_health = player_max_health
    player_rect.x = SCREEN_WIDTH // 2 - player_width // 2
    player_rect.y = SCREEN_HEIGHT - player_height
    
    game_win = False
    game_over = False
    boss_rect = None
    boss_max_health = 200
    boss_health = boss_max_health
    score = 0
    current_level = 1
    level_up_score = 10
    
    # Reset các chỉ số về mặc định ban đầu
    base_player_speed = 5
    player_speed = base_player_speed
    bullet_damage = 10
    base_fire_rate = 250
    
    enemy_speed = 3
    boss_bullet_speed = 5
    last_boss_shot = pygame.time.get_ticks()
    
    # Reset kỹ năng và hiệu ứng
    rapid_fire_active = False
    last_rapid_fire_use = 0
    spread_shot_active = False
    last_spread_shot_use = 0
    is_slowed = False

    upgrade_points = 0
    for key in upgrade_buttons:
        upgrade_buttons[key]["level"] = 0
    
def advance_level():
    """Tăng cấp độ, tăng độ khó và thiết lập lại game cho màn mới."""
    global current_level, enemy_speed, level_up_score, player_speed, bullet_damage, boss_max_health, boss_speed_x, boss_speed_y, player_max_health, score, upgrade_points, game_state, rapid_fire_active, spread_shot_active, is_slowed
    
    # Cộng điểm nâng cấp khi qua màn
    upgrade_points += 5
    
    current_level += 1
    
    # Tăng độ khó chung
    enemy_speed += 0.5
    
    # Tặng điểm khi qua màn
    score += 50
    
    # Tự động tăng sức mạnh cho người chơi
    player_speed += 0.5
    bullet_damage += 2
    player_max_health += 25
    player_health = player_max_health # Hồi đầy máu

    level_up_score += 15

    # Tăng độ khó cho boss khi lên level boss tiếp theo
    if current_level % BOSS_LEVEL == 0:
        boss_max_health += 100
        boss_speed_x += 0.5
        boss_speed_y += 0.1
        # Chuyển sang màn cốt truyện trước khi vào màn boss
        if current_level == 5 or current_level == 10:
            game_state = "story"
        else: # Các màn boss khác (nếu có) sẽ vào thẳng
            game_state = "playing"
            create_boss()
        
        if current_level == 10:
            boss_bullet_speed = 7
            boss_max_health = 400
    else:
        # Nếu là màn thường, chuyển thẳng sang màn chơi
        game_state = "playing"
        
    # Đặt lại trạng thái kỹ năng và hiệu ứng khi qua màn
    rapid_fire_active = False
    spread_shot_active = False
    is_slowed = False

def show_game_over_screen():
    """Hiển thị màn hình game over."""
    screen.fill(BLACK)
    game_over_text = font_large.render("GAME OVER", True, DARK_RED)
    score_text = font_medium.render(f"Điểm số của bạn: {score}", True, WHITE)
    high_score_text = font_medium.render(f"Điểm cao nhất: {high_score}", True, GOLD)
    continue_text = font_medium.render("Nhấn ENTER để chơi lại", True, WHITE)
    
    game_over_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 100))
    score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 30))
    high_score_rect = high_score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 10))
    continue_rect = continue_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 80))
    
    screen.blit(game_over_text, game_over_rect)
    screen.blit(score_text, score_rect)
    screen.blit(high_score_text, high_score_rect)
    screen.blit(continue_text, continue_rect)
    
    pygame.display.flip()

def main_menu():
    """Hàm hiển thị menu chính của game."""
    global start_game_rect, tutorial_rect
    screen.fill(BLACK)
    title_text = font_large.render("BẢO VỆ TRÁI ĐẤT", True, GOLD)
    start_text = font_medium.render("BẮT ĐẦU CHƠI", True, WHITE)
    tutorial_text = font_medium.render("HƯỚNG DẪN CHƠI", True, WHITE)
    high_score_text = font_medium.render(f"Điểm cao nhất: {high_score}", True, GOLD)
    
    title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 100))
    start_game_rect = start_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
    tutorial_rect = tutorial_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 60))
    high_score_rect = high_score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 120))
    
    screen.blit(title_text, title_rect)
    pygame.draw.rect(screen, WHITE, start_game_rect, 2)
    screen.blit(start_text, start_game_rect)
    pygame.draw.rect(screen, WHITE, tutorial_rect, 2)
    screen.blit(tutorial_text, tutorial_rect)
    screen.blit(high_score_text, high_score_rect)
    pygame.display.flip()
    
def show_tutorial_screen():
    """Hàm hiển thị màn hình hướng dẫn và bảng màu chung."""
    screen.fill(BLACK)

    # Tiêu đề
    title_text = font_large.render("HƯỚNG DẪN & BẢNG MÀU", True, GOLD)
    title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, 50))
    screen.blit(title_text, title_rect)

    # Hướng dẫn điều khiển
    controls_title = font_medium.render("ĐIỀU KHIỂN", True, WHITE)
    controls_title_rect = controls_title.get_rect(midleft=(50, 120))
    screen.blit(controls_title, controls_title_rect)
    
    controls_text = [
        ("Di chuyển", "Mũi tên TRÁI / PHẢI"),
        ("Bắn đạn", "Phím SPACE"),
        ("Kỹ năng Bắn Nhanh", "Phím R (Hồi chiêu 10s)"),
        ("Kỹ năng Đạn Chùm", "Phím S (Hồi chiêu 15s)")
    ]

    y_pos = 160
    for text, key in controls_text:
        line = font_small.render(f"- {text}: {key}", True, WHITE)
        rect = line.get_rect(midleft=(50, y_pos))
        screen.blit(line, rect)
        y_pos += 30

    # Bảng màu
    color_title = font_medium.render("BẢNG MÀU", True, WHITE)
    color_title_rect = color_title.get_rect(midleft=(450, 120))
    screen.blit(color_title, color_title_rect)

    guide_items = [
        ("Xanh dương", BLUE, "Phi thuyền của bạn"),
        ("Trắng", WHITE, "Đạn của bạn"),
        ("Đỏ", RED, "Kẻ địch thường"),
        ("Vàng", YELLOW, "Kẻ địch nhanh"),
        ("Đỏ sẫm", DARK_RED, "Kẻ địch xe tăng"),
        ("Tím", PURPLE, "Kẻ địch đặc biệt & Mìn"),
        ("Nâu", BROWN, "Thiên thạch"),
        ("Vàng kim", GOLD, "Hộp quà"),
        ("Xanh lá", GREEN, "Vật phẩm hồi máu"),
        ("Cam", ORANGE, "Boss"),
    ]

    y_start = 160
    for color_name, color, description in guide_items:
        color_box = pygame.Rect(450, y_start, 20, 20)
        pygame.draw.rect(screen, color, color_box)
        
        guide_text = font_small.render(f"- {description}", True, WHITE)
        guide_rect = guide_text.get_rect(midleft=(480, y_start + 10))
        screen.blit(guide_text, guide_rect)
        y_start += 30

    back_text = font_medium.render("NHẤN ENTER ĐỂ QUAY LẠI MENU", True, WHITE)
    back_rect = back_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50))
    screen.blit(back_text, back_rect)
    
    pygame.display.flip()

def show_story_screen(story_text):
    """Hàm hiển thị màn hình cốt truyện với hiệu ứng nhấp nháy."""
    global last_update_time
    screen.fill(BLACK)
    
    story_lines = story_text.split('.')
    y_pos = SCREEN_HEIGHT // 2 - len(story_lines) * 20
    
    for line in story_lines:
        line = line.strip()
        if line:
            story_surface = font_small.render(line + ".", True, WHITE)
            story_rect = story_surface.get_rect(center=(SCREEN_WIDTH // 2, y_pos))
            screen.blit(story_surface, story_rect)
            y_pos += 40
    
    now = pygame.time.get_ticks()
    press_enter_text = font_medium.render("Nhấn ENTER để tiếp tục...", True, GOLD)
    press_enter_rect = press_enter_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 100))
    if int(now / 500) % 2 == 0:
        screen.blit(press_enter_text, press_enter_rect)
    
    pygame.display.flip()
        
def draw_game_elements():
    """Hàm vẽ tất cả các đối tượng trong game."""
    screen.fill(BLACK)
    
    # Vẽ người chơi
    pygame.draw.rect(screen, BLUE, player_rect)
    
    # Vẽ các viên đạn của người chơi
    for bullet in bullets:
        if isinstance(bullet, dict):
            pygame.draw.rect(screen, WHITE, bullet['rect'])
        else:
            pygame.draw.rect(screen, bullet_color, bullet)
        
    # Vẽ kẻ địch
    for enemy in enemies:
        pygame.draw.rect(screen, enemy.color, enemy)
        health_bar_width = (enemy.health / enemy.max_health) * enemy.width
        health_bar_rect = pygame.Rect(enemy.left, enemy.top - 5, health_bar_width, 3)
        pygame.draw.rect(screen, DARK_GREEN, health_bar_rect)
        
    # Vẽ thiên thạch
    for meteor in meteors:
        pygame.draw.rect(screen, meteor.color, meteor)
        
    # Vẽ vật phẩm hồi máu
    for health_pack in health_packs:
        pygame.draw.rect(screen, health_pack_color, health_pack)
        
    # Vẽ hộp quà
    for gift_box in gift_boxes:
        pygame.draw.rect(screen, gift_box.color, gift_box)
        
    # Vẽ mìn sát thương
    for mine in damage_mines:
        pygame.draw.rect(screen, mine.color, mine)
        
    # Vẽ đạn của boss
    for boss_bullet in boss_bullets:
        pygame.draw.rect(screen, boss_bullet_color, boss_bullet['rect'])
        
    # Vẽ boss và thanh máu
    if boss_rect:
        pygame.draw.rect(screen, boss_color, boss_rect)
        boss_health_bar_width = (boss_health / boss_max_health) * boss_width
        boss_health_bar = pygame.Rect(boss_rect.left, boss_rect.top - 10, boss_health_bar_width, 5)
        pygame.draw.rect(screen, GREEN, boss_health_bar)
        
    # Vẽ thông tin game
    level_surface = font_medium.render(f"Màn chơi: {current_level}", True, WHITE)
    score_surface = font_medium.render(f"Điểm số: {score}", True, WHITE)
    health_surface = font_medium.render(f"Máu: {player_health}/{player_max_health}", True, WHITE)
    
    screen.blit(level_surface, (10, 10))
    screen.blit(score_surface, (10, 40))
    
    # Hiển thị mục tiêu nếu không phải màn boss
    if current_level % BOSS_LEVEL != 0:
        level_up_score_surface = font_medium.render(f"Mục tiêu: {level_up_score}", True, WHITE)
        screen.blit(level_up_score_surface, (10, 70))
        screen.blit(health_surface, (10, 100))
    else:
        screen.blit(health_surface, (10, 70))
        
    # Vẽ trạng thái kỹ năng Rapid Fire
    now = pygame.time.get_ticks()
    cooldown_progress_r = min(1.0, (now - last_rapid_fire_use) / rapid_fire_cooldown)
    cooldown_bar_bg_r = pygame.Rect(SCREEN_WIDTH - 160, SCREEN_HEIGHT - 30, 150, 20)
    pygame.draw.rect(screen, BLACK, cooldown_bar_bg_r)
    pygame.draw.rect(screen, WHITE, cooldown_bar_bg_r, 2)
    cooldown_bar_fill_r = pygame.Rect(SCREEN_WIDTH - 160, SCREEN_HEIGHT - 30, 150 * cooldown_progress_r, 20)
    pygame.draw.rect(screen, CYAN, cooldown_bar_fill_r)
    skill_text_r = font_small.render("KỸ NĂNG: R", True, WHITE)
    screen.blit(skill_text_r, (SCREEN_WIDTH - 155, SCREEN_HEIGHT - 28))
    
    # Vẽ trạng thái kỹ năng Spread Shot
    cooldown_progress_s = min(1.0, (now - last_spread_shot_use) / spread_shot_cooldown)
    cooldown_bar_bg_s = pygame.Rect(SCREEN_WIDTH - 160, SCREEN_HEIGHT - 60, 150, 20)
    pygame.draw.rect(screen, BLACK, cooldown_bar_bg_s)
    pygame.draw.rect(screen, WHITE, cooldown_bar_bg_s, 2)
    cooldown_bar_fill_s = pygame.Rect(SCREEN_WIDTH - 160, SCREEN_HEIGHT - 60, 150 * cooldown_progress_s, 20)
    pygame.draw.rect(screen, GOLD, cooldown_bar_fill_s)
    skill_text_s = font_small.render("ĐẠN CHÙM: S", True, WHITE)
    screen.blit(skill_text_s, (SCREEN_WIDTH - 155, SCREEN_HEIGHT - 58))
    
    pygame.display.flip()

def draw_upgrade_screen():
    """Hàm vẽ màn hình nâng cấp phi thuyền."""
    global upgrade_points, player_max_health, player_health, bullet_damage, base_fire_rate, player_speed
    
    screen.fill(BLACK)
    
    title_text = font_large.render("NÂNG CẤP PHI THUYỀN", True, GOLD)
    upgrade_points_text = font_medium.render(f"Điểm nâng cấp: {upgrade_points}", True, WHITE)
    
    title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, 80))
    upgrade_points_rect = upgrade_points_text.get_rect(center=(SCREEN_WIDTH // 2, 140))
    
    screen.blit(title_text, title_rect)
    screen.blit(upgrade_points_text, upgrade_points_rect)
    
    y_pos = 220
    for key, item in upgrade_buttons.items():
        if key == "speed": text = f"Tốc độ di chuyển"
        elif key == "fire_rate": text = f"Tốc độ bắn"
        elif key == "bullet_power": text = f"Sát thương đạn"
        elif key == "health_boost": text = f"Máu tối đa"
        
        display_text = f"{text} Cấp {item['level']}/{item['max_level']} - Giá: {item['cost']}"
        
        can_upgrade = upgrade_points >= item['cost'] and item['level'] < item['max_level']
        
        if not can_upgrade:
            display_text += " (Thiếu)"
            color = GRAY
        else:
            color = WHITE
            
        button_rect = pygame.Rect(0, 0, 350, 50)
        button_rect.center = (SCREEN_WIDTH // 2, y_pos)
        item['rect'] = button_rect
        
        pygame.draw.rect(screen, color, button_rect, 2)
        item_text = font_medium.render(display_text, True, color)
        item_text_rect = item_text.get_rect(center=button_rect.center)
        screen.blit(item_text, item_text_rect)
        y_pos += 70

    continue_text = font_medium.render("TIẾP TỤC", True, GREEN)
    continue_button_rect = continue_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 80))
    pygame.draw.rect(screen, GREEN, continue_button_rect, 2)
    screen.blit(continue_text, continue_button_rect)

    pygame.display.flip()

def draw_shop_screen():
    """Hàm vẽ màn hình cửa hàng."""
    global upgrade_points, player_max_health, player_health, bullet_damage
    
    screen.fill(BLACK)

    title_text = font_large.render("CỬA HÀNG", True, GOLD)
    upgrade_points_text = font_medium.render(f"Điểm nâng cấp: {upgrade_points}", True, WHITE)
    back_text = font_medium.render("QUAY LẠI", True, WHITE)

    title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, 80))
    upgrade_points_rect = upgrade_points_text.get_rect(center=(SCREEN_WIDTH // 2, 140))
    back_button_rect = back_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 80))

    screen.blit(title_text, title_rect)
    screen.blit(upgrade_points_text, upgrade_points_rect)

    y_pos = 220
    for key, item in shop_items.items():
        if key == "armor": text = "Giáp (Tăng Máu)"
        elif key == "damage_boost": text = "Tăng Sát thương"
        
        display_text = f"{text} - Giá: {item['cost']}"
        can_buy = upgrade_points >= item['cost']

        color = WHITE if can_buy else GRAY
        if not can_buy:
            display_text += " (Thiếu)"
            
        button_rect = pygame.Rect(0, 0, 350, 50)
        button_rect.center = (SCREEN_WIDTH // 2, y_pos)
        item['rect'] = button_rect

        pygame.draw.rect(screen, color, button_rect, 2)
        item_text = font_medium.render(display_text, True, color)
        item_text_rect = item_text.get_rect(center=button_rect.center)
        screen.blit(item_text, item_text_rect)
        y_pos += 70

    pygame.draw.rect(screen, WHITE, back_button_rect, 2)
    screen.blit(back_text, back_button_rect)
    
    pygame.display.flip()

# --- Vòng Lặp Chính Của Game ---
load_high_score()
running = True
    
while running:
    # 1. Xử lý Sự kiện
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            save_high_score()
        
        if game_state == "menu":
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if start_game_rect.collidepoint(event.pos):
                    reset_game_state()
                    game_state = "story"
                elif tutorial_rect.collidepoint(event.pos):
                    game_state = "tutorial"
            
        elif game_state == "tutorial":
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                game_state = "menu"
        
        elif game_state == "story":
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                game_state = "playing"
                if current_level % BOSS_LEVEL == 0:
                    create_boss()
                else: 
                    for _ in range(5):
                        enemies.append(create_enemy())
        
        elif game_state == "UPGRADE_SCREEN":
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = event.pos
                
                continue_text = font_medium.render("TIẾP TỤC", True, GREEN)
                continue_rect = continue_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 80))

                if continue_rect.collidepoint(mouse_pos):
                    if waiting_for_next_level:
                        advance_level()
                        if current_level % BOSS_LEVEL != 0:
                            for _ in range(5):
                                enemies.append(create_enemy())
                        waiting_for_next_level = False
                    game_state = "playing"
                else:
                    for key, item in upgrade_buttons.items():
                        if item["rect"].collidepoint(mouse_pos):
                            if upgrade_points >= item["cost"] and item["level"] < item["max_level"]:
                                upgrade_points -= item["cost"]
                                item["level"] += 1
                                if key == "speed":
                                    player_speed += 1
                                    item["cost"] += 5
                                elif key == "fire_rate":
                                    base_fire_rate = max(50, base_fire_rate - 25)
                                    item["cost"] += 5
                                elif key == "bullet_power":
                                    bullet_damage += 5
                                    item["cost"] += 5
                                elif key == "health_boost":
                                    player_max_health += 25
                                    player_health = player_max_health
                                    item["cost"] += 5
        
        elif game_state == "SHOP_SCREEN":
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = event.pos
                
                back_text = font_medium.render("QUAY LẠI", True, WHITE)
                back_button_rect = back_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 80))

                if back_button_rect.collidepoint(mouse_pos):
                    game_state = "UPGRADE_SCREEN"
                else:
                    for key, item in shop_items.items():
                        if item['rect'].collidepoint(mouse_pos):
                            if upgrade_points >= item['cost']:
                                upgrade_points -= item['cost']
                                if key == "armor":
                                    player_max_health += 25
                                    player_health = player_max_health
                                elif key == "damage_boost":
                                    bullet_damage += 5
        
        elif game_state == "game_over":
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                reset_game_state()
                game_state = "menu"
        
    # --- 2. Cập nhật Trạng thái Game ---
    if game_state == "playing":
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player_rect.left > 0:
            player_rect.x -= player_speed
        if keys[pygame.K_RIGHT] and player_rect.right < SCREEN_WIDTH:
            player_rect.x += player_speed
            
        now = pygame.time.get_ticks()

        if keys[pygame.K_SPACE] and not game_over and not game_win:
            current_fire_rate = rapid_fire_rate if rapid_fire_active else base_fire_rate
            if is_slowed:
                current_fire_rate = base_fire_rate * 3
            if now - last_shot > current_fire_rate:
                if spread_shot_active:
                    new_bullets = create_spread_shot()
                    bullets.extend(new_bullets)
                else:
                    bullets.append(create_bullet())
                last_shot = now

        if keys[pygame.K_r] and now - last_rapid_fire_use > rapid_fire_cooldown:
            # if sound_enabled and skill_sound:
            #     skill_sound.play()
            rapid_fire_active = True
            rapid_fire_start_time = now
            last_rapid_fire_use = now

        if rapid_fire_active and now - rapid_fire_start_time > rapid_fire_duration:
            rapid_fire_active = False

        if keys[pygame.K_s] and now - last_spread_shot_use > spread_shot_cooldown:
            # if sound_enabled and skill_sound:
            #     skill_sound.play()
            spread_shot_active = True
            spread_shot_start_time = now
            last_spread_shot_use = now

        if spread_shot_active and now - spread_shot_start_time > spread_shot_duration:
            spread_shot_active = False

        # Hồi phục tốc độ sau khi bị làm chậm
        if is_slowed and now - slowed_start_time > mine_effect_duration:
            is_slowed = False

        # Cập nhật vị trí đạn của người chơi
        for bullet in bullets[:]:
            if isinstance(bullet, dict):
                bullet['rect'].x += bullet['velocity_x']
                bullet['rect'].y += bullet['velocity_y']
                if bullet['rect'].bottom < 0 or bullet['rect'].left > SCREEN_WIDTH or bullet['rect'].right < 0:
                    bullets.remove(bullet)
            else:
                bullet.y += bullet_speed
                if bullet.bottom < 0:
                    bullets.remove(bullet)

        # Cập nhật vị trí kẻ địch
        for enemy in enemies[:]:
            enemy.y += enemy.speed
            if enemy.top > SCREEN_HEIGHT:
                enemies.remove(enemy)
            
        # Cập nhật vị trí thiên thạch
        for meteor in meteors[:]:
            meteor.y += meteor.speed
            if meteor.top > SCREEN_HEIGHT:
                meteors.remove(meteor)

        # Cập nhật vị trí mìn
        for mine in damage_mines[:]:
            mine.y += mine.speed
            if mine.top > SCREEN_HEIGHT:
                damage_mines.remove(mine)
            
        # Cập nhật vị trí vật phẩm hồi máu
        for health_pack in health_packs[:]:
            health_pack.y += health_pack_speed
            if health_pack.top > SCREEN_HEIGHT:
                health_packs.remove(health_pack)
            if player_rect.colliderect(health_pack):
                health_packs.remove(health_pack)
                player_health = min(player_max_health, player_health + health_restore_amount)

        # Cập nhật vị trí hộp quà
        for gift_box in gift_boxes[:]:
            gift_box.y += gift_box_speed
            if gift_box.top > SCREEN_HEIGHT:
                gift_boxes.remove(gift_box)
            if player_rect.colliderect(gift_box):
                gift_boxes.remove(gift_box)
                upgrade_points += gift_box.score_value
                # Tạo ngẫu nhiên một vật phẩm mới từ hộp quà
                random_item = random.randint(1, 10)
                if random_item <= 3:
                    player_health = min(player_max_health, player_health + 10)
                elif random_item <= 6:
                    bullet_damage += 1
                elif random_item <= 9:
                    player_speed += 0.5
                else:
                    base_fire_rate = max(50, base_fire_rate - 10)


        # Cập nhật vị trí đạn của boss
        for boss_bullet in boss_bullets[:]:
            boss_bullet['rect'].x += boss_bullet['velocity_x']
            boss_bullet['rect'].y += boss_bullet['velocity_y']
            if boss_bullet['rect'].top > SCREEN_HEIGHT or boss_bullet['rect'].left > SCREEN_WIDTH or boss_bullet['rect'].right < 0:
                boss_bullets.remove(boss_bullet)
            if player_rect.colliderect(boss_bullet['rect']):
                player_health -= 25
                boss_bullets.remove(boss_bullet)
                if player_health <= 0:
                    game_over = True
                    save_high_score()

        # Kiểm tra va chạm giữa đạn của người chơi và kẻ địch/boss
        for bullet in bullets[:]:
            for enemy in enemies[:]:
                if bullet.colliderect(enemy):
                    enemy.health -= bullet_damage
                    if enemy.health <= 0:
                        enemies.remove(enemy)
                        score += enemy.score_value
                        if isinstance(enemy, SpecialEnemy):
                            gift_boxes.append(GiftBox())
                            damage_mines.append(DamageMine())
                        if random.randint(1, 100) < 10:
                            health_packs.append(create_health_pack())
                    if bullet in bullets:
                        bullets.remove(bullet)
                    break
            if boss_rect and bullet.colliderect(boss_rect):
                boss_health -= bullet_damage
                if bullet in bullets:
                    bullets.remove(bullet)
                if boss_health <= 0:
                    score += 100
                    boss_rect = None
                    waiting_for_next_level = True
                    game_state = "UPGRADE_SCREEN"
                break

        # Sinh kẻ địch
        if current_level % BOSS_LEVEL != 0:
            if now - last_update_time > 1500 and len(enemies) < 10:
                enemies.append(create_enemy())
                last_update_time = now
            if score >= level_up_score:
                waiting_for_next_level = True
                game_state = "UPGRADE_SCREEN"
                
        # Sinh thiên thạch
        if current_level >= 3 and random.randint(1, 200) == 1:
            meteors.append(Meteor())

        # Boss di chuyển và bắn đạn
        if boss_rect:
            boss_rect.x += boss_speed_x
            if boss_rect.left < 0 or boss_rect.right > SCREEN_WIDTH:
                boss_speed_x *= -1
            boss_rect.y += boss_speed_y
            if boss_rect.y > 100 or boss_rect.y < 50:
                boss_speed_y *= -1
            if now - last_boss_shot > boss_fire_rate:
                boss_bullets.extend(create_triple_shot())
                last_boss_shot = now

        draw_game_elements()
    
    elif game_state == "menu":
        main_menu()
    
    elif game_state == "tutorial":
        show_tutorial_screen()
    
    elif game_state == "story":
        story_text = story_data.get(current_level, story_data.get("start"))
        show_story_screen(story_text)
    
    elif game_state == "game_over":
        show_game_over_screen()
        
    elif game_state == "UPGRADE_SCREEN":
        draw_upgrade_screen()
    
    elif game_state == "SHOP_SCREEN":
        draw_shop_screen()
        
    clock.tick(FPS)
    
pygame.quit()
