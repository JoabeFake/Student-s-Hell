import pygame

keys = None

def update():
    global keys

    keys = pygame.key.get_pressed()

def isDown(key):
    return keys[key]