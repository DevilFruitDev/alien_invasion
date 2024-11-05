# utilities/utils.py
import pygame

def check_collision(sprite1, sprite2):
    return pygame.sprite.collide_rect(sprite1, sprite2)

def group_collide(group1, group2):
    return pygame.sprite.groupcollide(group1, group2, True, True)
