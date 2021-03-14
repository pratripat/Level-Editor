import pygame
import json

#Initializing pygame and few parameters
pygame.init()

width = 1000
height = 700
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Level Editor')

clock = pygame.time.Clock()

res = 24

rows = height//res
cols = width//res

scroll = [0,0]

colors = json.load(open('data/graphics/colors.json', 'r'))

selection = {
    'image': None
}
