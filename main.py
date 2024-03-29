
import math
import random

import pygame
from pygame import mixer  # used for playing audio in pygame

from src.bullet import Bullet
from src.constants import *
from src.enemy import Enemy
from src.explosion import Explosion
from src.player import Player

#initialization
pygame.init()


#create a screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))

#set up clock for frame rate count
clock = pygame.time.Clock()

#Create Title
pygame.display.set_caption("War Craft")

#Create Icon for the game
icon = pygame.image.load("assets/images/player.png")
# icon.set_colorkey(WHITE)
pygame.display.set_icon(icon)


#background music
mixer.music.load("assets/audio/background_music.mp3") #load the music file
mixer.music.play(-1)    #play the music in loop

#load image that will be used for backgroud
backgroud_image = pygame.image.load("assets/images/space.jpg").convert()  #load backgroud image
full_life = pygame.image.load("assets/images/full_life.png").convert()    #Load life indicator
full_life.set_colorkey(WHITE)                               #remove whilte backgroud from the image
half_life = pygame.image.load("assets/images/half_life.png").convert()    #load image for half_life
half_life.set_colorkey(WHITE)                               #remove white backgroud from the image


#All the sprite object group
sprites = pygame.sprite.Group()     #all the game sprites
enemies = pygame.sprite.Group()     #all the enemies
bullets = pygame.sprite.Group()     #all the bullets sprites

#return highest_score
def get_highest_score(file_name):
    game_file = {}
    try:
        game_file = open(file_name, "r")    #Open file for reading
        data = game_file.read()
        game_file.close()
        game_file = data
    except Exception:
        game_file = open(file_name, "w")    #if the file doesn't exit() create the file
        game_file.close()
        game_file = ""
    game_file = game_file.split("\n")   #split the opened file by new line
    if len(game_file) > 0:              #if the file is not empty return the content
        try:
            return int(game_file[0])
        except Exception:
            return 0
    return 0                           #return zero if no content

