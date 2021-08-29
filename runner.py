import pygame
from random import randint

gravity = 0
game_active = False
start_time = 0
score = 0

def display_score():
    current_time = int((pygame.time.get_ticks()/1000)) - start_time
    score_font = my_font.render(f'Score: {current_time}', False, 'black')
    score_rect = score_font.get_rect(center=(400,50))
    screen.blit(score_font,score_rect)
    return current_time

def obstacle_moment(obstacle_list):
    if obstacle_list:
        for obstalce_rect in obstacle_list:
            obstalce_rect.x -= 5
            
            if obstalce_rect.bottom == 300:
                screen.blit(snail_surf,obstalce_rect)
            else:
                screen.blit(fly_surf,obstalce_rect)

        obstacle_list = [obstacle for obstacle in obstacle_list if obstacle.x > -100]
        return obstacle_list
    else:
        return list()

def collsions(player,obstacle):
    if obstacle:
        for obstacle_rect in obstacle:
           if player.colliderect(obstacle_rect): return False
    return True

def player_animations():
    global player_index, player_surf
    if player_rect.bottom < 300:
        player_surf = player_jump
    else:
        player_index += 0.1
        if player_index >= len(player_walk): player_index = 0
        player_surf = player_walk[int(player_index)]

pygame.init()

screen = pygame.display.set_mode((800,400))
pygame.display.set_caption("Runner")
clock = pygame.time.Clock()

jump = pygame.mixer.Sound('audio\jump.mp3')
jump.set_volume(1)
music = pygame.mixer.Sound('audio\music.wav')


my_font = pygame.font.Font('font\Pixeltype.ttf',50)

sky_surf = pygame.image.load('graphics\Sky.png')
ground_surf = pygame.image.load('graphics\ground.png')


player_walk1 = pygame.image.load('graphics\Player\player_walk_1.png')
player_walk2 = pygame.image.load('graphics\Player\player_walk_2.png')
player_walk = [player_walk1,player_walk2]
player_index = 0
player_jump = pygame.image.load('graphics\Player\jump.png')
player_surf = player_walk[player_index]
player_rect = player_surf.get_rect(midbottom=(80,300))

player_stand = pygame.image.load('graphics\Player\player_stand.png')
player_stand = pygame.transform.rotozoom(player_stand,0,2)
player_stand_rect = player_stand.get_rect(center=(400,200))

game_name = my_font.render("Pixal Runner", False, (111,196,169))
game_name_rect = game_name.get_rect(center=(400,50))

game_message = my_font.render("Tap Space To Run", False, (111,196,169))
game_message_rect = game_message.get_rect(center=(400,330))

snail_frame1 = pygame.image.load('graphics\snail\snail1.png')
snail_frame2 = pygame.image.load('graphics\snail\snail2.png')
snail_frames = [snail_frame1,snail_frame2]
snail_index = 0
snail_surf = snail_frames[snail_index]

fly_frame1 = pygame.image.load('graphics\Fly\Fly1.png')
fly_frame2 = pygame.image.load('graphics\Fly\Fly2.png')
fly_frames = [fly_frame1,fly_frame2]
fly_index = 0
fly_surf = fly_frames[fly_index]

obstacle_rect_list = list()

music.play(loops = -1)


obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 1500)

snail_animation_timer = pygame.USEREVENT + 2
pygame.time.set_timer(snail_animation_timer,500)

fly_animation_timer = pygame.USEREVENT + 3
pygame.time.set_timer(fly_animation_timer,200)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if game_active:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and player_rect.bottom == 300:
                    gravity = -20
                    jump.play()
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True
                start_time = int((pygame.time.get_ticks()/1000))

        if game_active:
            if event.type == obstacle_timer:
                if randint(0,2):
                    obstacle_rect_list.append(snail_surf.get_rect(bottomright=(randint(900,1100),300)))
                else:
                    obstacle_rect_list.append(fly_surf.get_rect(bottomright=(randint(900,1100),210)))

            if event.type == snail_animation_timer:
                if snail_index == 0: snail_index = 1
                else: snail_index = 0
                snail_surf = snail_frames[snail_index]
            
            if event.type == fly_animation_timer:
                if fly_index == 0: fly_index = 1
                else: fly_index = 0
                fly_surf = fly_frames[fly_index]

    if game_active:
        screen.blit(sky_surf,(0,0))
        screen.blit(ground_surf,(0,300))
        
        score = display_score()
        gravity += 1
        player_rect.y += gravity
        if player_rect.bottom >= 300: player_rect.bottom = 300
        screen.blit(player_surf,player_rect)
        player_animations()

        obstacle_rect_list  = obstacle_moment(obstacle_rect_list)

        game_active = collsions(player_rect,obstacle_rect_list)
        
    else:
        screen.fill((92,111,233))
        screen.blit(player_stand,player_stand_rect)
        screen.blit(game_name,game_name_rect)
        obstacle_rect_list.clear()

        score_message = my_font.render(f"Your Score is  {score}", False, (111,196,169))
        score_message_rect = score_message.get_rect(center=(400,330))
        
        if score == 0: screen.blit(game_message,game_message_rect)
        else: screen.blit(score_message,score_message_rect)



    pygame.display.update()
    clock.tick(60)