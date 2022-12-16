"""
author = Alex Olivier Michaud
This is the main file of the game, it is used to start the game, show the score and exit the game.
The game is a space shooter like, where you have to avoid the asteroids
to navigate the ship it uses an accelerometer, connected to a raspberry pi
"""
# TODO: reunite the language of the code to english
import pygame
from sys import exit
from random import randint, uniform
from multiprocessing import Process, Queue
from client import client
import sqlite3

# Global variables for window size
H = 800
W = 1000

def score(queue):
    """
    This function is used to show the score in the menu of the game
    :param queue: the main queue of the game to share resources
    :return: None
    """
    global H, W
    pygame.init()
    screen = pygame.display.set_mode((W, H))
    # pygame.image.load("menu.png")
    myFont = pygame.font.Font("8-BIT WONDER.ttf", 30)
    pygame.display.update()
    # database of score
    conn = sqlite3.connect('score.db')
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS score (score integer)")
    c.execute("""SELECT MAX(score) FROM score""")
    data = c.fetchone()
    print(data)
    conn.close()
    if data[0] is None:
        data = 0
    run = True
    while run:
        screen.blit(pygame.image.load("img/menu.png"), (-10, -90))
        # create text
        text_1 = myFont.render("Best Score", True, (0, 0, 0))
        text_2 = myFont.render("Return", True, (0, 0, 0))
        text_score = myFont.render(str(data[0]), True, (0, 0, 0))
        # Creating text rectangles
        text_1_rect = text_1.get_rect(midtop=(W / 2, 300))
        text_2_rect = text_2.get_rect(midtop=(W / 2, 400))
        text_score_rect = text_score.get_rect(midtop=(W / 2, 350))
        # blit text
        screen.blit(text_1, text_1_rect)
        screen.blit(text_2, text_2_rect)
        screen.blit(text_score, text_score_rect)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                queue.put("exit")
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if text_2_rect.collidepoint(event.pos):
                    run = False
                    main_menu(queue)
        pygame.display.flip()
    return


def main_menu(queue):
    """
    This function is used to show the main menu of the game, which is used to start the game,
    show the score and exit the game
    :param queue: the main queue of the game to share resources
    :return: None
    """
    global H, W
    pygame.init()
    screen = pygame.display.set_mode((W, H))
    # font is from https://www.dafont.com/8bit-wonder.font
    myFont = pygame.font.Font("8-BIT WONDER.ttf", 30)
    pygame.display.update()
    run = True
    while run:
        # the queue is used here, because the client is always running, so if you restart the game,
        # the spaceship would otherwise move in a random direction, so if you empty the queue,
        # the spaceship will not move, until you move it, and the [0,0,0] is
        # here, so you will start the game with the spaceship in the middle of the screen
        queue.get()
        queue.put([0, 0, 0])
        # create background
        screen.blit(pygame.image.load("img/menu.png"), (-10, -90))
        # create text
        text_1 = myFont.render("Avoid Asteroids", True, (0, 0, 0))
        text_2 = myFont.render("Press tab to start", True, (0, 0, 0))
        text_3 = myFont.render("Check the score", True, (0, 0, 0))
        # Creating text rectangles
        text_1_rect = text_1.get_rect(midtop=(W / 2, 300))
        text_2_rect = text_2.get_rect(midtop=(W / 2, 350))
        text_3_rect = text_3.get_rect(midtop=(W / 2, 400))
        # blit text
        screen.blit(text_1, text_1_rect)
        screen.blit(text_2, text_2_rect)
        screen.blit(text_3, text_3_rect)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                queue.put("exit")
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    run = False
                    App(queue)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if text_2_rect.collidepoint(event.pos):
                    run = False
                    App(queue)
                if text_3_rect.collidepoint(event.pos):
                    run = False
                    score(queue)
        pygame.display.flip()