#draw life
def remaining_life_draw():
    write_screen("Life : ", WHITE, (350,0), 24)
    init_pos = 250 + 7*24
    for i in range(remaining_life//2):
        screen.blit(full_life, (init_pos+i*24, 0))
    if remaining_life%2 != 0:
        screen.blit(half_life, (init_pos+(remaining_life//2)*24, 0))


#write text on screen
def write_screen(message, text_color, cordinate, font_size, font_style="freesansbold.ttf"):
    '''
        write text to the screen

        message : the test to be write on screen
        text_color: the color of the text written on the screen
        coordinate : the coordinate the text will be displayed
        font_size : the font size of the displayed text
        font_style : the font style of the text
    '''
    font = pygame.font.Font(font_style, font_size)
    screen_text = font.render(message, True, text_color)
    screen.blit(screen_text, cordinate)


#Initializing game file
# def game_static_init():
    # highest_score = get_highest_score("highest_score.txt")  #update the global variable for highest_score
    # print(highest_score)

#game space
def backgroud():
    '''
        update the backgroud and score components before drawing game sprites
    '''
    screen.fill(BLACK)  #fill the backgroud with black color
    screen.blit(backgroud_image, (0,-599))  #place the backgroud image
    write_screen("Score : {}".format(str(current_score)), WHITE, (0,0), 24) #write the current score on the screen
    write_screen("Level : {}".format(str(current_level)), WHITE, (200,0), 24)   #write the current level on the screen
    remaining_life_draw()
    highest_score = get_highest_score("highest_score.txt")  #update the global variable for highest_score
    write_screen("High Score: {}".format(str(highest_score)), WHITE, (550,0), 24)   #write the highest score on the screen


player = Player()       #initialize the player object(sprite)
sprites.add(player)     #include the player sprite in the group of sprites
enemy = Enemy(sprites, enemies)         #initialize the first enemy sprite
sprites.add(enemy)      #add the enemy sprite to the sprite group used to update the screen
enemies.add(enemy)      #add the enemy sprite to the sprite group used keeping track of enemies



#Game Loop
running = True      #variable used to keep the game loop running or stop
# game_static_init()  #initialize from the static file
while running:
    clock.tick(FRAME_RATE)  #set the frame rate of the game

    #track events
    for event in pygame.event.get():
        #check if a close event has occured
        if event.type == pygame.QUIT:
            running = False
        #if any key is pressed
        elif event.type == pygame.KEYDOWN:
            #if the key pressed is space
            if event.key == pygame.K_SPACE:
                gun_shot = mixer.Sound("assets/audio/shoot.wav")     #load shooting sound
                gun_shot.play()                         #emit shooting sound
                player.shoot(sprites, bullets)                          #place a bullet at the player's possition
            #if the key pressed is p to pause
            if event.key == pygame.K_p:
                write_screen("PAUSE", WHITE, (300, 200), 64)    #write pause on screen
                write_screen("press p to play", WHITE, (320, 280), 24)  #write how to start play on the screen
                pygame.display.update()                         #update the screen

                #start loop till player decide to restart
                keep_loop = True
                while keep_loop:
                    #track events
                    for event in pygame.event.get():
                        #catch key press
                        if event.type == pygame.KEYDOWN:
                            #catch p press
                            if event.key == pygame.K_p:     #break from the loop
                                keep_loop = False
                                break



    #Update the game elements
    sprites.update()        #update the sprites on the screen

    #look for collision between enemies and bullet
    bullet_hit = pygame.sprite.groupcollide(enemies, bullets, True, True)
    #check for the specific enemy hit
    for hit in bullet_hit:
        # print("hit group : ", dir(hit.groups), "\n hit rect", dir(hit.rect))
        explosion_sound = mixer.Sound("assets/audio/explosion.wav")  #load explosion sound
        explosion_sound.play()                          #emit explosion sound
        explosion_x = hit.rect.x + 32                   #calculate the x coordinate of the explosion image relative to the postion of the enemy
        explosion_y = hit.rect.y + 32                   #calculate the y coordinate of the explosion image relative to the postion of the enemy
        explosion = Explosion(explosion_x, explosion_y) #place an explosion
        sprites.add(explosion)                          #add the explosion to group for update
        current_score += 1                              #increment score
        #increment the number of enemies based on the increment_enemy value
        for i in range(increment_enemy):
            enemy = Enemy(sprites, enemies)
            sprites.add(enemy)
            enemies.add(enemy)


    #look for collision between player and enemies
    player_hit = pygame.sprite.spritecollide(player, enemies, False)
    #check if there is a hit
    if len(player_hit) > 0: #check for the specific enemy collided with
        for enemy_sprite in player_hit:
            explosion_sound = mixer.Sound("assets/audio/explosion.wav")  #load explosion sound
            explosion_sound.play()                          #emit explosion sound
            #calculate x and y coordinate for explosion
            explosion_x = min(enemy_sprite.rect.centerx, player.rect.centerx) + math.sqrt(math.pow((enemy_sprite.rect.centerx-player.rect.centerx), 2))//2
            explosion_y = min(enemy_sprite.rect.centery, player.rect.centery) + math.sqrt(math.pow((enemy_sprite.rect.centery-player.rect.centery), 2))//2
            explosion = Explosion(explosion_x, explosion_y) #place an explosion
            sprites.add(explosion)                          #add the explosion to group for update
            remaining_life -= 1                             #decrement the playing life
            enemy_sprite.kill()                             #remove the enemy involved in the collision
            enemy = Enemy(sprites, enemies) #create a new enemy
            sprites.add(enemy)  #add the enemy to the sprite group for update
            enemies.add(enemy)  #add the enemy to the sprite group for that keeps track of the enemies sprite
            # explosions.add(explosion)




    #Redraw the screen with the update
    backgroud()
    sprites.draw(screen)

    #calculate the current level
    current_level = current_score//10 if current_score//10 > 0 else 1

    #define the difficulty for level 1
    if current_level == 1:  #increment 1 enemy for every enemy destroyed, make the enemies speedx = 2, make the enemies speedy = 2
        increment_enemy = 1
        enemy_speed_x = 2
        enemy_speed_y = 2
    #define the difficulty for level 2
    elif current_level == 2:    #increment 2 enemy for every enemy destroyed, make the enemies speedx = 2, make the enemies speedy = 2
        increment_enemy = 2
        enemy_speed_x = 2
        enemy_speed_y = 2
    #define the difficulty for level 3
    elif current_level == 3:    #increment 1 enemy for every enemy destroyed, make the enemies speedx = 3, make the enemies speedy = 3
        increment_enemy = 1
        enemy_speed_x = 3
        enemy_speed_y = 3
    #define the difficulty for level 4
    elif current_level == 4:    #increment 1 enemy for every enemy destroyed, make the enemies speedx = 4, make the enemies speedy = 4
        increment_enemy = 1
        enemy_speed_x = 4
        enemy_speed_y = 4
    #define the difficulty for level 5
    elif current_level == 5:    #increment 1 enemy for every enemy destroyed, make the enemies speedx = 5, make the enemies speedy = 5
        increment_enemy = 1
        enemy_speed_x = 5
        enemy_speed_y = 5


    #check if life has finished
    if remaining_life <= 0:     #if life is now zero
        write_screen("GAME OVER", WHITE, (200, 200), 64)    #display game over
        write_screen("press q to quit and r to restart", WHITE, (220, 280), 24) #display instruction to quit or restart the game with
        pygame.display.update() #update the screen

        #fetch the initial highest score in storage
        highest_score = get_highest_score("highest_score.txt")
        if current_score > highest_score: #check if the current score is more than the iniitial highest_score then update the stored highest score
            # update the stored highest score with the new highest score
            score_file = open("highest_score.txt", "w")
            score_file.write(str(current_score))
            score_file.close()
            highest_score = current_score

        #wait for user to either quit or replay the game
        keep_loop = True
        while keep_loop:
            #track events
            for event in pygame.event.get():
                #check if key press event occured
                if event.type == pygame.KEYDOWN:
                    #if q is pressed quit the game by setting running to False this will cause the game loop to end
                    if event.key == pygame.K_q:
                        running = False
                        keep_loop = False
                    #if r key is pressed restart the game by initializing the gaming parameters to the original values
                    if event.key == pygame.K_r:
                        keep_loop = False
                        enemy_speed_x = 2   #enemy speedx = 2
                        enemy_speed_y = 2   #enemy speedy = 2
                        current_level = 1   #current level to 1
                        current_score = 0   #score to 0
                        remaining_life = 6  #remaing life to 6/2
                        sprites.empty()     #clear all the sprite fron the screen
                        enemies.empty()     #remove all the enemies sprite
                        bullets.empty()     #remove all the bullets sprites
                        player = Player()       #initialize the player object(sprite)
                        sprites.add(player)     #include the player sprite in the group of sprites
                        enemy = Enemy(sprites, enemies)     #create on new enemy
                        sprites.add(enemy)  #set the enemy for screen update
                        enemies.add(enemy)  #add the enemy to the group that keeps track of the enemies
                        break
    #pygame display update
    pygame.display.update()     #update the display

#Update high score before quiting the game
highest_score = get_highest_score("highest_score.txt")
if current_score > highest_score:
    # print("current : ", current_score, "\nhigh : ", highest_score)
    score_file = open("highest_score.txt", "w")
    score_file.write(str(current_score))
    score_file.close()
    highest_score = current_score

#close the python program
pygame.quit()
