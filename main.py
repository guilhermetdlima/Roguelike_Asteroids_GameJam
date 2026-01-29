import pygame, sys, os, math

dirpath = os.getcwd()
sys.path.append(dirpath)
if getattr(sys, "frozen", False):
    os.chdir(sys._MEIPASS)

from cutSceneEnterLevel import CutSceneEnterLevel
from cutSceneEnterShop import CutSceneEnterShop
from cutSceneExitShop import CutSceneExitShop
from cutSceneManager import CutSceneManager
from cutSceneShop import CutSceneShop
from player import Player
from bulletConfig import BulletConfig
from baseAsteroid import BaseAsteroid
from fastAsteroid import FastAsteroid
from tankAsteroid import TankAsteroid
from multAsteroid import MultAsteroid
from levelManager import LevelManager
from shop import shopMenu
from itens import itens
from laser import LaserBullet

pygame.init()

infoObject = pygame.display.Info()
SCREEN_WIDTH = infoObject.current_w
SCREEN_HEIGHT = infoObject.current_h
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN | pygame.SCALED)
pygame.display.set_caption("roguelike sem nome")
clock = pygame.time.Clock()
FPS = 60

START_MENU = "start_menu"
DIFFICULTY_MENU = "difficulty_menu"
GAMEPLAY = "gameplay"
GAMEPLAY_ENTER_CUTSCENE = "gameplay_enter_cutscene"
SHOP_MENU = "shop_menu"
SHOP_ENTER_CUTSCENE = "shop_enter_cutscene"
WIN_SCREEN = "win_screen"
HIGHSCORE_SCREEN = "highscore_screen"
small_font = pygame.font.SysFont(None, 24) 
font = pygame.font.SysFont(None, 36)
player_sprite = pygame.image.load("imagens/player.png").convert_alpha()
player_sprite = pygame.transform.scale(player_sprite, (50, 50))
bossSprite = pygame.image.load("imagens/boss.png").convert_alpha()
bossSprite = pygame.transform.scale(bossSprite, (500, 500))
background = pygame.image.load("imagens/background1.jpg").convert_alpha()
background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))
backgroundLoja = pygame.image.load("imagens/backgroundLoja.png").convert_alpha()
backgroundLoja = pygame.transform.scale(backgroundLoja, (SCREEN_WIDTH, SCREEN_HEIGHT))
barra_topo_img = pygame.image.load("imagens/barra_topo_img.png").convert_alpha()
barra_topo_img = pygame.transform.scale(barra_topo_img, (SCREEN_WIDTH, barra_topo_img.get_height()))
bullet_spritesheet = pygame.image.load("imagens/bullet_spritesheet2.png").convert_alpha()
bossBulletSprite = pygame.image.load("imagens/bullet_spritesheet3.png").convert_alpha()

shoot_sound = pygame.mixer.Sound("sounds/shoot_sfx2.mp3")
shoot_sound.set_volume(0.15)
pygame.mixer.set_num_channels(32)
print(SCREEN_WIDTH, SCREEN_HEIGHT)

def draw_text_centered(text, font, color, surface, x, y):
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect(center=(x, y))
    surface.blit(text_obj, text_rect)
    return text_rect

def draw_button(text, rect, selected=False):
    color = (100, 100, 255) if selected else (50, 50, 50)
    pygame.draw.rect(SCREEN, color, rect)
    pygame.draw.rect(SCREEN, (255, 255, 255), rect, 2)
    draw_text_centered(text, font, (255, 255, 255), SCREEN, rect.centerx, rect.centery)


def load_highscores(filename="highscore.txt"):
    try:
        with open(filename, "r") as f:
            scores = [int(line.strip()) for line in f.readlines()]
        scores.sort(reverse=True)
        return scores[:10]
    except FileNotFoundError:
        return [0]*10

def save_highscore(new_score, filename="highscore.txt"):
    scores = load_highscores(filename)
    scores.append(new_score)
    scores = sorted(scores, reverse=True)[:10]
    with open(filename, "w") as f:
        for score in scores:
            f.write(f"{score}\n")