def App(queue):
    """
    This function is used to show the game, and to control the game
    :param queue:
    :return:
    """
    global H, W
    pygame.init()
    screen = pygame.display.set_mode((W, H))
    pygame.display.set_caption("Space Invaders")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("Arial", 30)

    # import images
    sky_surface = pygame.image.load("img/l.png")
    ship = pygame.image.load("img/ship.png").convert_alpha()
    meteorite = pygame.image.load("img/meteorite.png").convert_alpha()
    meteorite_2 = pygame.image.load("img/meteorite_2.png").convert_alpha()
    coin = pygame.image.load("img/coin.png").convert_alpha()
    heart = pygame.image.load("img/heart_for_game.png").convert_alpha()
    dead_heart = pygame.image.load("img/die_heart_game.png").convert_alpha()

    # scale images
    ship = pygame.transform.scale(ship, (90, 90))
    meteorite = pygame.transform.scale(meteorite, (90, 90))
    meteorite_2 = pygame.transform.scale(meteorite_2, (90, 90))
    coin = pygame.transform.scale(coin, (90, 90))
    heart = pygame.transform.scale(heart, (50, 50))
    dead_heart = pygame.transform.scale(dead_heart, (50, 50))

    # coordinates
    ship_x = 450
    meteorite_x = randint(0, 1000)
    meteorite_y = 0
    meteorite_x_2 = randint(0, 1000)
    meteorite_y_2 = 0
    coin_x = randint(0, 1000)
    coin_y = 0

    # rectangles
    ship_rect = ship.get_rect(midbottom=(ship_x, 800))
    meteorite_rect = meteorite.get_rect(midbottom=(meteorite_x, meteorite_y))
    meteorite_rect_2 = meteorite_2.get_rect(midbottom=(meteorite_x_2, meteorite_y_2))
    coin_rect = coin.get_rect(midbottom=(coin_x, coin_y))
    sky_surface_rect = sky_surface.get_rect(topleft=(0, 0))
    heart_rect = heart.get_rect(topright=(W, 0))
    heart_rect_2 = heart.get_rect(topright=(W - 50, 0))
    heart_rect_3 = heart.get_rect(topright=(W - 100, 0))
    dead_heart_rect = dead_heart.get_rect(topright=(W, 0))
    dead_heart_rect_2 = dead_heart.get_rect(topright=(W - 50, 0))
    dead_heart_rect_3 = dead_heart.get_rect(topright=(W - 100, 0))

    # speed
    ship_speed = 0
    meteorite_speed = 5
    meteorite_speed_2 = 5
    coin_speed = 5
    # speed in y
    meteorite_speed_y = 0
    meteorite_speed_y_2 = 0
    coin_speed_y = 0

    # number of coins
    coins = 0
    # number of lives
    lives = 3

    # text for coins
    coins_text = font.render(f"Coins: {coins}", True, (255, 255, 255))

    # previous position
    old_position = 0

    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                queue.put("exit")
                pygame.quit()
                exit()

        # spawning objects
        screen.blit(sky_surface, (0, 0))
        screen.blit(ship, ship_rect)
        screen.blit(meteorite, meteorite_rect)
        screen.blit(meteorite_2, meteorite_rect_2)
        screen.blit(coin, coin_rect)
        screen.blit(coins_text, (10, 10))
        screen.blit(heart, heart_rect)
        screen.blit(heart, heart_rect_2)
        screen.blit(heart, heart_rect_3)

        # checking the number of lives and spawning dead hearts if needed
        if lives == 2:
            screen.blit(dead_heart, dead_heart_rect)
        if lives == 1:
            screen.blit(dead_heart, dead_heart_rect)
            screen.blit(dead_heart, dead_heart_rect_2)
        if lives == 0:
            screen.blit(dead_heart, dead_heart_rect)
            screen.blit(dead_heart, dead_heart_rect_2)
            screen.blit(dead_heart, dead_heart_rect_3)
            # updating the number of score in the database
            conn = sqlite3.connect("score.db")
            cursor = conn.cursor()
            cursor.execute("CREATE TABLE IF NOT EXISTS score (score integer)")
            cursor.execute("INSERT INTO score VALUES (?)", (coins,))
            conn.commit()
            conn.close()
            run = False
            ###game over###
            main_menu(queue)

        if queue.empty() is False:
            data = queue.get()
            print(data)
            if ship_rect.left > W:  # if the ship is out of the screen
                ship_speed -= 2
            elif ship_rect.left < 0:  # if the ship is out of the screen
                ship_speed += 2
            elif data[2] > 0:
                ship_speed += 0.01 * data[2]  # linear function to represent the speed of the ship
            elif data[2] <= 0:
                ship_speed += 0.01 * data[2]

        # TODO: make the ship movement more smooth
        if 0 <= ship_rect.left + ship_speed <= W - 90:  # if the ship is in the screen
            ship_rect.left += ship_speed
            if old_position < 0 < ship_speed:  # better movement, if the ship is moving to the right
                # it resets the speed, thus making the movement smoother
                ship_speed -= ship_speed
            elif old_position > 0 > ship_speed:  # same as above but for the left
                ship_speed += ship_speed
            if ship_speed > 200:  # if the speed is too high, it resets it
                ship_speed -= 100
        else:
            ship_speed = 0

        # moving objects, random sleep, random spawn, random speed
        if sky_surface_rect.colliderect(meteorite_rect) is False:
            if meteorite_rect.left == 0:  # if its 0 I would get a division by 0 error
                meteorite_rect.left = 1
            meteorite_speed_y = uniform(-1 * (1000 / meteorite_rect.left), 1000 / (
                    1000 - meteorite_rect.left))  # linear function to represent the direction of the meteorite
            meteorite_speed = randint(3, 10)  # random speed in x
            meteorite_rect.top = 0  # respawn the meteorite at the top of the screen

        if sky_surface_rect.colliderect(meteorite_rect_2) is False:
            if meteorite_rect_2.left == 0:  # if its 0 I would get a division by 0 error
                meteorite_rect_2.left = 1
            meteorite_speed_y_2 = uniform(-1 * (1000 / meteorite_rect_2.left), 1000 / (
                    1000 - meteorite_rect_2.left))  # linear function to represent the direction of the meteorite
            meteorite_speed_2 = randint(3, 10)  # random speed in x
            meteorite_rect_2.top = 0  # respawn the meteorite at the top of the screen

        if sky_surface_rect.colliderect(coin_rect) is False:
            if coin_rect.left == 0:  # if its 0 I would get a division by 0 error
                coin_rect.left = 1
            coin_speed_y = uniform(-1 * (1000 / coin_rect.left), 1000 / (
                    1000 - coin_rect.left))  # linear function to represent the direction of the meteorite
            coin_speed = randint(3, 10)  # random speed in x
            coin_rect.top = 0  # respawn the meteorite at the top of the screen

        # moving objects
        meteorite_rect.top += meteorite_speed
        meteorite_rect_2.top += meteorite_speed_2
        coin_rect.top += coin_speed
        # moving objects in y. m,
        meteorite_rect.left += meteorite_speed_y
        meteorite_rect_2.left += meteorite_speed_y_2
        coin_rect.left += coin_speed_y

        # collisions with the ship, if the ship collides with the meteorite, it loses a life
        # if the ship collides with the coin, it gets a coin and updates the score
        if meteorite_rect.colliderect(ship_rect):
            lives -= 1
            meteorite_rect.top = 0

        if meteorite_rect_2.colliderect(ship_rect):
            lives -= 1
            meteorite_rect_2.top = 0

        if coin_rect.colliderect(ship_rect):
            coins += 1
            coins_text = font.render(f"Coins: {coins}", True, (255, 255, 255))
            coin_rect.top = 0

        pygame.display.update()
        clock.tick(60)


if __name__ == "__main__":
    queue = Queue()  # object to communicate between the processes,
    # the queue is used for the data from the accelerometer the format is [x, y, z]
    menu_proc = Process(target=main_menu, args=(
        queue,))  # process for the menu, it interacts with the functions App() and Score(),
    # so these processes are not needed
    client_proc = Process(target=client, args=(
        queue,))  # process for the accelerometer, it sends the data to the queue,
    # it is imported from the client.py file
    client_proc.start()
    menu_proc.start()
    client_proc.join()
    menu_proc.join()
    ##TODO: if the process menu_proc is closed, the client_proc processes should be closed too
