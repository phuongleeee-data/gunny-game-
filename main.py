# gunny-game-
import pygame
import random
import os
import sys

# Khởi tạo pygame
pygame.init()

# Cài đặt màn hình
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Game Ban Ga Trong Chuong")

# Màu sắc
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BROWN = (139, 69, 19)
YELLOW = (255, 255, 0)

# Font chữ
try:
    # Thử sử dụng font hệ thống hỗ trợ tiếng Việt
    font = pygame.font.SysFont("Arial", 36)
    small_font = pygame.font.SysFont("Arial", 24)
except:
    # Nếu không có font hỗ trợ, sử dụng font mặc định
    font = pygame.font.Font(None, 36)
    small_font = pygame.font.Font(None, 24)

# Biến toàn cục
level = 1
score = 0
escaped_chickens = 0
max_escaped = 5
game_active = True
chickens_to_spawn = 10  # Số gà mỗi level

# Lớp súng (người chơi)
class Gun(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # Tạo hình súng đơn giản
        self.image = pygame.Surface((60, 20))
        self.image.fill(BLACK)
        pygame.draw.rect(self.image, BROWN, (0, 0, 40, 20))
        pygame.draw.rect(self.image, BLACK, (40, 5, 20, 10))
        
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH // 2
        self.rect.bottom = HEIGHT - 10
        self.cooldown = 0
        self.ammo = 30  # Tăng số đạn ban đầu

    def update(self):
        # Di chuyển súng theo chuột
        pos = pygame.mouse.get_pos()
        self.rect.centerx = pos[0]
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        
        # Giảm thời gian chờ bắn
        if self.cooldown > 0:
            self.cooldown -= 1

    def shoot(self):
        if self.cooldown == 0 and self.ammo > 0:
            bullet = Bullet(self.rect.centerx, self.rect.top)
            all_sprites.add(bullet)
            bullets.add(bullet)
            self.cooldown = 10  # Thời gian chờ giữa các lần bắn
            self.ammo -= 1
            return True
        return False

    def reload(self, amount=10):
        self.ammo += amount

# Lớp gà
class Chicken(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # Kích thước gà ngẫu nhiên (càng lớn càng béo, điểm càng cao)
        self.size = random.randint(30, 60)
        self.weight = self.size - 20  # Trọng lượng gà (điểm)
        
        # Tạo hình gà đơn giản với kích thước tương ứng
        self.image = pygame.Surface((self.size, self.size), pygame.SRCALPHA)
        
        # Vẽ thân gà
        pygame.draw.circle(self.image, YELLOW, (self.size//2, self.size//2), self.size//2)
        
        # Vẽ mỏ gà
        pygame.draw.polygon(self.image, RED, [
            (self.size-5, self.size//2-5),
            (self.size+5, self.size//2),
            (self.size-5, self.size//2+5)
        ])
        
        # Vẽ mắt gà
        pygame.draw.circle(self.image, BLACK, (self.size-15, self.size//2-8), 3)
        
        self.rect = self.image.get_rect()
        
        # Vị trí ban đầu (trong chuồng gà)
        self.rect.x = random.randint(50, WIDTH-100)
        self.rect.y = random.randint(50, HEIGHT-200)
        
        # Tốc độ di chuyển
        self.speed = max(1, 6 - self.size//10)  # Gà càng béo càng chậm
        self.direction = random.choice([(1, 0), (-1, 0), (0, 1), (0, -1), 
                                       (1, 1), (-1, 1), (1, -1), (-1, -1)])
        self.direction_timer = random.randint(30, 100)
        
        # Xác suất gà chạy ra khỏi chuồng
        self.escape_chance = 0.002 * level  # Tăng theo level, tăng gấp đôi để gà dễ xổng chuồng hơn

    def update(self):
        global escaped_chickens  # Khai báo global ở đầu phương thức
        
        # Đếm ngược thời gian đổi hướng
        self.direction_timer -= 1
        if self.direction_timer <= 0:
            self.direction = random.choice([(1, 0), (-1, 0), (0, 1), (0, -1), 
                                           (1, 1), (-1, 1), (1, -1), (-1, -1)])
            self.direction_timer = random.randint(30, 100)
        
        # Di chuyển gà
        old_x = self.rect.x
        old_y = self.rect.y
        self.rect.x += self.direction[0] * self.speed
        self.rect.y += self.direction[1] * self.speed
        
        # Kiểm tra xem gà có di chuyển quá xa không
        if abs(self.rect.x - old_x) > self.speed * 2 or abs(self.rect.y - old_y) > self.speed * 2:
            # Nếu di chuyển quá xa, quay lại vị trí cũ
            self.rect.x = old_x
            self.rect.y = old_y
        
        # Giữ gà trong chuồng (phần lớn thời gian)
        if self.rect.left < 50:
            if random.random() < self.escape_chance:
                # Gà có thể xổng chuồng
                if self.rect.right < 0:
                    self.kill()
                    escaped_chickens += 1
            else:
                self.rect.left = 50
                self.direction = random.choice([(1, 0), (0, 1), (0, -1), (1, 1), (1, -1)])
        
        if self.rect.right > WIDTH-50:
            if random.random() < self.escape_chance:
                # Gà có thể xổng chuồng
                if self.rect.left > WIDTH:
                    self.kill()
                    escaped_chickens += 1
            else:
                self.rect.right = WIDTH-50
                self.direction = random.choice([(-1, 0), (0, 1), (0, -1), (-1, 1), (-1, -1)])
        
        if self.rect.top < 50:
            if random.random() < self.escape_chance:
                # Gà có thể xổng chuồng
                if self.rect.bottom < 0:
                    self.kill()
                    escaped_chickens += 1
            else:
                self.rect.top = 50
                self.direction = random.choice([(1, 0), (-1, 0), (0, 1), (1, 1), (-1, 1)])
        
        if self.rect.bottom > HEIGHT-50:
            if random.random() < self.escape_chance:
                # Gà có thể xổng chuồng
                if self.rect.top > HEIGHT:
                    self.kill()
                    escaped_chickens += 1
            else:
                self.rect.bottom = HEIGHT-50
                self.direction = random.choice([(1, 0), (-1, 0), (0, -1), (1, -1), (-1, -1)])

# Lớp đạn
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((8, 8))
        self.image.fill(BLACK)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        
        # Lấy vị trí chuột để xác định hướng đạn
        mouse_x, mouse_y = pygame.mouse.get_pos()
        
        # Tính toán vector hướng
        dx = mouse_x - x
        dy = mouse_y - y
        
        # Chuẩn hóa vector
        distance = (dx**2 + dy**2)**0.5
        if distance > 0:
            self.speed_x = dx / distance * 10
            self.speed_y = dy / distance * 10
        else:
            self.speed_x = 0
            self.speed_y = -10

    def update(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y
        
        # Xóa đạn nếu ra khỏi màn hình
        if (self.rect.bottom < 0 or self.rect.top > HEIGHT or 
            self.rect.right < 0 or self.rect.left > WIDTH):
            self.kill()

# Lớp hiệu ứng
class Effect(pygame.sprite.Sprite):
    def __init__(self, x, y, size):
        super().__init__()
        self.size = size
        self.image = pygame.Surface((size, size), pygame.SRCALPHA)
        pygame.draw.circle(self.image, RED, (size//2, size//2), size//2)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.timer = 10
    
    def update(self):
        self.timer -= 1
        if self.timer <= 0:
            self.kill()
        # Thu nhỏ hiệu ứng
        new_size = int(self.size * (self.timer / 10))
        if new_size > 0:
            self.image = pygame.Surface((new_size, new_size), pygame.SRCALPHA)
            pygame.draw.circle(self.image, RED, (new_size//2, new_size//2), new_size//2)
            old_center = self.rect.center
            self.rect = self.image.get_rect()
            self.rect.center = old_center

# Lớp vật phẩm
class PowerUp(pygame.sprite.Sprite):
    def __init__(self, x, y, type):
        super().__init__()
        self.type = type  # 'ammo' hoặc 'speed'
        self.image = pygame.Surface((20, 20))
        if type == 'ammo':
            self.image.fill(YELLOW)
        else:
            self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.timer = 300  # Tồn tại 5 giây
    
    def update(self):
        self.timer -= 1
        if self.timer <= 0:
            self.kill()

# Vẽ chuồng gà
def draw_coop():
    # Vẽ tường chuồng
    pygame.draw.rect(screen, BROWN, (40, 40, WIDTH-80, HEIGHT-80), 5)
    
    # Vẽ cửa chuồng
    pygame.draw.rect(screen, BROWN, (WIDTH//2-50, 35, 100, 10))
    pygame.draw.rect(screen, BROWN, (WIDTH//2-50, HEIGHT-45, 100, 10))
    pygame.draw.rect(screen, BROWN, (35, HEIGHT//2-50, 10, 100))
    pygame.draw.rect(screen, BROWN, (WIDTH-45, HEIGHT//2-50, 10, 100))

# Tạo các nhóm sprite
all_sprites = pygame.sprite.Group()
chickens = pygame.sprite.Group()
bullets = pygame.sprite.Group()
effects = pygame.sprite.Group()
powerups = pygame.sprite.Group()

# Tạo người chơi
gun = Gun()
all_sprites.add(gun)

# Tạo gà
def spawn_chickens(num):
    for i in range(num):
        chicken = Chicken()
        all_sprites.add(chicken)
        chickens.add(chicken)

# Hàm hiển thị thông tin
def show_info():
    # Hiển thị điểm
    score_text = font.render(f"Diem: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))
    
    # Hiển thị cấp độ
    level_text = font.render(f"Cap do: {level}/50", True, WHITE)
    screen.blit(level_text, (WIDTH//2 - level_text.get_width()//2, 10))
    
    # Hiển thị số gà còn lại
    chickens_text = font.render(f"Ga con lai: {len(chickens)}", True, WHITE)
    screen.blit(chickens_text, (10, 50))
    
    # Hiển thị số gà đã xổng chuồng
    escaped_text = font.render(f"Ga xong chuong: {escaped_chickens}/{max_escaped}", True, WHITE)
    screen.blit(escaped_text, (WIDTH - escaped_text.get_width() - 10, 10))
    
    # Hiển thị số đạn
    ammo_text = font.render(f"Dan: {gun.ammo}", True, WHITE)
    screen.blit(ammo_text, (WIDTH - ammo_text.get_width() - 10, 50))

# Hàm hiển thị màn hình kết thúc
def show_game_over(win=False):
    overlay = pygame.Surface((WIDTH, HEIGHT))
    overlay.set_alpha(180)
    overlay.fill(BLACK)
    screen.blit(overlay, (0, 0))
    
    if win:
        if level >= 50:
            title_text = font.render("CHUC MUNG! BAN DA HOAN THANH TRO CHOI!", True, GREEN)
        else:
            title_text = font.render(f"CHIEN THANG! LEVEL {level} HOAN THANH", True, GREEN)
    else:
        title_text = font.render("GAME OVER - QUA NHIEU GA XONG CHUONG!", True, RED)
    
    score_text = font.render(f"Diem so: {score}", True, WHITE)
    level_text = font.render(f"Cap do dat duoc: {level}/50", True, WHITE)
    
    if win and level < 50:
        continue_text = font.render("Nhan SPACE de tiep tuc level tiep theo", True, WHITE)
        screen.blit(continue_text, (WIDTH//2 - continue_text.get_width()//2, HEIGHT//2 + 50))
    
    restart_text = font.render("Nhan R de choi lai tu dau", True, WHITE)
    quit_text = font.render("Nhan Q de thoat", True, WHITE)
    
    screen.blit(title_text, (WIDTH//2 - title_text.get_width()//2, HEIGHT//2 - 100))
    screen.blit(score_text, (WIDTH//2 - score_text.get_width()//2, HEIGHT//2 - 50))
    screen.blit(level_text, (WIDTH//2 - level_text.get_width()//2, HEIGHT//2))
    screen.blit(restart_text, (WIDTH//2 - restart_text.get_width()//2, HEIGHT//2 + 100))
    screen.blit(quit_text, (WIDTH//2 - quit_text.get_width()//2, HEIGHT//2 + 150))

# Hàm khởi tạo level mới
def start_new_level():
    global chickens_to_spawn
    # Tăng số lượng gà theo level
    chickens_to_spawn = 10 + (level - 1) * 2
    # Tạo gà mới
    spawn_chickens(chickens_to_spawn)
    # Nạp đạn cho người chơi
    gun.ammo = 30 + (level // 5) * 10  # Tăng số đạn mỗi level

# Khởi tạo level đầu tiên
start_new_level()

# Vòng lặp game
clock = pygame.time.Clock()
running = True

while running:
    # Giữ tốc độ game
    clock.tick(60)
    
    # Xử lý sự kiện
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and game_active:
            if event.button == 1:  # Chuột trái
                gun.shoot()
        elif event.type == pygame.KEYDOWN:
            if not game_active:
                if event.key == pygame.K_r:
                    # Khởi động lại game
                    level = 1
                    score = 0
                    escaped_chickens = 0
                    game_active = True
                    
                    # Xóa tất cả sprite
                    all_sprites.empty()
                    chickens.empty()
                    bullets.empty()
                    effects.empty()
                    powerups.empty()
                    
                    # Tạo người chơi mới
                    gun = Gun()
                    all_sprites.add(gun)
                    
                    # Bắt đầu level mới
                    start_new_level()
                    
                elif event.key == pygame.K_q:
                    running = False
                elif event.key == pygame.K_SPACE and level < 50:
                    # Tiếp tục level tiếp theo
                    level += 1
                    escaped_chickens = 0
                    game_active = True
                    
                    # Xóa tất cả sprite
                    all_sprites.empty()
                    chickens.empty()
                    bullets.empty()
                    effects.empty()
                    powerups.empty()
                    
                    # Tạo người chơi mới
                    gun = Gun()
                    all_sprites.add(gun)
                    
                    # Bắt đầu level mới
                    start_new_level()

    if game_active:
        # Cập nhật
        all_sprites.update()
        # Kiểm tra va chạm giữa đạn và gà (sử dụng collide_rect để tăng độ chính xác) 
        hits = pygame.sprite.groupcollide(chickens, bullets, True, True, pygame.sprite.collide_rect)
        for chicken, bullet_list in hits.items():
            # Tăng điểm dựa trên trọng lượng gà
            score += chicken.weight
            
            # Tạo hiệu ứng
            effect = Effect(chicken.rect.centerx, chicken.rect.centery, chicken.size)
            all_sprites.add(effect)
            effects.add(effect)
            
            # Cơ hội rơi vật phẩm
            if random.random() < 0.2:  # 20% cơ hội
                powerup_type = random.choice(['ammo', 'speed'])
                powerup = PowerUp(chicken.rect.centerx, chicken.rect.centery, powerup_type)
                all_sprites.add(powerup)
                powerups.add(powerup)
        
        # Kiểm tra va chạm giữa súng và vật phẩm
        hits = pygame.sprite.spritecollide(gun, powerups, True)
        for powerup in hits:
            if powerup.type == 'ammo':
                gun.reload(5)
            else:
                # Tăng tốc độ súng (giảm cooldown)
                gun.cooldown = max(1, gun.cooldown - 2)
        
        # Kiểm tra điều kiện thắng/thua
        if len(chickens) == 0:
            # Thắng level
            game_active = False
        
        if escaped_chickens >= max_escaped:
            # Thua game
            game_active = False
        
        # Vẽ
        screen.fill(BLACK)
        
        # Vẽ chuồng gà
        draw_coop()
        
        # Vẽ các sprite
        all_sprites.draw(screen)
        
        # Hiển thị thông tin
        show_info()
    else:
        # Hiển thị màn hình kết thúc
        show_game_over(escaped_chickens < max_escaped)
    
    # Cập nhật màn hình
    pygame.display.flip()

pygame.quit()
sys.exit()
