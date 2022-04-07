import sys

import random
import pygame
import math
from pygame.locals import *

pygame.init()

fps = 60
fpsClock = pygame.time.Clock()

width, height = 1000, 480

screen = pygame.display.set_mode((width, height))
top_screen = pygame.Surface((width, height/2))





global_x = 0
global_y = 0


resolution = 3
#colours
RED = (255, 0, 0)
class player:
    def __init__(self):
        self.speed = 10
        self.x = width/2
        self.y = height/2
        self.fov = 80
        self.direction = 0
p1 = player()
class object:
    def __init__(self, x, y, size_x, size_y):
        self.x = x
        self.y = y
        self.size_x = size_x
        self.size_y = size_y
        self.colour = (100, 100, 100)

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.size_x, self.size_y)
    def display(self):
        pygame.draw.rect(screen, self.colour, pygame.Rect(self.x + global_x, self.y + global_y, self.size_x, self.size_y))
class ray:
    def __init__(self, x, y, x_vel, y_vel):
        self.x = x
        self.y = y
        self.x_vel = x_vel
        self.y_vel = y_vel
        self.distance_x = 0
        self.distance_y = 0
        self.distance = 0

    def get_rect(self):
        return pygame.Rect(self.x, self.y, 10*resolution/5, 10*resolution/5)

    def display(self):
        pygame.draw.rect(screen, (255, 255, 0), pygame.Rect(self.x + global_x, self.y + global_y, 10*resolution/5, 10*resolution/5))




def create_level():
    global objects
    objects = []

    for x in range(5):
        objects.append(object(random.randint(0, 1000), random.randint(0, 1000), random.randint(100, 200), random.randint(100, 200)))

    for obj in objects.copy():
        if obj.x > p1.x + 100 or obj.x < p1.x - 300 or obj.y > p1.y + 100 or obj.y < p1.y - 280:
            pass
        else:
            objects.remove(obj)


    objects.append(object(0, 0, 1000, 100))
    objects.append(object(0, 0, 100, 1000))
    objects.append(object(0, 1000, 1100, 100))
    objects.append(object(1000, 0, 100, 1000))

def check_hitboxes(placex, placey):

    for obj in objects:
        if placex*-1 > obj.x - p1.x and placex*-1 < obj.x  + obj.size_x - p1.x and placey*-1 > obj.y - p1.y and placey*-1 < obj.y  + obj.size_y - p1.y:

            return False
    return True


def shoot_ray(direction, direct):
    global global_x
    global global_y
    distance_x = 0
    distance_y = 0




    direction -= 90
    direction = direction * math.pi/180
    r1 = ray(global_x * -1 + p1.x, global_y * -1 + p1.y, math.cos(direction) * 4*resolution, math.sin(direction) * 4*resolution)

    moved = True
    while moved == True:

        for obj in objects:
            if r1.get_rect().colliderect(obj.get_rect()):
                moved = False
                while r1.get_rect().colliderect(obj.get_rect()):
                    r1.x -= r1.x_vel * 0.01
                    r1.y -= r1.y_vel * 0.01
                    r1.distance_x -= r1.x_vel * 0.01
                    r1.distance_y -= r1.y_vel * 0.01
                r1.display()
        if moved == True:
            r1.x += r1.x_vel
            r1.y += r1.y_vel
            r1.distance_x += r1.x_vel
            r1.distance_y += r1.y_vel
    r1.distance = math.sqrt((r1.distance_x ** 2 + r1.distance_y ** 2))
    #r1.distance = r1.distance * math.cos(direction)
    rays.append(r1)






