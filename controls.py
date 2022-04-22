import math
from character import main_character
import pygame

fps = 144
width, height = 1080, 608
lava_width, lava_height = width / 10 + 5, 20
boden = lava_height - 5
pygame.init()

class controls():
    def __init__(self, rand_links, rand_rechts, character_active, clock, objects_ingame):
        self.character_active = character_active
        self.rand_links = rand_links
        self.rand_rechts = rand_rechts
        self.clock = clock
        self.objects_ingame = objects_ingame

    def left(self, aktueller_offset, shift_clicked):
        left_offset = 0
        rand_beruehrung = self.character_active.get_character_rect().colliderect(self.rand_links)
        if not rand_beruehrung:
            self.character_active.move_character("left")
        if rand_beruehrung and not aktueller_offset < 100:
            if not self.character_active.get_is_jumping():
                left_offset -= self.character_active.move_character("left")
            elif self.character_active.get_is_jumping():
                left_offset -= self.character_active.move_character("left")
        count = 0
        for key,value in self.objects_ingame.items():
            if self.character_active.get_character_rect().colliderect(value):
                count += 1
        if count < 1 and not self.character_active.get_is_jumping():
            self.character_active.velocity = 0
            self.character_active.set_is_jumping(True)

        return left_offset

    def right(self, aktueller_offset, shift_clicked):
        right_offset = 0
        rand_beruehrung = self.character_active.get_character_rect().colliderect(self.rand_rechts)
        if not rand_beruehrung:
            self.character_active.move_character("right")
        if rand_beruehrung and not aktueller_offset >= 3500:
            if not self.character_active.get_is_jumping() :
                right_offset = self.character_active.move_character("right")
            if self.character_active.get_is_jumping():
                right_offset = self.character_active.move_character("right")

        count = 0
        for key, value in self.objects_ingame.items():
            if self.character_active.get_character_rect().colliderect(value):
                count += 1
        if count < 1 and not self.character_active.get_is_jumping():
            self.character_active.velocity = 0
            self.character_active.set_is_jumping(True)
        return right_offset

    def up(self, shift_clicked):
        if not self.character_active.get_is_jumping():
            self.character_active.jump()
            self.character_active.set_is_jumping(True)

    def down(self, shift_clicked):
        pass
