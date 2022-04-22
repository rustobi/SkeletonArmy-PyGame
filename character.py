import math
import pygame
import os

width, height = 1080, 608
boden = 20 - 5
pygame.mixer.init()
FPS = 144

axe_sound = pygame.mixer.Sound(
    os.path.join("Assets", "character_new", "sounds", "hit", "0.wav"))

hitted_sound = pygame.mixer.Sound(
    os.path.join("Assets", "character_new", "sounds", "hitted", "hitted.mp3"))

walk_sound = pygame.mixer.Sound(os.path.join("Assets", "character_new", "sounds", "walk", "step.wav"))

hitted_sound.set_volume(0.5)
walk_sound.set_volume(0.3)


class main_character:
    def __init__(self, name, window, objects_ingame, clock,
                 characters_width=188, characters_height=100, power=10,
                 characters_mass=1, speed=1,
                 rand_links=None, rand_rechts=None):

        self.clock = clock  # Initialisiert die Clock aus der Main Datei
        self.objects_ingame = objects_ingame  # Initialisiert die Objekte der Map
        self.stopping = False  # Initialisiert den Status des Characters, auf Stoppen bezogen
        self.name = name  # NAME DES CHARACTERS
        self.characters_width, self.characters_height = characters_width, characters_height  # GRÖßE DES CHARACTERS
        self.character_mass = characters_mass  # Initialisiert die Masse des Characters
        self.velocity_max = 8  # Initialisiert die maximale Velocity beim Springen
        self.velocity = self.velocity_max  # Initialisiert die aktuelle Velocity beim Springen
        self.walking_block = False  # Initialisiert, ob der Character aktuell einen Lauf Block hat
        self.power = power  # Initialisiert die Kraft des Characters
        self.window = window  # Initialisiert das Fenster der Main Datei

        self.rand_links = rand_links  # Initialisiert den linken Rand
        self.rand_rechts = rand_rechts  # Initialisiert den renken Rand

        self.abklingbar_size_x, self.abklingbar_size_y = 100, 20  # Initialisiert X und Y Größen der Abklingbar
        self.healthbar_size_x, self.healthbar_size_y = 100, 20  # Initialisiert X und Y Größen der Healthbar

        self.max_abklingzeit = 200  # Initialisiert die maximale Abklingzeit
        self.abklingzeit = 0  # Initialisiert die Abklingzeit
        self.abkling_bar_image = pygame.image.load(os.path.join("Assets", "GAME", "gui", "abklingbar", "abklingb.png")) # Initialisiert das Abklingbar Image
        self.abkling_bar = pygame.transform.scale(self.abkling_bar_image,
                                                       (self.abklingbar_size_x, self.abklingbar_size_y))    # Transformiert das Abklingbar Image
        self.abkling_animation_time = 1  # Initialisiert die Abklingbaranimationszeit
        self.abklingzeit_bar_rect = pygame.Rect(0, 0, 100, height)  # Initialisiert das Abklingbaranimations Rectangle

        self.health = 100  # Aktuelles Leben festgelegt
        self.max_health = self.health  # Max Leben festgelegt
        self.health_bar_image = pygame.image.load(
            os.path.join("Assets", "GAME", "gui", "healthbar", "hb.png"))  # Erstellt das Lebensbarbild
        self.health_bar = pygame.transform.scale(self.health_bar_image, (
        self.healthbar_size_x, self.healthbar_size_y))  # Transformiert das Lebensbarbild
        self.health_animations_bar_rect = pygame.Rect(0, 0, 100,
                                                      self.health_bar.get_height())  # Erstellt den "Animations-timer" Rectangle
        self.health_animations_bar_rect_time = 0  # Setzt den "Animations-timer" der "Healthbar" runter

        self.animations_status = ["idle", "r"]  # Aktuelle Animation festgelegt
        self.jump_timer = 0  # jump_timer um die Sprunggeschwindigkeit zu regulieren
        self.speed = speed  # Allgemeine Geschwindigkeit des Characters festgelegt
        self.move_velocity = 0  # Bewegungsgeschwindigkeit festgelegt
        self.max_speed = 2  # Max Geschwindigkeit festgelegt
        self.animation_times = 1  # Schnelligkeit der Animation
        self.animation_time = 1  # Aktueller Animationsbilderstand

        self.character_image = pygame.image.load(
            os.path.join("Assets", "character_new", "idle", "1.png"))  # Legt das aktuelle Bild des Characters fest
        self.character = pygame.transform.scale(self.character_image, (
        self.characters_width, self.characters_height))  # Transformiert das Bild des Characters auf feste Größen
        self.position = pygame.Rect(100, height - self.characters_height - boden, self.characters_width,
                                    self.characters_height)  # Erstellt ein Rectangle um die Position des Characters zu steuern

        self.character_rect = pygame.Rect(self.position.x + 62, self.position.y, 75,
                                          self.characters_height)  # Erstellt ein Rect aus der Angriffsfläche des Characters
        self.attack_character_rect = pygame.Rect(self.position.x + 105, self.position.y, 80,
                                                 self.characters_height)  # Erstellt ein Rect aus der Fläche, die bei einem Angriff beachtet werden soll

        self.jumping = False  # Setzt den Jump-status auf False
        self.animation_dict = {"idle": 11, "walk": 13, "jump": 8,
                               "hit": 18}  # Erstellt ein Dictionary aus allen Animationen
        self.pixel_of_image = None

        self.movement = 0

    def set_walking_block(self, block):
        self.walking_block = block

    def get_walking_block(self):
        return self.walking_block

    def hit(self):
        if self.abklingzeit == 0:
            if self.get_animation()[1] == "l":
                self.set_animation(["hit", "l"])
            else:
                self.set_animation(["hit", "r"])
            self.abklingzeit = 1
            self.set_walking_block(True)
            self.move_velocity = 0
            self.max_speed = 2

    def abkling_animation(self):
        self.abklingzeit_bar_rect = pygame.Rect(
            self.window.get_width() - self.abkling_bar.get_width() - 15, 50,
            (self.max_abklingzeit - self.abklingzeit) * (self.abklingbar_size_x / self.max_abklingzeit),
            self.abkling_bar.get_height())
        pygame.draw.rect(self.window, (255, 250, 0), self.abklingzeit_bar_rect)

        if self.abkling_animation_time > 5:
            self.abkling_bar_image = pygame.image.load(
                os.path.join("Assets", "GAME", "gui", "abklingbar", "abklingb.png"))
        else:
            self.abkling_bar_image = pygame.image.load(
                os.path.join("Assets", "GAME", "gui", "abklingbar", str(int(
                    self.abkling_animation_time)) + ".png"))

        self.abkling_bar = pygame.transform.scale(self.abkling_bar_image,
                                                       (self.abklingbar_size_x, self.abklingbar_size_y))
        self.window.blit(self.abkling_bar,
                         (self.window.get_width() - self.abkling_bar.get_width() - 15, 50))

        self.abkling_animation_time += 0.05
        if self.abkling_animation_time >= 25:
            self.abkling_animation_time = 1

    def health_animation(self):
        if self.health_animations_bar_rect_time != self.health:
            if self.health_animations_bar_rect_time > self.health:
                self.health_animations_bar_rect_time -= 1
            else:
                self.health_animations_bar_rect_time += 1

        self.health_animations_bar_rect = pygame.Rect(self.window.get_width() - self.health_bar.get_width() - 15, 20,
                                                      self.health_animations_bar_rect_time * (
                                                              self.healthbar_size_x / self.max_health),
                                                      self.health_bar.get_height())
        pygame.draw.rect(self.window, (255, 0, 0), self.health_animations_bar_rect)

        self.window.blit(self.health_bar, (self.window.get_width() - self.health_bar.get_width() - 15, 20))

    def character_animation(self):
        global axe_sound, walk_sound

        if self.move_velocity > 6 and not 0.17414966225624084 == walk_sound.get_length():
            walk_sound = pygame.mixer.Sound(os.path.join("Assets", "character_new", "sounds", "walk", "step_fast.mp3"))
            walk_sound.set_volume(0.3)
        elif self.move_velocity < 6 and 0.17414966225624084 == walk_sound.get_length():
            walk_sound = pygame.mixer.Sound(os.path.join("Assets", "character_new", "sounds", "walk", "step.wav"))
            walk_sound.set_volume(0.3)

        if self.get_animation()[0] == "hit" and self.animation_dict.get(self.get_animation()[0]) // 2 == int(
                self.animation_time):
            if not axe_sound.get_num_channels():
                axe_sound.play()

        # Automatisches regenerieren von Leben
        if self.health < self.max_health:
            self.health += 0.01

        if not self.health < self.max_health:
            self.health = self.max_health

        if self.animation_times != 0.5:
            self.health_animation()
            self.abkling_animation()

        if self.animation_dict.get(self.get_animation()[0]) == int(self.animation_time):
            if self.get_animation()[0] == "hit":
                if self.get_animation()[1] == "l":
                    self.set_animation(["idle", "l"])
                if self.get_animation()[1] == "r":
                    self.set_animation(["idle", "r"])
                self.set_walking_block(False)
            self.animation_time = 1

        self.initilise_character(
            os.path.join("Assets", "character_new", self.get_animation()[0], str(int(self.animation_time)) + ".png"),
            self.get_animation()[1])
        self.animation_time += 0.2 * self.animation_times

    def sound_design(self):
        global walk_sound
        if self.get_animation()[0] == "idle":
            walk_sound.stop()
        elif self.get_animation()[0] == "walk" and not walk_sound.get_num_channels():
            walk_sound.play()

    def update_character(self):
        self.sound_design()
        if self.stopping:
            self.stop_character()
        if self.abklingzeit >= 1:
            self.abklingzeit += 1
        if self.abklingzeit >= self.max_abklingzeit:
            self.abkling_animation_time = 1
            self.abklingzeit = 0
        if self.get_is_jumping():
            try:
                if self.jump_timer % self.speed == 0:
                    self.jump()
            except Exception as e:
                self.jump()
                print(e)
            self.jump_timer += 1
        else:
            for objekt_key, objekt_value in self.objects_ingame.items():
                new_foot_rect = pygame.Rect(self.get_character_rect().x, self.get_character_rect().y + 85,
                                            self.get_character_rect().width, 15)
                if new_foot_rect.colliderect(objekt_value):
                    self.position.y = objekt_value.y - self.get_height() + 5
        self.position = pygame.Rect(self.position.x, self.position.y, self.characters_width, self.characters_height)
        self.character_animation()

    def set_attack_character_rect(self):
        if self.get_animation()[1] == "r":
            self.attack_character_rect = pygame.Rect(self.position.x + 105, self.position.y, 80, self.characters_height)
        elif self.get_animation()[1] == "l":
            self.attack_character_rect = pygame.Rect(self.position.x, self.position.y, 80, self.characters_height)

    def set_character_rect(self):
        if self.get_animation()[1] == "r":
            self.character_rect = pygame.Rect(self.position.x + 63, self.position.y, 45, self.characters_height)
        elif self.get_animation()[1] == "l":
            self.character_rect = pygame.Rect(self.position.x + 80, self.position.y, 45, self.characters_height)

    def initilise_character(self, path, direction):
        self.set_character_rect()
        self.set_attack_character_rect()
        if direction == "r":
            self.character_image = pygame.image.load(path)
            self.character = pygame.transform.scale(self.character_image,
                                                    (self.characters_width, self.characters_height))
        elif direction == "l":
            self.character_image = pygame.image.load(path)
            self.character = pygame.transform.flip(pygame.transform.scale(self.character_image,
                                                                          (self.characters_width,
                                                                           self.characters_height)), True, False)
        """ Erstellung einer Pixelgenauen Kopie des Characters in Rects
        meine_zwecke = pygame.Surface.copy(self.character)
        self.pixel_of_image = pygame.PixelArray(meine_zwecke)
        self.pixel_of_image.transpose()
        """

    def get_pixel_of_image(self):
        return self.pixel_of_image

    def set_animation(self, animation):
        if int(self.animation_time) != 1 and animation != self.animations_status:
            self.animation_time = 1
        self.animations_status = animation

    def set_speed(self, speed):
        self.speed = speed

    def move_character(self, direction):
        self.movement = 0
        if direction == "right" and self.get_is_jumping():
            if self.velocity > 0:
                self.movement = math.ceil((self.move_velocity * 144) / self.clock.get_fps()) + 5
            else:
                self.movement = math.ceil((self.move_velocity * 144) / self.clock.get_fps())
            self.position.x += self.movement
            if self.get_animation() != ["jump", "r"]:
                self.set_animation(["jump", "r"])
            if self.move_velocity < self.max_speed:
                self.move_velocity += 0.05
            else:
                self.move_velocity -= 0.05

        elif direction == "right" and not self.get_is_jumping():
            if self.get_animation() != ["walk", "r"]:
                self.set_animation(["walk", "r"])
                self.move_velocity = 0
            self.movement = math.ceil((self.move_velocity * 144) / self.clock.get_fps())
            self.position.x += self.movement
            if self.move_velocity < self.max_speed:
                self.move_velocity += 0.05
            else:
                self.move_velocity -= 0.05

        if direction == "left" and self.get_is_jumping():
            if self.velocity > 0:
                self.movement = math.ceil((self.move_velocity * 144) / self.clock.get_fps()) + 5
            else:
                self.movement = math.ceil((self.move_velocity * 144) / self.clock.get_fps())
            self.position.x -= self.movement
            if self.get_animation() != ["jump", "l"]:
                self.set_animation(["jump", "l"])
            if self.move_velocity < self.max_speed:
                self.move_velocity += 0.05
            else:
                self.move_velocity -= 0.05

        elif direction == "left" and not self.get_is_jumping():
            if self.get_animation() != ["walk", "l"]:
                self.set_animation(["walk", "l"])
                self.move_velocity = 0
            self.movement = math.ceil((self.move_velocity * 144) / self.clock.get_fps())
            self.position.x -= self.movement
            if self.move_velocity < self.max_speed:
                self.move_velocity += 0.05
            else:
                self.move_velocity -= 0.05

        return self.movement

    def move_character_regular(self, x, y):
        self.position.x += x
        self.position.y += y

    def stop_character(self):
        self.stopping = True
        if self.get_animation()[1] == "r":
            if self.move_velocity <= 0.2:
                self.move_velocity = 0
                self.stopping = False
            else:
                if self.position.colliderect(self.rand_rechts):
                    self.move_velocity = 0
                else:
                    self.position.x += math.ceil((math.floor(self.move_velocity)) * 144 // self.clock.get_fps())
                    self.move_velocity -= 0.2
        if self.get_animation()[1] == "l":
            if self.move_velocity <= 0.2:
                self.move_velocity = 0
                self.stopping = False
            else:
                if self.position.colliderect(self.rand_links):
                    self.move_velocity = 0
                else:
                    self.position.x -= math.ceil((math.floor(self.move_velocity)) * 144 // self.clock.get_fps())
                    self.move_velocity -= 0.2

    def jump(self):
        if self.get_animation()[0] != "jump":
            if self.get_animation()[1] == "r":
                self.set_animation(["jump", "r"])
            elif self.get_animation()[1] == "l":
                self.set_animation(["jump", "l"])
            self.jump_timer = 0

        if self.velocity > 0:
            F = (0.5 * self.character_mass * (self.velocity * self.velocity))
        else:
            F = -(0.5 * self.character_mass * (self.velocity * self.velocity))

        # Change position
        self.position.y -= F
        self.character_rect.y -= F

        # Change velocity
        if self.velocity > -8:
            self.velocity -= 1

        new_foot_rect = pygame.Rect(self.get_character_rect().x, self.get_character_rect().y + 85, self.get_character_rect().width, 15)


        # If ground is reached, reset variables.
        for objekt_key, objekt_value in self.objects_ingame.items():
            if objekt_key[:5] == "boden" and self.velocity < 0:
                if new_foot_rect.colliderect(objekt_value):
                    self.position.y = objekt_value.y - self.get_height() + 5
                    self.set_is_jumping(False)
                    self.set_walking_block(False)
                    self.velocity = self.velocity_max
                    if self.get_animation()[1] == "r":
                        self.set_animation(["idle", "r"])
                    elif self.get_animation()[1] == "l":
                        self.set_animation(["idle", "l"])

    def damage_got(self, damage_got):
        self.health -= damage_got
        hitted_sound.play()

    def get_is_jumping(self):
        return self.jumping

    def get_character(self):
        return self.character

    def get_character_rect(self):
        return self.character_rect

    def get_attack_character_rect(self):
        return self.attack_character_rect

    def set_is_jumping(self, jumping):
        try:
            self.jumping = jumping
        except Exception as e:
            print(e)

    def get_position(self):
        return self.position

    def get_animation(self):
        return self.animations_status

    def get_width(self):
        return self.characters_width

    def get_height(self):
        return self.characters_height

    def get_power(self):
        return self.power

    def set_power(self, power):
        self.power = power
