import pygame as pg
import random, time
import asyncio

pg.init()
clock = pg.time.Clock()

black = (0, 0, 0)

win_width = 800
win_height = 600
screen = pg.display.set_mode((win_width, win_height))
pg.display.set_caption('Falling Debris')

s_image = pg.image.load('./assets/images/ss.png')

font = pg.font.Font(None, 30)
speed = 10
score = 0
running = True
player_size = 50
player_pos = [win_width / 2, win_height - player_size]  # 400, 600-40
player_image = pg.image.load('./assets/images/shopping-cart.png')
player_image = pg.transform.scale(player_image, (player_size, player_size))  # 40,40

kirby_size = 60

screen.blit(s_image,(10,10))
kirby_data = []     # List to store kirbyrectss positions and their images
kirby = pg.image.load('./assets/images/Kirby-21.png')
kirby = pg.transform.scale(kirby, (kirby_size, kirby_size))

obj_size = 60
obj_data = []     # List to store kirbyrectss positions and their images
obj = pg.image.load('./assets/images/mushroom.png')
obj = pg.transform.scale(obj, (obj_size, obj_size))



bg_image = pg.image.load('./assets/images/NTUZ FATT.htm')
bg_image = pg.transform.scale(bg_image, (win_width, win_height))


def create_kirbyrects(kirby_data):
    if len(kirby_data) < 10 and random.random() < 0.1:    
        x = random.randint(0, win_width - kirby_size)
        y = 0                                         
        kirby_data.append([x, y, kirby])


def update_kirbyrects(kirby_data):
    global score

    for kirbyrects in kirby_data:
        x, y, image_data = kirbyrects
        if y < win_height:
            y += speed
            kirbyrects[1] = y
            screen.blit(image_data, (x, y))
        else:
            kirby_data.remove(kirbyrects)
            score += 1


def collision_check(kirby_data, player_pos):
    global running
    for kirbyrects in kirby_data:
        x, y, image_data = kirbyrects
        player_x, player_y = player_pos[0], player_pos[1]
        kirby_rect = pg.Rect(x, y, kirby_size, kirby_size)
        player_rect = pg.Rect(player_x, player_y, player_size, player_size)
        if player_rect.colliderect(kirby_rect):
            time.sleep(2)
            running = False
            break
        
def create_objrects(obj_data):
    if len(obj_data) < 10 and random.random() < 0.1:    
        x = random.randint(0, win_width - obj_size)
        y = 0                                         
        obj_data.append([x, y, obj])


def update_objrects(obj_data):
    global score

    for objrects in obj_data:
        x, y, image_data = objrects
        if y < win_height:
            y += speed
            objrects[1] = y
            screen.blit(image_data, (x, y))
        else:
            obj_data.remove(objrects)
            score += 1


def collision_check2(obj_data, player_pos):
    global running, score
    for objrects in obj_data:
        x, y, image_data = objrects
        player_x, player_y = player_pos[0], player_pos[1]
        obj_rect = pg.Rect(x, y, obj_size, obj_size)
        player_rect = pg.Rect(player_x, player_y, player_size, player_size)
        if player_rect.colliderect(obj_rect):
            #time.sleep(2)
            #running = False
            #break
            score += 1
            obj_data.remove(objrects)

async def main():
    global running, player_pos

    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False

            if event.type == pg.KEYDOWN:
                x, y = player_pos[0], player_pos[1]
                if event.key == pg.K_LEFT:
                    x -= 20
                elif event.key == pg.K_RIGHT:
                    x += 20
                player_pos = [x, y]

        screen.blit(s_image,(10,10))
        screen.blit(bg_image, (0, 0))
        screen.blit(player_image, (player_pos[0], player_pos[1]))

        text = f'Score: {score}'
        text = font.render(text, 10, black)
        screen.blit(text, (win_width - 200, win_height - 40))
        screen.blit(s_image,(10,10))


        create_kirbyrects(kirby_data)
        update_kirbyrects(kirby_data)
        collision_check(kirby_data, player_pos)

        create_objrects(obj_data)
        update_objrects(obj_data)
        collision_check2(obj_data, player_pos)
        
        collision_check(obj_data, player_pos)
        clock.tick(30)
        pg.display.flip()
        await asyncio.sleep(0)
    pg.quit()

asyncio.run(main())