def get_input():
    global global_x
    global global_y


    keys_pressed = pygame.key.get_pressed()  # Gets all pressed keys

    direction = p1.direction * (math.pi/180)
    direction -= 180
    x_vel = math.cos(direction) * p1.speed
    y_vel = math.sin(direction) * p1.speed


    if keys_pressed[pygame.K_a] and keys_pressed[
        pygame.K_w]:  # these check if you are trying to move diagonally, and if so reduce your speed to normal (speed/1.41)
        global_x += p1.speed / 1.41
        global_y += p1.speed / 1.41
        if check_hitboxes(global_x, global_y) == False:
            global_x -= p1.speed / 1.41
            global_y -= p1.speed / 1.41
    elif keys_pressed[pygame.K_a] and keys_pressed[pygame.K_s]:  # A+S
        global_x += p1.speed / 1.41
        global_y -= p1.speed / 1.41
        if check_hitboxes(global_x, global_y) == False:
            global_x -= p1.speed / 1.41
            global_y += p1.speed / 1.41
    elif keys_pressed[pygame.K_w] and keys_pressed[pygame.K_d]:  # W+D
        global_x -= p1.speed / 1.41
        global_y += p1.speed / 1.41
        if check_hitboxes(global_x, global_y) == False:
            global_x += p1.speed / 1.41
            global_y -= p1.speed / 1.41
    elif keys_pressed[pygame.K_d] and keys_pressed[pygame.K_s]:  # D+S
        global_x -= p1.speed / 1.41
        global_y -= p1.speed / 1.41
        if check_hitboxes(global_x, global_y) == False:
            global_x += p1.speed / 1.41
            global_y += p1.speed / 1.41


    else:
        if keys_pressed[pygame.K_a]:  # movement for only one key pressed
            pass  # Move left
            if check_hitboxes(global_x, global_y) == False:
                pass

        if keys_pressed[pygame.K_d]:

            pass


            if check_hitboxes(global_x, global_y) == False:
                pass

        if keys_pressed[pygame.K_w]:
            global_y += y_vel
            global_x += x_vel

            if check_hitboxes(global_x, global_y) == False:
                global_y -= y_vel
                global_x -= x_vel



        if keys_pressed[pygame.K_s]:
            global_y -= y_vel
            global_x -= x_vel
            if check_hitboxes(global_x, global_y) == False:
                global_y += y_vel
                global_x += x_vel
    if keys_pressed[pygame.K_LEFT]:
        p1.direction -= 4
    if keys_pressed[pygame.K_RIGHT]:
        p1.direction += 4

def render_3d_world():

    global top_screen


    pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(0, height/2, width, 150))


    for x in range(255):
        pygame.draw.rect(screen, (x, x, x), pygame.Rect(0, height/2+80+x, width, 10))




    for i, ray in enumerate(rays):
        colour = 255 - ray.distance*0.6
        if colour < 0:
            colour = 0
        if colour > 255:
            colour = 255
        pygame.draw.rect(screen, (colour, colour, colour), pygame.Rect(((width/len(rays))*i), height/2, 12, height-ray.distance))
        pygame.draw.rect(top_screen, (colour, colour, colour), pygame.Rect(((width / len(rays))*i), 0, 12, ray.distance))

    top_screen = pygame.transform.flip(top_screen, False, True)
    for x in range(255):
        pygame.draw.rect(top_screen, (abs(x-255), abs(x-255), abs(x-255)), pygame.Rect(0, x/4, width, x/4))
    screen.blit(top_screen, (0, 0))




def display():
    global rays
    pygame.draw.rect(screen, RED, pygame.Rect(p1.x, p1.y, 5, 5))
    global direct
    for object in objects:


        object.display()
    #pygame.draw.polygon(screen, (255, 0, 0),
                        #points=[(p1.x, p1.y), (p1.direction + 360, 100), (p1.direction + 360 + p1.fov, 100)])
    rays = []
    total_rays = (round(p1.fov/resolution*5))
    print(total_rays)
    for i in range(total_rays):
        #spacing = ((i - (round(total_rays/2)))) * 0.1
        spacing = 0
        shoot_ray(p1.direction + i*resolution/5-spacing,0)

    render_3d_world()




create_level()
# Game loop.
while True:
    screen.fill((0, 0, 0))

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    get_input()

    display()
    # Update.

    # Draw.

    pygame.display.flip()
    fpsClock.tick(fps)
