
import time

import pygame
import json
pygame.init()

debug_mode = False

width = 700
height = 700

tile_size = 35

clock = pygame.time.Clock()

bg_music = pygame.mixer.Sound('Music/bgmusic.mp3')
death_music = pygame.mixer.Sound('Music/death.mp3')
coin_music = pygame.mixer.Sound('Music/coin.mp3')
jump_music = pygame.mixer.Sound('Music/jump.mp3')

game_over = 0
def_hp = 5
hp = def_hp
coins = 0
level_coins = 0

display = pygame.display.set_mode((width, height), vsync=1)
pygame.display.set_caption('Platformer')

bg_image = pygame.image.load('Icon/bg11.png')
bg_rect = bg_image.get_rect()

with open('Levels/level1.json', 'r') as file:
    world_data = json.load(file)

level_num = 1
max_level = 4

def reset_level():
    global level_coins
    global world_data
    player.rect.x = 100
    player.rect.y = height - 130
    player.pos_x = float(player.rect.x)
    player.pos_y = float(player.rect.y)
    lava_group.empty()
    exit_group.empty()
    coin_group.empty()
    if debug_mode:
        print(f"C: {coins}, LC: {level_coins}")
    level_coins = 0
    with open(f'Levels/level{level_num}.json', 'r') as file:
        world_data = json.load(file)
    world = World(world_data)
    return world

def draw_text(text, color, size, x, y):
    font = pygame.font.Font("Fonts/PixelFont.ttf", size)
    img = font.render(text, True, color)
    display.blit(img, (x, y))

class Player:
    def __init__(self):
        self.images_right = []
        self.images_left = []
        self.index = 0
        self.animation_timer = 0.0
        self.animation_interval = 10.0 / 60.0

        for num in range(1, 5):
            img_right = pygame.image.load(f'Icon/player{num}.png')
            img_right = pygame.transform.scale(img_right, (35, 60))
            img_left = pygame.transform.flip(img_right, True, False)
            self.images_right.append(img_right)
            self.images_left.append(img_left)

        self.image = self.images_right[self.index]
        self.rect = self.image.get_rect()
        self.rect.x = 100
        self.rect.y = height - 40 - 60

        self.pos_x = float(self.rect.x)
        self.pos_y = float(self.rect.y)

        self.gravity = 0.0
        self.jump_velocity = -1050.0
        self.gravity_acceleration = 4100.0
        self.max_fall_speed = 10000.0

        self.jumped = False
        self.direction = 0
        self.width = self.image.get_width()
        self.height = self.image.get_height()

    def update(self, dt):
        global game_over

        x = 0.0
        y = 0.0
        walk_speed = 300.0

        if game_over == 0:
            key = pygame.key.get_pressed()

            if (key[pygame.K_SPACE] or key[pygame.K_UP]) and self.jumped == False:
                jump_music.play()
                self.gravity = self.jump_velocity
                self.jumped = True

            moving = False

            if key[pygame.K_LEFT]:
                x -= walk_speed * dt
                self.direction = -1
                moving = True

            if key[pygame.K_RIGHT]:
                x += walk_speed * dt
                self.direction = 1
                moving = True

            if moving:
                self.animation_timer += dt

                while self.animation_timer >= self.animation_interval:
                    self.animation_timer -= self.animation_interval
                    self.index += 1

                    if self.index >= len(self.images_right):
                        self.index = 0

                    if self.direction == 1:
                        self.image = self.images_right[self.index]
                    else:
                        self.image = self.images_left[self.index]
            else:
                self.animation_timer = 0.0
                self.index = 0

                if self.direction == 1:
                    self.image = self.images_right[self.index]
                elif self.direction == -1:
                    self.image = self.images_left[self.index]

            self.gravity += self.gravity_acceleration * dt

            if self.gravity > self.max_fall_speed:
                self.gravity = self.max_fall_speed

            y = self.gravity * dt

            # Горизонтальное столкновение
            new_x = self.pos_x + x
            test_rect = self.rect.copy()
            test_rect.x = round(new_x)

            for tile in world.tile_list:
                if tile[1].colliderect(test_rect):
                    if x > 0:
                        new_x = tile[1].left - self.width
                    elif x < 0:
                        new_x = tile[1].right
                    x = 0.0
                    break

            self.pos_x = new_x
            self.rect.x = round(self.pos_x)

            # Вертикальное столкновение
            new_y = self.pos_y + y
            test_rect = self.rect.copy()
            test_rect.y = round(new_y)

            for tile in world.tile_list:
                if tile[1].colliderect(test_rect):
                    if self.gravity < 0:
                        new_y = tile[1].bottom
                        self.gravity = 0
                    elif self.gravity >= 0:
                        new_y = tile[1].top - self.height
                        self.gravity = 0
                        self.jumped = False

                    break

            self.pos_y = new_y
            self.rect.y = round(self.pos_y)

            if self.rect.bottom > height:
                self.rect.bottom = height
                self.pos_y = float(self.rect.y)
                self.gravity = 0
                self.jumped = False

            lava_indicator = pygame.sprite.spritecollide(self, lava_group, False)

            if lava_indicator:
                death_music.play()
                game_over = -1

            if pygame.sprite.spritecollide(self, exit_group, False):
                game_over = 1

        display.blit(self.image, self.rect)