def draw_health_bar_centered(surface, player, screen_width, y=20):
    max_health = player.max_health if hasattr(player, "max_health") else 10
    num_cubes = 5
    health_per_cube = max_health / num_cubes
    current_cubes = int(player.health / health_per_cube + 0.999)  # Arredonda para cima

    cube_width = 30
    cube_height = 30
    spacing = 8

    total_width = num_cubes * cube_width + (num_cubes - 1) * spacing
    start_x = (screen_width // 2) - (total_width // 2)

    for i in range(num_cubes):
        x = start_x + i * (cube_width + spacing)
        color = (0, 200, 0) if i < current_cubes else (60, 60, 60)
        if player.health > player.max_health // 2:
            color = (0, 200, 0) if i < current_cubes else (60, 60, 60)
        elif player.health > player.max_health // 4:
            color = (200, 200, 0) if i < current_cubes else (60, 60, 60)
        else :
            color = (200, 0, 0) if i < current_cubes else (60, 60, 60)
            
        pygame.draw.rect(surface, color, (x, y, cube_width, cube_height), border_radius=6)
        pygame.draw.rect(surface, (255, 255, 255), (x, y, cube_width, cube_height), 2, border_radius=6)

def main():
    game_state = START_MENU

    #Configurações da loja
    
    score_timer = pygame.time.get_ticks()
    score_interval = 2000  # 2 segundos em milissegundos
    
    #Botões do menu
    start_button_rect = pygame.Rect(SCREEN_WIDTH//2 - 100, SCREEN_HEIGHT//2 - 25, 200, 50)
    easy_button_rect = pygame.Rect(SCREEN_WIDTH//2 - 100, SCREEN_HEIGHT//2 - 100, 200, 50)
    medium_button_rect = pygame.Rect(SCREEN_WIDTH//2 - 100, SCREEN_HEIGHT//2 - 40, 200, 50)
    hard_button_rect = pygame.Rect(SCREEN_WIDTH//2 - 100, SCREEN_HEIGHT//2 + 20, 200, 50)
    begin_button_rect = pygame.Rect(SCREEN_WIDTH//2 - 100, SCREEN_HEIGHT//2 + 100, 200, 50)
    return_button_rect = pygame.Rect(SCREEN_WIDTH//2 - 100, SCREEN_HEIGHT//2 + 160, 200, 50)
    play_again_button_rect = pygame.Rect(SCREEN_WIDTH//2 - 100, SCREEN_HEIGHT//2, 200, 50)
    back_to_menu_button_rect = pygame.Rect(SCREEN_WIDTH//2 - 100, SCREEN_HEIGHT//2 + 70, 200, 50)
    highscore_button_rect = pygame.Rect(SCREEN_WIDTH//2 - 100, SCREEN_HEIGHT//2 + 60, 200, 50)
    back_from_highscore_button_rect = pygame.Rect(SCREEN_WIDTH//2 - 100, SCREEN_HEIGHT//2 + 200, 200, 50)

    #Configurações do jogador
    bulletConfig = BulletConfig(damage=5, cooldown=0.6, speed=15)
    player = Player(speed=5, health=10, bullet_config=bulletConfig, sprite=player_sprite, bulletSprite=bullet_spritesheet, shootSFX=shoot_sound)

    #Vetor usado para controlar as balas na tela
    bullets = []
    enemy_bullets = []
    laser_bullets = []
    floating_texts = []
    selected_difficulty = "Normal"
    #Gerenciador de niveis      
    level_manager = LevelManager(SCREEN_WIDTH, SCREEN_HEIGHT)
    
    #Preenche o vetor inimigos com os inimigos do nivel atual -- AQUI SERÁ IMPLEMENTADA A DIFICULDADE, PASSANDO-A POR PARAMETRO
    enemies = level_manager.spawn_enemies(player, player.bullet_config, selected_difficulty, bossSprite, bossBulletSprite) 

    #Configurações da loja
    font = pygame.font.SysFont(None, 36)
    shop_items = [
        itens("Vida +5", 2, lambda p: setattr(p, "health", p.health + 5), "Comum"),
        itens("Dano +1", 3, lambda p: setattr(p.bullet_config, "damage", p.bullet_config.damage + 1 ),"Comum"),
        itens("Cooldown -0.1", 3, lambda p: setattr(p.bullet_config, "cooldown", max(0.1, p.bullet_config.cooldown - 0.1)), "Comum"),
        itens("Multitiro + 1", 7, lambda p: setattr(p.bullet_config, "multB", p.bullet_config.multB + 1), "Raro" ),
        itens("Balas teleguiadas", 10, lambda p: setattr(p.bullet_config, "homing", True), "Léndario"),
        itens("Bala + 1", 7, lambda p: setattr(p.bullet_config, "numB", p.bullet_config.numB + 1), "Raro"),
        itens("Inimigo explode ao morrer.", 5, lambda p: setattr(p.bullet_config, "bomb", True), "Léndario"),
        itens("Laser.", 10, lambda p: setattr(p.bullet_config, "type", "laser" ), "Léndario"),   
        itens("Chance de Critico + 10%", 2, lambda p: setattr(p.bullet_config, "critC", p.bullet_config.critC + 0.1), "Incomum"),
        ]
    shop = shopMenu(SCREEN, font, shop_items)  # shop_items é a lista de itens da loja
    

    cut_scene_manager = CutSceneManager(SCREEN)
    

    running = True
    while running:

        clock.tick(FPS)
        current_time = pygame.time.get_ticks()
        if game_state == GAMEPLAY and current_time - score_timer >= score_interval:
            player.score = max(0, player.score - 60)
            score_timer = current_time
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

            # WIN SCREEN BUTTONS FUNCTIONALITY
            if game_state == WIN_SCREEN and event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                if play_again_button_rect.collidepoint((mx, my)):
                    # Reset player and game state
                    player.health = 10
                    player.money = 0
                    player.score = 0
                    player.bullet_config = BulletConfig(damage=4, cooldown=0.7)
                    # Reset other player stats if needed
                    level_manager.current_level = 1
                    enemies = level_manager.spawn_enemies(player, player.bullet_config, selected_difficulty, bossSprite, bossBulletSprite)
                    bullets.clear()
                    laser_bullets.clear()
                    game_state = GAMEPLAY
                    if hasattr(main, "score_saved"):
                        del main.score_saved
                elif back_to_menu_button_rect.collidepoint((mx, my)):
                    # Reset everything as needed
                    player.health = 10
                    player.money = 0
                    player.score = 0
                    player.bullet_config = BulletConfig(damage=4, cooldown=0.7)
                    level_manager.current_level = 1
                    enemies = level_manager.spawn_enemies(player, player.bullet_config, selected_difficulty, bossSprite, bossBulletSprite)
                    bullets.clear()
                    laser_bullets.clear()
                    game_state = START_MENU
                    if hasattr(main, "score_saved"):
                        del main.score_saved

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                if game_state == START_MENU:
                    if start_button_rect.collidepoint((mx, my)):
                        game_state = DIFFICULTY_MENU
                    elif highscore_button_rect.collidepoint((mx, my)):
                        game_state = HIGHSCORE_SCREEN

                elif game_state == DIFFICULTY_MENU: #SELECAO DIFICULDADE
                    if easy_button_rect.collidepoint((mx, my)):
                        selected_difficulty = "Easy"
                    elif medium_button_rect.collidepoint((mx, my)):
                        selected_difficulty = "Medium"
                    elif hard_button_rect.collidepoint((mx, my)):
                        selected_difficulty = "Hard"

                    elif return_button_rect.collidepoint((mx, my)): #BOTAO VOLTAR
                        game_state = START_MENU

                    elif begin_button_rect.collidepoint((mx, my)) and selected_difficulty: #BOTAO INICIAR
                        cut_scene_manager.update()
                        cut_scene_manager.draw()
                        game_state = GAMEPLAY

                elif game_state == HIGHSCORE_SCREEN:
                    if back_from_highscore_button_rect.collidepoint((mx, my)):
                        game_state = START_MENU
                
        if game_state == SHOP_ENTER_CUTSCENE:
            SCREEN.fill((0, 0, 0))
            SCREEN.blit(background, (0, 0))
            cut_scene_manager.update()
            cut_scene_manager.draw()
            player.draw(SCREEN)
            if not cut_scene_manager.cut_scene_running:
                shop.reset_shop()
                shop.reroll_options()
                game_state = SHOP_MENU  # Agora sim, entra na loja

        elif game_state == SHOP_MENU:
            SCREEN.fill((0, 0, 0))
            SCREEN.blit(backgroundLoja, (0, 0))
            SCREEN.blit(barra_topo_img, (0, 0))
            shop.show_shop(player, SCREEN, font)
            #UI onde mostra vida, pontuacao, dinheiro e stats para teste
            health_text = font.render(f"Status da Nave", True, (255, 255, 255))
            SCREEN.blit(health_text, ((SCREEN_WIDTH // 4) - 220, 10))
            draw_health_bar_centered(SCREEN, player, (SCREEN_WIDTH // 3) + 6, y= 58)

            score_text = small_font.render(f"Score: {player.score}", True, (0, 0, 0))
            SCREEN.blit(score_text, (SCREEN_WIDTH - 177, 28))
            score_text = small_font.render(f"Dinheiro: {player.money}", True, (0, 0, 0))
            SCREEN.blit(score_text, (SCREEN_WIDTH - 177, 53))
            score_text = small_font.render(f"Nivel: {level_manager.current_level}", True, (0, 0, 0))
            SCREEN.blit(score_text, (SCREEN_WIDTH - 177, 78))

            # Draw player idle animation
            center_x = (SCREEN_WIDTH // 2)
            center_y = 63
            Player.draw_player_idle_animation(SCREEN, player_sprite, center_x, center_y)
            

            exit_button_rect = pygame.Rect((SCREEN_WIDTH // 2) - 70, SCREEN_HEIGHT - 80, 140, 50)
            pygame.draw.rect(SCREEN, (150, 0, 0), exit_button_rect)
            pygame.draw.rect(SCREEN, (255, 255, 255), exit_button_rect, 2)
            exit_text = font.render("Sair da loja", True, (255, 255, 255))
            SCREEN.blit(exit_text, ((SCREEN_WIDTH // 2) - 70, SCREEN_HEIGHT - 65))

            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                shop.handle_mouse_click((mx, my), player)
                if exit_button_rect.collidepoint((mx, my)):
                    cut_scene_shop_exit = CutSceneExitShop(player, SCREEN_WIDTH)
                    cut_scene_manager.start_cut_scene(cut_scene_shop_exit)
                    game_state = "cutscene2"

        if game_state == START_MENU: #Roda as telas
            SCREEN.fill((0, 0, 0))
            SCREEN.blit(background, (0, 0))
            draw_button("Start", start_button_rect)
            draw_button("Highscores", highscore_button_rect)

        elif game_state == DIFFICULTY_MENU:
            SCREEN.fill((0, 0, 0))
            SCREEN.blit(background, (0, 0))
            draw_button("Easy", easy_button_rect, selected_difficulty == "Easy")
            draw_button("Medium", medium_button_rect, selected_difficulty == "Medium")
            draw_button("Hard", hard_button_rect, selected_difficulty == "Hard")
            draw_button("Begin", begin_button_rect)
            draw_button("Return", return_button_rect)
            
        elif game_state == "cutscene":
            
            SCREEN.fill((0, 0, 0))  # Clear the screen!
            SCREEN.blit(barra_topo_img, (0, 0))
            SCREEN.blit(background, (0, 0))
            cut_scene_manager.update()
            cut_scene_manager.draw()
            player.update(FPS)
            player.draw(SCREEN)
            if not cut_scene_manager.cut_scene_running:
                player.set_position(-30, (SCREEN_HEIGHT // 2) + 100)
                cut_scene_shop_enter = CutSceneEnterShop(player, SCREEN_WIDTH)
                cut_scene_manager.start_cut_scene(cut_scene_shop_enter)
                game_state = SHOP_ENTER_CUTSCENE
        
        #cutscene de saida da loja
        elif game_state == "cutscene2":
            
            SCREEN.fill((0, 0, 0))
            SCREEN.blit(barra_topo_img, (0, 0))
            SCREEN.blit(background, (0, 0))
            cut_scene_manager.update()
            cut_scene_manager.draw()
            player.draw(SCREEN)
            if not cut_scene_manager.cut_scene_running:
                player.set_position(-30, (SCREEN_HEIGHT // 2) - player.height // 2)
                cut_scene_gameplay_enter = CutSceneEnterLevel(player, SCREEN_WIDTH)
                cut_scene_manager.start_cut_scene(cut_scene_gameplay_enter)
                game_state = GAMEPLAY_ENTER_CUTSCENE
        
        #cutscene de entrada na fase
        elif game_state == GAMEPLAY_ENTER_CUTSCENE:
            SCREEN.fill((0, 0, 0))
            SCREEN.blit(barra_topo_img, (0, 0))
            SCREEN.blit(background, (0, 0))
            
            player.update(FPS)
            cut_scene_manager.update()
            cut_scene_manager.draw()
            player.draw(SCREEN)
            if not cut_scene_manager.cut_scene_running:
                game_state = GAMEPLAY


        elif game_state == GAMEPLAY:
            # gameplay normal aqui
            
            cut_scene_shop_enter = CutSceneEnterShop(player, SCREEN_WIDTH)
            cut_scene_manager.start_cut_scene(cut_scene_shop_enter)
            keys = pygame.key.get_pressed()
            player.move(keys, SCREEN_WIDTH, SCREEN_HEIGHT)


            # Verifica se o vetor de inimigos está vazio, avançando para o proximo nivel
            if not enemies:
                level_manager.next_level(player)
                if level_manager.current_level == 25:
                    game_state = WIN_SCREEN
                elif level_manager.current_level % 4 == 0:
                    cut_scene_shop = CutSceneShop(player, bullets, laser_bullets, enemies, SCREEN_WIDTH)
                    cut_scene_manager.start_cut_scene(cut_scene_shop)
                    print(f"Avançando para o nível {level_manager.current_level}")
                    game_state = "cutscene"
                else:
                    enemies = level_manager.spawn_enemies(player, player.bullet_config, selected_difficulty, bossSprite, bossBulletSprite)
                    print(f"Avançando para o nível {level_manager.current_level}")
            
            #Move os inigmiso
            for enemy in enemies:
                if hasattr(enemy, "update"):
                    enemy.update(enemy_bullets)  # BossShooter vai atirar!
                enemy.move(SCREEN_WIDTH, SCREEN_HEIGHT)
                if player.rect.colliderect(enemy.rect): #Verifica se o jogador colidiu com algum inimigo
                    push_distance = 5
                    push_angle = math.atan2(player.rect.centery - enemy.rect.centery, player.rect.centerx - enemy.rect.centerx)
                    player.x += math.cos(push_angle) * push_distance
                    player.y += math.sin(push_angle) * push_distance
                    player.rect.topleft = (player.x, player.y)
                    player.take_damage(enemy.damage)
                    enemy.angle = math.atan2(enemy.rect.centery - player.rect.centery, enemy.rect.centerx - player.rect.centerx)
                    enemy.x += enemy.speed * math.cos(enemy.angle)
                    enemy.y += enemy.speed * math.sin(enemy.angle)
                    enemy.rect.topleft = (enemy.x, enemy.y)

            # After moving enemies, before drawing:
            for enemy in enemies[:]:
                # If it's a SpawnerAsteroid, try to spawn new enemies
                if hasattr(enemy, "try_spawn_enemy"):
                    new_enemies = enemy.try_spawn_enemy()
                    if new_enemies:
                        enemies.extend(new_enemies)
                
            
            #Atira
            if pygame.mouse.get_pressed()[0]:
                if player.bullet_config.type == "laser":
                    laser = player.shot_laser()
                    if laser:
                        laser_bullets.append(laser)
                elif player.bullet_config.type == "bala":
                    player.agenda_shoot()
                    player.update_shooting(bullets)
                
            if player.health <= 0:
                game_state = WIN_SCREEN
                bullets.clear()
                laser_bullets.clear()

            #Aumenta velocidade de tiros para teste
            if keys[pygame.K_r]:
                if player.bullet_config.cooldown > 0.01:
                    player.bullet_config.cooldown -= 0.05
                else:
                    player.bullet_config.cooldown = 0.01

            if keys[pygame.K_f]:
                    player.bullet_config.cooldown +=0.05

            if keys[pygame.K_t]:
                    player.bullet_config.bounce +=1

            if keys[pygame.K_y]:
                    player.bullet_config.pierce +=1

            

            # Atualiza e desenha o jogador
            SCREEN.fill((0, 0, 0))
            SCREEN.blit(background, (0, 0))

            player.update(FPS)
            player.draw(SCREEN)

            # Before the loop, assume normal speed
            player.max_speed = player.base_max_speed

            laser_firing = False
            for laser in laser_bullets[:]:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                angle = math.degrees(math.atan2(mouse_y - (player.y + player.height // 2), mouse_x - (player.x + player.width // 2)))
                laser.update_position(player.x + player.width // 2, player.y + player.height // 2, angle, smoothing=0.01)
                laser.update_laser()
                laser.draw(SCREEN)
                if laser.fired:
                    laser_firing = True
                    laser_start = (laser.x, laser.y)
                    laser_end = (
                        laser.x + math.cos(laser.angle) * laser.length,
                        laser.y + math.sin(laser.angle) * laser.length
                    )
                    for enemy in enemies[:]:
                        if enemy.rect.clipline(laser_start, laser_end):
                            floating_texts.append({"text": str(laser.damage), "x": enemy.x + enemy.width // 2, "y": enemy.y, "alpha": 255, "time": pygame.time.get_ticks()})
                            if enemy.take_damage(laser.damage, bullets, bulletConfig):
                                enemies.remove(enemy)
                                player.add_score(enemy.score)
                                new_enemies = enemy.on_death(bullets, bulletConfig)
                                if isinstance(new_enemies, list):
                                    enemies.extend(new_enemies)
                if laser.should_remove():
                    laser_bullets.remove(laser)

            # After the loop, apply speed reduction only if a laser is firing
            if laser_firing:
                player.max_speed = player.base_max_speed * 0.1
            else:
                player.max_speed = player.base_max_speed
            # Atualiza e desenha as balas
            for bullet in bullets[:]:
                bullet.update(enemies)
                if bullet.is_off_screen(SCREEN_WIDTH, SCREEN_HEIGHT):
                    bullets.remove(bullet)
                else:
                    bullet.draw(SCREEN)
                    for enemy in enemies[:]: 
                        if bullet.rect.colliderect(enemy.rect):
                            if not bullet.pierced_enemies.get(enemy, False):
                                floating_texts.append({"text": str(bullet.damage), "crit": str(bullet.isCrit), "x": enemy.x + enemy.width // 2, "y": enemy.y, "alpha": 255, "time": pygame.time.get_ticks()})
                                if enemy.take_damage(bullet.damage, bullets, bullet.config):
                                    enemies.remove(enemy)
                                    player.add_score(enemy.score)

                                    new_enemies = enemy.on_death(bullets, bullet.config) #Verifica se o inimigo gera novos inimigos
                                    if isinstance(new_enemies, list):
                                        enemies.extend(new_enemies)

                                bullet.pierced_enemies[enemy] = True #Verifica lógica de só passar por inimigos uma vez até sair dele
                                if bullet.pierce > 0:
                                    bullet.pierce -= 1
                                else: #Aqui será implementado a logica de ricochetear de um inimigo
                                    bullets.remove(bullet)
                                    break
                        else:
                            if enemy in bullet.pierced_enemies:
                                bullet.pierced_enemies[enemy] = False

            # Atualiza e desenha as balas inimigas
            for bullet in enemy_bullets[:]:
                bullet.update([player])  # Passa o player como "alvo"
                if bullet.is_off_screen(SCREEN_WIDTH, SCREEN_HEIGHT):
                    enemy_bullets.remove(bullet)
                else:
                    bullet.draw(SCREEN)
                    # Colisão com o player
                    if bullet.rect.colliderect(player.rect):
                        player.take_damage(bullet.damage)
                        enemy_bullets.remove(bullet)

            # Atualiza e desenha os inimigos
            for enemy in enemies:
                enemy.draw(SCREEN)

            font = pygame.font.SysFont(None, 24)
            current_time = pygame.time.get_ticks()

            for text in floating_texts[:]:
                elapsed = current_time - text["time"]
                text["y"] -= 0.5  # move upward
                text["alpha"] = max(0, 255 - (elapsed // 2))  # fade out

                if text["alpha"] <= 0:
                    floating_texts.remove(text)
                    continue
                if text.get("crit") == "1":
                    damage_surf = font.render(text["text"], True, (255, 0, 0))
                else:
                    damage_surf = font.render(text["text"], True, (255, 255, 255))
                damage_surf.set_alpha(text["alpha"])
                SCREEN.blit(damage_surf, (text["x"], text["y"]))


            SCREEN.blit(barra_topo_img, (0, 0))


            #UI onde mostra vida, pontuacao, dinheiro e stats para teste
            health_text = font.render(f"Status da Nave", True, (255, 255, 255))
            SCREEN.blit(health_text, ((SCREEN_WIDTH // 4) - 220, 10))
            draw_health_bar_centered(SCREEN, player, (SCREEN_WIDTH // 3) + 6, y= 58)

            score_text = small_font.render(f"Score: {player.score}", True, (0, 0, 0))
            SCREEN.blit(score_text, (SCREEN_WIDTH - 177, 28))
            score_text = small_font.render(f"Dinheiro: {player.money}", True, (0, 0, 0))
            SCREEN.blit(score_text, (SCREEN_WIDTH - 177, 53))
            score_text = small_font.render(f"Nivel: {level_manager.current_level}", True, (0, 0, 0))
            SCREEN.blit(score_text, (SCREEN_WIDTH - 177, 78))

            # Draw player idle animation
            center_x = (SCREEN_WIDTH // 2)
            center_y = 63
            Player.draw_player_idle_animation(SCREEN, player_sprite, center_x, center_y)

        elif game_state == WIN_SCREEN:
            if game_state == WIN_SCREEN and not hasattr(main, "score_saved"):
                save_highscore(player.score)
                main.score_saved = True
            SCREEN.fill((0, 0, 0))
            if player.health > 0:
                win_text = font.render("You Win!", True, (255, 255, 0))
            else:
                win_text = font.render("You Lose! :(", True, (255, 0, 0))
            SCREEN.blit(win_text, (SCREEN_WIDTH//2 - win_text.get_width()//2, SCREEN_HEIGHT//2 - 100))
            draw_button("Play Again", play_again_button_rect)
            draw_button("Back to Menu", back_to_menu_button_rect)

        elif game_state == HIGHSCORE_SCREEN:
            SCREEN.fill((0, 0, 0))
            highscores = load_highscores()
            title = font.render("Top 10 Scores", True, (255, 255, 0))
            SCREEN.blit(title, (SCREEN_WIDTH//2 - title.get_width()//2, 100))
            for i, score in enumerate(highscores):
                score_text = font.render(f"{i+1}. {score}", True, (255, 255, 255))
                SCREEN.blit(score_text, (SCREEN_WIDTH//2 - score_text.get_width()//2, 160 + i*35))
            draw_button("Back", back_from_highscore_button_rect)

        pygame.display.flip()
    pygame.quit()
    sys.exit()

if __name__ == "__main__": 
    main()

