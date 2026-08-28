import pygame
import json
pygame.init()

width = 700
height = 700

tile_size = 35

clock = pygame.time.Clock()
fps = 60

game_over = 0

display = pygame.display.set_mode((width, height))
pygame.display.set_caption('Platformer')

bg_image = pygame.image.load('Icon/bg11.png')
bg_rect = bg_image.get_rect()

with open('Levels/level1.json', 'r') as file:
    world_data = json.load(file)

level_num = 1
max_level = 4

def reset_level():
    player.rect.x = 100
    player.rect.y = height - 130
    lava_group.empty()
    exit_group.empty()
    with open(f'Levels/level{level_num}.json', 'r') as file:
        world_data = json.load(file)
    world = World(world_data)
    return world

class Player:
    def __init__(self):
        self.images_right = []
        self.images_left = []
        self.index = 0
        self.counter = 0
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
        self.gravity = 0
        self.jumped = False
        self.direction = 0
        self.width = self.image.get_width()
        self.height = self.image.get_height()

    def update(self):
        global game_over
        x = 0
        y = 0
        walk_speed = 10 # раз в 10 повторений будет анимация

        if game_over == 0:
            key = pygame.key.get_pressed()
            if (key[pygame.K_SPACE] or key[pygame.K_UP]) and self.jumped == False:
                self.gravity = -15
                self.jumped = True

            if key[pygame.K_LEFT]:
                x -= 5
                self.direction = -1
                self.counter += 1
            if key[pygame.K_RIGHT]:
                x += 5
                self.direction = 1
                self.counter += 1

            if self.counter > walk_speed:
                self.counter = 0
                self.index += 1
                if self.index >= len(self.images_right):
                    self.index = 0
                if self.direction == 1:
                    self.image = self.images_right[self.index]
                else:
                    self.image = self.images_left[self.index]

            # add gravity
            self.gravity += 1.0
            if self.gravity > 10:
                self.gravity = 10
            y += self.gravity


            for tile in world.tile_list:
                if tile[1].colliderect(self.rect.x + x, self.rect.y, self.width, self.height):
                    x = 0
                if tile[1].colliderect(self.rect.x, self.rect.y + y, self.width, self.height):
                    if self.gravity < 0:
                        y = tile[1].bottom - self.rect.top
                        self.gravity = 0
                    elif self.gravity >= 0:
                        y = tile[1].top - self.rect.bottom
                        self.gravity = 0
                        self.jumped = False

            # update player coordinates
            self.rect.x += x
            self.rect.y += y

            if self.rect.bottom > height:
                self.rect.bottom = height

            if pygame.sprite.spritecollide(self, lava_group, False):
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
                    lava = Lava(col_count * tile_size, row_count * tile_size + (tile_size // 2))
                    lava_group.add(lava)
                elif tile == 5:
                    exit = Exit(col_count * tile_size, row_count * tile_size - (tile_size // 2))
                    exit_group.add(exit)
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
        self.image = pygame.transform.scale(img, (tile_size, int(tile_size*1.5)))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
lava_group = pygame.sprite.Group()
exit_group = pygame.sprite.Group()

world = World(world_data)
player = Player()
restart_button = Button(width // 2, height // 2, "Icon/restart_btn.png", (300, 105))
start_button = Button(width // 2 - 150, height // 2, "Icon/start_btn.png")
exit_button = Button(width // 2 + 150, height // 2, "Icon/exit_btn.png")
final_exit_button = Button(350, 650, "Icon/exit_btn.png")

run = True
main_menu = True
while run:
    clock.tick(fps)
    display.blit(bg_image, bg_rect)
    if main_menu:
        if start_button.draw():
            main_menu = False
            level_num = 1
            world = reset_level()
        if exit_button.draw():
            run = False
    else:
        world.draw()
        lava_group.draw(display)
        lava_group.update()
        exit_group.draw(display)
        player.update()

        if game_over == -1:
            if restart_button.draw():
                player = Player()
                world = reset_level()
                game_over = 0
        if game_over == 1:
            game_over = 0
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