class World:
    def __init__(self, data):
        self.tile_list = []
        dirt_img = pygame.image.load('Icon/tile4.png')
        grass_img = pygame.image.load('Icon/grass.png')
        row_count = 0

        for row in data:
            col_count = 0

            for tile in row:
                if tile == 1 or tile == 2:
                    images = {
                        1: dirt_img,
                        2: grass_img
                    }

                    img = pygame.transform.scale(images[tile], (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)

                elif tile == 3:
                    lava = Lava(
                        col_count * tile_size,
                        row_count * tile_size + (tile_size // 2)
                    )
                    lava_group.add(lava)

                elif tile == 5:
                    exit = Exit(
                        col_count * tile_size,
                        row_count * tile_size - (tile_size // 2)
                    )
                    exit_group.add(exit)

                elif tile == 6:
                    coin = Coin(
                        col_count * tile_size + (tile_size // 2),
                        row_count * tile_size + (tile_size // 2)
                    )
                    coin_group.add(coin)

                col_count += 1

            row_count += 1

    def draw(self):
        for tile in self.tile_list:
            display.blit(tile[0], tile[1])

class Lava(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        img = pygame.image.load('Icon/lava.png')
        self.image = pygame.transform.scale(img, (tile_size, tile_size // 2))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Button:
    def __init__(self, x, y, image, size=None):
        img = pygame.image.load(image)

        if size:
            scale_factor = size[0] / img.get_width()
            self.image = pygame.transform.scale_by(img, scale_factor)
        else:
            self.image = img

        self.rect = self.image.get_rect(center=(x, y))

    def draw(self):
        action = False

        if self.rect.collidepoint(pygame.mouse.get_pos()):
            if pygame.mouse.get_pressed()[0] == 1:
                action = True

        display.blit(self.image, self.rect)
        return action

class Exit(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        img = pygame.image.load('Icon/door1.png')
        self.image = pygame.transform.scale(img, (tile_size, int(tile_size * 1.5)))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Coin(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        img = pygame.image.load('Icon/coin.png')
        self.image = pygame.transform.scale(img, (tile_size // 2, tile_size // 2))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

lava_group = pygame.sprite.Group()
exit_group = pygame.sprite.Group()
coin_group = pygame.sprite.Group()

world = World(world_data)
player = Player()

restart_button = Button(width // 2, height // 2, "Icon/restart_btn.png", (300, 105))
start_button = Button(width // 2 - 150, height // 2, "Icon/start_btn.png")
exit_button = Button(width // 2 + 150, height // 2, "Icon/exit_btn.png")
final_exit_button = Button(350, 650, "Icon/exit_btn.png")

run = True
main_menu = True
bg_music.play(-1)

while run:
    dt = clock.tick() / 1000.0

    if dt > 0.05:
        dt = 0.05

    display.blit(bg_image, bg_rect)

    if main_menu:
        if start_button.draw():
            main_menu = False
            level_num = 1
            hp = def_hp
            coins = 0
            world = reset_level()

        if exit_button.draw():
            run = False

    else:
        world.draw()
        lava_group.draw(display)
        lava_group.update()
        exit_group.draw(display)
        coin_group.draw(display)

        draw_text(f"Coins:{str(coins + level_coins)}", (255, 255, 0), 30, 5, 3)
        draw_text(f"HP:{str(hp)}", (255, 0, 0), 30, 600, 3)

        player.update(dt)

        if pygame.sprite.spritecollide(player, coin_group, True):
            if debug_mode:
                print(f"C: {coins}, LC: {level_coins}")

            level_coins += 1
            coin_music.play()

        if game_over == -1:
            if restart_button.draw():
                hp = hp - 1

                if debug_mode:
                    print(hp)

                if hp == 0:
                    main_menu = True
                    time.sleep(0.1)
                else:
                    player = Player()
                    world = reset_level()

                game_over = 0

        if game_over == 1:
            game_over = 0
            coins += level_coins

            if debug_mode:
                print(f"C: {str(coins)}")

            if level_num < max_level:
                level_num += 1
                world = reset_level()
            else:
                img = pygame.image.load("Icon/win.jpg")
                image = pygame.transform.scale(img, (700, 700))
                rect = image.get_rect()
                display.blit(image, rect)

                if final_exit_button.draw():
                    run = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()

pygame.quit()
