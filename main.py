import os
import pygame
import random
import math
from pytmx.util_pygame import load_pygame

# IMPORTANT SETTINGS
from character import main_character
from controls import controls
from enemy import enemy

fps = 144
width, height = 1080, 608
lava_width, lava_height = width / 10 + 5, 20
boden = lava_height - 5
vel = 1
character_status = "IDLE"
is_jumping = False
anzahl = 1
framerate = 0
world_offset = [0, 0]
anzahl_enemys = 0
anzahl_enemys_counter = 5
kills_enemys = 0
insel_movement = 0

radien_insel = []
insel_liste = []
insel_movement_pace = []

# SCREENS
start_screen = True
won_game = False
game_over_screen = False
button_clicked = False
f1_clicked_enemy_view = False
f2_clicked_character_view = False

# INITIALISE PYGAME AND SET CAPTION
WIN = pygame.display.set_mode((width, height), pygame.RESIZABLE)

pygame.font.init()
pygame.display.set_caption("DEV")
tmxdata = load_pygame("")

# DECLARE COLORS
color_white = (255, 255, 255)
color_red = (255, 0, 0)
color_green = (0, 255, 0)
color_blue = (0, 0, 255)
color_black = (0, 0, 0)

pygame.mixer.init()
pygame.mixer.pre_init()

lava = None

pygame.mixer.music.load(os.path.join("Assets", "musik", "background.mp3"))
pygame.mixer.music.play(loops=-1)


