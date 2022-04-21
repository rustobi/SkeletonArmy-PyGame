import os
from random import randint
import pygame

width, height = 1080, 608
lava_width, lava_height = width / 10 + 5, 20
boden = lava_height - 5
hitted = False

pygame.mixer.init()
pygame.mixer.pre_init()

hit_sound = pygame.mixer.Sound(os.path.join("Assets", "enemy_new", "sounds", "hitted", "1.wav"))


class enemy:
    def __init__(self, name, window, enemy_width=208, enemy_height=90, enemy_mass=1, speed=1, position=None,
                 health=50,
                 walk_status="LEFT", asset_color="enemy_new", strength=30):
        self.name = name  # NAME DES CHARACTERS
        self.enemy_width, self.enemy_height = enemy_width, enemy_height  # GRÖßE DES CHARACTERS
        self.enemy_mass = enemy_mass
        self.velocity_standard = 8
        self.velocity = self.velocity_standard

        self.asset_color = asset_color

        self.way_to_right = randint(100, 150)
        self.way_to_left = self.way_to_right

        self.live_image = pygame.image.load(os.path.join("Assets", self.asset_color, "LIVE", "0.png"))
        self.enemy_live = pygame.transform.scale(self.live_image, (40, 10))

        self.walked_way_left = 0
        self.walked_way_right = 0

        self.walk_status = walk_status

        self.animation = ["idle", "l"]
        self.framerate_animation = 0
        self.timer = 0
        self.speed = speed
        self.max_health = health
        self.health = health
        self.animation_time = 1
        self.window = window
        self.strength = strength

        self.health_animation_time = 0
        self.enemy_live_rect = pygame.Rect(0, 0, self.health_animation_time, 10)

        self.animation_list = {"idle": 4, "die": 13, "hitted": 3, "walk": 10, "hit": 14}

        if position is None:
            position = [width - self.enemy_width - 10, height - self.enemy_height - boden]

        self.enemy_image = pygame.image.load(os.path.join("Assets", "enemy_new", "idle", "1.png"))
        self.enemy = pygame.transform.scale(self.enemy_image, (self.enemy_width, self.enemy_height))
        self.position = pygame.Rect(position[0], position[1], self.enemy_width, self.enemy_height)

        self.enemy_rect = pygame.Rect(self.position.x + 59, self.position.y, 90, self.enemy_height)
        self.attack_enemy_rect = pygame.Rect(self.position.x, self.position.y, 88, self.enemy_height)

    def damage(self, damage):
        self.animation_time = 1
        self.set_animation(["hitted", self.get_animation()[1]])
        self.health -= damage
        hit_sound.play()

    def health_animation(self, x, y):
        if self.health_animation_time != self.health:
            if self.health_animation_time > self.health:
                self.health_animation_time -= 1
            else:
                self.health_animation_time += 1

        self.enemy_live_rect = pygame.Rect(x, y, (40 / self.max_health) * self.health_animation_time, 10)

        pygame.draw.rect(self.window, (255, 0, 0), self.enemy_live_rect)

    def enemy_animation(self, character):
        global hitted
        # X and Y Coordination's of ENEMY LIVE
        x = self.get_position().x + self.get_width() // 2 - 20
        y = self.get_position().y - 30

        self.health_animation(x, y)

        if self.health > 0 and self.health_animation_time > 0:
            self.window.blit(self.enemy_live, (x, y))

        if self.get_animation()[0] == "die" and self.animation_list.get(self.get_animation()[0]) == int(
                self.animation_time):
            self.framerate_animation = None
            self.health = -500
            self.move_enemy(0, 10000)

        elif self.animation_list.get(self.get_animation()[0]) == int(self.animation_time):
            self.animation_time = 1
            if self.get_animation()[0] == "hitted":
                hitted = False
                self.set_animation(["idle", self.get_animation()[1]])

        self.initilise_again(
            os.path.join("Assets", self.asset_color, self.get_animation()[0], str(int(self.animation_time)) + ".png"),
            self.get_animation()[1])

        if self.get_animation()[0] == "hitted":
            self.animation_time += 0.03

        if not self.get_animation()[0] == "walk":
            self.animation_time += 0.1 * (self.animation_list.get(self.get_animation()[0]) / 12)
        else:
            self.animation_time += 0.1 * (self.animation_list.get(self.get_animation()[0]) / 12) * self.speed

        # Greift den Character an, wenn IDLE einmal durchlaufen ist.
        if self.get_animation()[0] == "idle":
            if self.animation_list.get(self.get_animation()[0]) // 2 == int(self.animation_time):
                self.animation_time = 1
                self.set_animation(["hit", self.get_animation()[1]])
                hitted = False

        if self.get_animation()[0] == "hit":
            if self.animation_list.get(self.get_animation()[0]) // 2 == int(self.animation_time) and not hitted:
                if self.attack_enemy_rect.colliderect(character.get_character_rect()):
                    character.damage_got(self.strength)
                    hitted = True

            if self.animation_list.get(self.get_animation()[0]) == int(self.animation_time):
                self.animation_time = 1
                self.set_animation(["idle", self.get_animation()[1]])
                hitted = False

    def update_character(self, character):
        if self.framerate_animation is not None:
            self.enemy_animation(character)
            self.move(character)
        if self.health < 1 and not self.get_animation()[0] == "die":
            self.set_animation(["die", self.get_animation()[1]])

    def move_char(self, x=0, y=0):
        self.get_position().x += x
        self.get_position().x += y

    def move(self, character):
        if self.attack_enemy_rect.colliderect(character.get_position()):
            if self.get_animation()[0] == "walk":
                self.set_animation(["idle", self.get_animation()[1]])
        else:
            if self.get_animation()[0] != "hit" and self.get_animation()[0] != "die":
                self.set_animation(["walk", self.get_animation()[1]])
                if self.walked_way_left > self.way_to_left:
                    self.walked_way_left = 0
                    self.set_animation(["walk", "r"])

                if self.walked_way_right > self.way_to_right:
                    self.walked_way_right = 0
                    self.set_animation(["walk", "l"])

                if self.get_animation()[1] == "r":
                    self.walked_way_right += 1
                    self.position.x += 1 * self.speed

                if self.get_animation()[1] == "l":
                    self.walked_way_left += 1
                    self.position.x -= 1 * self.speed

    def set_attack_enemy_rect(self):
        if self.get_animation()[1] == "r":
            self.attack_enemy_rect = pygame.Rect(self.position.x + 140, self.position.y, 65, self.enemy_height)
        elif self.get_animation()[1] == "l":
            self.attack_enemy_rect = pygame.Rect(self.position.x + 10, self.position.y, 65, self.enemy_height)

    def set_enemy_rect(self):
        self.enemy_rect = pygame.Rect(self.position.x + 59, self.position.y, 90, self.enemy_height)

    def initilise_again(self, path, direction):
        self.set_attack_enemy_rect()
        self.set_enemy_rect()

        if direction == "r":
            self.enemy_image = pygame.image.load(path)
            self.enemy = pygame.transform.scale(self.enemy_image,
                                                (self.enemy_width, self.enemy_height))
        elif direction == "l":
            self.enemy_image = pygame.image.load(path)
            self.enemy = pygame.transform.flip(pygame.transform.scale(self.enemy_image,
                                                                      (self.enemy_width, self.enemy_height)), True,
                                               False)

    def get_attack_enemy_rect(self):
        return self.attack_enemy_rect

    def get_enemy_rect(self):
        return self.enemy_rect

    def set_animation(self, animation):
        if int(self.animation_time) != 1 and animation != self.animation:
            self.animation_time = 1
        self.animation = animation

    def set_speed(self, speed):
        self.speed = speed

    def move_enemy(self, x, y):
        self.position.x += x
        self.position.y += y

    def set_walk_status(self, status):
        self.walk_status = status

    def get_walk_status(self):
        return self.walk_status

    def get_enemy(self):
        return self.enemy

    def get_position(self):
        return self.position

    def get_animation(self):
        return self.animation

    def get_width(self):
        return self.enemy_width

    def get_height(self):
        return self.enemy_height