def main():
    global anzahl, kills_enemys, anzahl_enemys, anzahl_enemys_counter, start_screen, won_game, game_over_screen, button_clicked, width, height, lava, f1_clicked_enemy_view, f2_clicked_character_view, insel_movement

    spiel_gestartet_mit_knopf_druck = False

    def world_move(x=0, y=0):
        for key, value in objects_ingame.items():
            if value == objects_ingame["boden"]:
                lava.x -= x
                continue

        for key, value in enemy_objects.items():
            if not value == "DEAD":
                value.move_char(-x, y)

        for key,value in objects_ingame.items():
            if key != "boden":
                value.x -= x

        neuer_x_wert = background_liste[1][0] - (x * 0.1)
        background_liste[1] = (neuer_x_wert, y)

        character.move_character_regular(-x, y)

    def circle_animation(insel, insel_nr):
        # Erstellen einer Radius Liste f??r die Schwebenden Inseln
        if not radien_insel:
            for i in range(0, len(objects_ingame) - 1):
                insel_liste.append([0,"r"])
                radien_insel.append(random.randint(1, 3))

        if insel_liste[int(insel_nr)][1] == "r" and insel_liste[int(insel_nr)][0] < radien_insel[int(insel_nr)]:
            insel_liste[int(insel_nr)][0] += 0.1
        if insel_liste[int(insel_nr)][1] == "l" and insel_liste[int(insel_nr)][0] > -radien_insel[int(insel_nr)]:
            insel_liste[int(insel_nr)][0] -= 0.1
        if insel_liste[int(insel_nr)][1] == "r" and insel_liste[int(insel_nr)][0] >= radien_insel[int(insel_nr)]:
            insel_liste[int(insel_nr)][1] = "l"
        if insel_liste[int(insel_nr)][1] == "l" and insel_liste[int(insel_nr)][0] <= -radien_insel[int(insel_nr)]:
            insel_liste[int(insel_nr)][1] = "r"

        if insel_liste[int(insel_nr)][1] == "r" and insel_liste[int(insel_nr)][0] >= 0:
            movement = math.floor(insel_liste[int(insel_nr)][0])
            if movement == 0:
                movement = 1
            insel.x += movement
            insel.y += movement

        elif insel_liste[int(insel_nr)][1] == "l" and insel_liste[int(insel_nr)][0] >= 0:
            movement = math.floor(insel_liste[int(insel_nr)][0])
            if movement == 0:
                movement = 1
            insel.x -= movement
            insel.y += movement

        elif insel_liste[int(insel_nr)][1] == "l" and insel_liste[int(insel_nr)][0] <= 0:
            movement = math.ceil(insel_liste[int(insel_nr)][0])
            if movement == 0:
                movement = -1
            insel.x += movement
            insel.y += movement

        elif insel_liste[int(insel_nr)][1] == "r" and insel_liste[int(insel_nr)][0] <= 0:
            movement = math.ceil(insel_liste[int(insel_nr)][0])
            if movement == 0:
                movement = -1
            insel.x -= movement
            insel.y += movement

        if int(insel_nr) == 1:
            print(movement)

    def draw_window():
        global insel_movement

        if not insel_movement_pace:
            for i in range (0,len(objects_ingame) - 1):
                insel_movement_pace.append(0)

        if not start_screen and not won_game and not game_over_screen:
            WIN.blit(background_liste[0], background_liste[1])
            WIN.blit(pointsbar, (20, 20))

            if world_offset[0] > 0:
                menge = math.ceil(world_offset[0] / lava_width)
                for i in range(0, menge):
                    WIN.blit(lava_end, (lava.x + (lava_width * math.ceil(width / lava_width)) + (lava_width * i), lava.y))

            for keys, values in enemy_objects.items():
                try:
                    values.update_character(character)
                    if f1_clicked_enemy_view:
                        pygame.draw.rect(WIN, (255, 0, 0), character.get_character_rect())
                        pygame.draw.rect(WIN, (0, 255, 0), values.get_attack_enemy_rect())
                        WIN.blit(enemy_view, (20, 120))
                    if f2_clicked_character_view:
                        pygame.draw.rect(WIN, (255, 0, 50), character.get_attack_character_rect())
                        pygame.draw.rect(WIN, (0, 255, 50), values.get_enemy_rect())
                        WIN.blit(character_view, (20, 150))
                    WIN.blit(values.get_enemy(), (values.get_position().x, values.get_position().y))
                except Exception as e:
                    continue

            for key, value in objects_ingame.items():
                if key == "boden":
                    for i in range(0, int(width // lava_width + 1)):
                        WIN.blit(objects_ingame_images[key], (lava.x + lava_width * i, lava.y))
                else:
                    if insel_movement_pace[int(key[6:])] >= 1:
                        circle_animation(value, key[6:])
                        insel_movement_pace[int(key[6:])] = 0
                    else:
                        insel_movement_pace[int(key[6:])] += 0.2
                    WIN.blit(objects_ingame_images[key], (value.x, value.y))

            character.update_character()
            WIN.blit(character.get_character(), (character.get_position().x, character.get_position().y))

            text_surface = my_font.render(str(kills_enemys), False, color_white)
            text_surface2 = my_font.render("Rest: " + str(anzahl_enemys_counter), False, color_white)

            """
            for pixel_liste in enumerate(character.get_pixel_of_image()):
                for pixel in enumerate(pixel_liste[1]):
                    x, y = pixel_liste[0], pixel[0]
                    if pixel[1] != 0:
                        rect = pygame.Rect(character.position.x + x, character.position.y + y, 1, 1)
                        pygame.draw.rect(WIN, color_green, rect)
            """

            text_surface3 = fps_font.render(str(int(clock.get_fps())), False, color_white)
            WIN.blit(text_surface3, (width // 2 - text_surface3.get_width(), 10))
            WIN.blit(text_surface, (70, 20))
            WIN.blit(text_surface2, (20, 70))

        elif start_screen:
            WIN.blit(background_liste[0], background_liste[1])
            character.update_character()
            char = character.character.get_rect(center=(width // 2 - 150, height // 2))
            character.animation_times = 0.5
            WIN.blit(character.get_character(), char)
            WIN.blit(spiel_starten_lbl, text_rect)
            character.set_walking_block(True)

        elif game_over_screen:
            WIN.blit(background_liste[0], background_liste[1])
            character.update_character()
            char = character.character.get_rect(center=(width // 2, character.get_position().y))
            character.animation_times = 0.5
            character.width = 100
            WIN.blit(character.get_character(), char)
            WIN.blit(spielverloren_lbl, text_gover_rect)
            WIN.blit(spielneustarten_lbl, spielneustarten_rect)
            character.set_walking_block(True)
            pygame.display.update()
        else:
            WIN.blit(background_liste[0], background_liste[1])
            WIN.blit(spielgewonnen_lbl, text_win_rect)

        pygame.display.update()

    def tastatur_druck(pressed_key, left):
        if not character.get_walking_block() and not start_screen and not won_game and not game_over_screen:
            if pressed_key[pygame.K_a] and not pressed_key[pygame.K_d]:  # Left
                bewegung = steuerung.left(world_offset[0], pressed_key[pygame.K_LSHIFT])
                world_offset[0] += bewegung
                world_move(bewegung, 0)
            elif not pressed_key[pygame.K_a]:
                if character.get_animation() == ["walk", "l"]:
                    character.stop_character()
                    if character.move_velocity < 1:
                        character.set_animation(["idle", "l"])

            if pressed_key[pygame.K_d] and not pressed_key[pygame.K_a]:  # Right
                bewegung = steuerung.right(world_offset[0], pressed_key[pygame.K_LSHIFT])
                world_offset[0] += bewegung
                world_move(bewegung, 0)
            elif not pressed_key[pygame.K_d]:
                if character.get_animation() == ["walk", "r"]:
                    character.stop_character()
                    if character.move_velocity < 1:
                        character.set_animation(["idle", "r"])

            if pressed_key[pygame.K_d] and pressed_key[pygame.K_a]:
                character.stop_character()

            if pressed_key[pygame.K_LSHIFT]:
                character.max_speed = 10
                if character.move_velocity >= 8:
                    character.animation_times = 3
                else:
                    character.animation_times = 1
            else:
                character.max_speed = 2
                character.animation_times = 1

            if left:
                if character.get_animation()[0] != "hit":
                    if not character.get_is_jumping() and not character.get_walking_block():
                        character.hit()

    def spawn_enemys():
        global anzahl_enemys, anzahl_enemys_counter
        create_enemy = [False, 0]
        values_in_game = list(enemy_objects.values())
        if len(values_in_game) == 0:
            anzahl_enemys += 1
            create_enemy = [True, 750 + width - 1080]
        if world_offset[0] > 0:
            if len(values_in_game) < math.floor((world_offset[0] + 250) / 750) + 1:
                anzahl_enemys += 1
                create_enemy = [True, width + width - 1080]

        if create_enemy[0]:
            enemys = enemy("Peter2", WIN, speed=random.randint(1, 2),
                           position=[create_enemy[1], height - 90 - boden])
            enemy_objects[f"enemy_{str(anzahl_enemys)}"] = enemys

    # R??NDER INITIALISIERUNG
    rand_links = pygame.Rect(0, 0, 100, height)
    rand_rechts = pygame.Rect(width - 100, 0, 100, height)

    my_font = pygame.font.SysFont('Comic Sans MS', 30)
    fps_font = pygame.font.SysFont('Comic Sans MS', 16)

    background_liste = []
    background_image = pygame.image.load(os.path.join("Assets", "GAME", "bg1.png"))
    background_liste.append(pygame.transform.scale(background_image, (width * 2, height)))
    background_liste.append((0, 0))

    # LAVA INITIALISIERUNG
    lava_image = pygame.image.load(os.path.join("Assets", "lava", "1.png"))
    lava_end = pygame.transform.scale(lava_image, (lava_width, lava_height))
    lava = pygame.Rect(0, height - lava_height, lava_width, lava_height)

    # Start Screen
    font_screen = pygame.font.SysFont('Comic Sans MS', 50)
    spiel_starten_lbl = font_screen.render("Spiel starten", False, color_white)
    text_rect = spiel_starten_lbl.get_rect(center=(width // 2 + 35, height // 2 + 10))

    # End Screen
    spielgewonnen_lbl = font_screen.render("Sie haben gewonnen!", False, color_white)
    text_win_rect = spielgewonnen_lbl.get_rect(center=(width / 2, height / 2))

    # Game Over Screen
    font_newstart_screen = pygame.font.SysFont('Comic Sans MS', 25)
    spielverloren_lbl = font_screen.render("Sie haben versagt!", False, color_white)
    spielneustarten_lbl = font_newstart_screen.render("Neustarten", False, color_white)
    text_gover_rect = spielverloren_lbl.get_rect(center=(width / 2, height / 2))
    spielneustarten_rect = spielneustarten_lbl.get_rect(center=(width / 2, height / 2 + 70))

    # Attack View Labels
    font_view = pygame.font.SysFont('Comic Sans MS', 20)
    character_view = font_view.render("Character view", False, color_white)
    enemy_view = font_view.render("Enemy view", False, color_white)

    pointsbar_image = pygame.image.load(os.path.join("Assets", "GAME", "POINTS", "headcount.png"))
    pointsbar = pygame.transform.scale(pointsbar_image, (50, 40))

    # Objekte im Spiel Initialisieren
    schwebende_insel_image = pygame.image.load(os.path.join("Assets", "GAME", "ground2.png"))
    schwebende_insel = pygame.transform.scale(schwebende_insel_image, (80, 20))
    schwebende_insel_rect = pygame.Rect(width - 750, height - 100, 80, 20)
    schwebende_insel_rect2 = pygame.Rect(width - 500, height - 200, 80, 20)
    schwebende_insel_rect3 = pygame.Rect(width - 250, height - 300, 80, 20)
    schwebende_insel_rect4 = pygame.Rect(width - 550, height - 400, 80, 20)

    objects_ingame_images = {"boden": lava_end,
                             "boden_0": schwebende_insel,
                             "boden_1": schwebende_insel,
                             "boden_2": schwebende_insel,
                             "boden_3": schwebende_insel}

    objects_ingame = {"boden": (pygame.Rect(0, height - lava_height, width, lava_height)),
                      "boden_0": schwebende_insel_rect,
                      "boden_1": schwebende_insel_rect2,
                      "boden_2": schwebende_insel_rect3,
                      "boden_3": schwebende_insel_rect4}

    enemy_objects = {}

    clock = pygame.time.Clock()

    # SPIELER INITIALISIERUNG
    character = main_character("Franz", WIN, objects_ingame, clock, speed=3, rand_links=rand_links,
                               rand_rechts=rand_rechts)

    # STEUERUNG INITIALISIERUNG
    steuerung = controls(rand_links, rand_rechts, character, clock, objects_ingame)

    run = True

    while run:
        def crash_detection():  # Crash Kontrolle Methode
            for keys, values in enemy_objects.items():
                try:
                    if character.get_attack_character_rect().colliderect(values.get_enemy_rect()):
                        yield [True, values, keys]
                except Exception as e:
                    continue
            yield [False, ""]

        def update_window(event_type):
            global rand_links, rand_rechts, lava_width, lava_height, lava
            background_liste[0] = pygame.transform.scale(background_image, (width * 2, height))
            lava_width = width / 10 + 5
            lava = pygame.Rect(0, height - lava_height, lava_width, lava_height)

            rand_links = pygame.Rect(0, 0, 100, height)
            rand_rechts = pygame.Rect(width - 100, 0, 100, height)

            for key, value in enemy_objects.items():
                try:
                    value.position.y = height - value.get_height() - boden
                except Exception as e:
                    print(e)

            character.rand_links = rand_links
            character.rand_rechts = rand_rechts

            steuerung.rand_links = rand_links
            steuerung.rand_rechts = rand_rechts

            character.objects_ingame["boden"] = pygame.Rect(0, height - lava_height, lava_width * 10, lava_height)

            character.position.y = height - character.get_height() - boden

        # FPS Settings
        clock.tick(fps)

        if kills_enemys == 5:
            WIN.blit(spielgewonnen_lbl, text_win_rect)
            pygame.display.update()
            pygame.time.wait(1000)
            won_game = True
        left, middle, right = pygame.mouse.get_pressed()

        if start_screen:
            if text_rect.collidepoint(pygame.mouse.get_pos()):
                spiel_starten_lbl = font_screen.render("Spiel starten", False, color_red)
                if left:
                    button_clicked = True
                    character.set_animation(["jump", "r"])
            else:
                spiel_starten_lbl = font_screen.render("Spiel starten", False, color_white)

            if character.animation_time > 7.5 and not character.get_animation()[0] == "idle":
                character.set_animation(["idle", "r"])

            if button_clicked and character.animation_time > 2 and character.get_animation()[0] == "idle":
                character.set_animation(["idle", "r"])
                start_screen = False
                character.animation_times = 1
                spiel_gestartet_mit_knopf_druck = True

        elif game_over_screen:
            if spielneustarten_rect.collidepoint(pygame.mouse.get_pos()):
                spielneustarten_lbl = font_newstart_screen.render("Neustarten", False, color_red)
                if left:
                    game_over_screen = False
                    character.animation_times = 1
                    spiel_gestartet_mit_knopf_druck = True
                    anzahl_enemys = 0
                    world_move(-world_offset[0], 0)
                    world_offset[0] = 0
                    anzahl_enemys_counter = 5
                    kills_enemys = 0
                    enemy_objects = {}
                    character = main_character("Franz", WIN, enemy_objects, clock, speed=3,
                                               rand_links=rand_links, rand_rechts=rand_rechts)
                    steuerung = controls(rand_links, rand_rechts, character, clock, objects_ingame)
                    character.set_walking_block(True)
                    pygame.mixer.music.set_pos(0)
            else:
                spielneustarten_lbl = font_newstart_screen.render("Neustarten", False, color_white)
        else:
            # LAVA ANIMATION
            if anzahl <= 3:
                anzahl += 0.03
                lava_image = pygame.image.load(os.path.join("Assets", "lava", str(math.floor(anzahl)) + ".png"))
                objects_ingame_images["boden"] = pygame.transform.scale(lava_image, (lava_width, lava_height))
            else:
                anzahl = 1

            tastatur_druck(pygame.key.get_pressed(), left)

            if character.animation_time == int(character.animation_dict.get(character.get_animation()[0]) // 2) and (
                    character.get_animation()[0] == "hit"):
                crash_detected_enemy = crash_detection()
                for enemy_crashed in crash_detected_enemy:
                    if enemy_crashed[0]:
                        try:
                            enemy_crashed[1].damage(character.get_power())
                            if enemy_crashed[1].health <= 0:
                                kills_enemys += 1
                        except Exception as e:
                            print(str(e))

            for name, enemy_check in enemy_objects.items():
                if name == "boden":
                    continue
                if not enemy_objects[name] == "DEAD" and enemy_objects[name].health == -500:
                    enemy_objects[name] = "DEAD"
                    anzahl_enemys_counter -= 1

            # enemys werden gespawnt
            if anzahl_enemys < 5:
                spawn_enemys()
            # fenster wird gezeichnet
            if character.health <= 0 and character.health_animations_bar_rect_time <= 0:
                WIN.blit(spielverloren_lbl, text_gover_rect)
                pygame.display.update()
                pygame.time.wait(2000)
                game_over_screen = True
                if character.get_animation()[1] == "l":
                    character.set_animation(["idle", "l"])
                elif character.get_animation()[1] == "r":
                    character.set_animation(["idle", "r"])

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.WINDOWMAXIMIZED:
                width, height = pygame.display.get_surface().get_size()
                update_window(event.type)
            if event.type == pygame.WINDOWRESTORED:
                width, height = pygame.display.get_surface().get_size()
                update_window(event.type)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F1:
                    if not f1_clicked_enemy_view:
                        f1_clicked_enemy_view = True
                    else:
                        f1_clicked_enemy_view = False
                if event.key == pygame.K_F2:
                    if not f2_clicked_character_view:
                        f2_clicked_character_view = True
                    else:
                        f2_clicked_character_view = False
                if (event.key == pygame.K_SPACE or event.key == pygame.K_w) and not character.get_walking_block():
                    if character.get_position().y <= (height - character.get_height() - boden):
                        steuerung.up(False)

        if not start_screen and not left and spiel_gestartet_mit_knopf_druck and not game_over_screen:
            spiel_gestartet_mit_knopf_druck = False
            character.set_walking_block(False)

        draw_window()

    pygame.quit()


if __name__ == "__main__":
    main()
