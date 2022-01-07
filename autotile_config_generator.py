import pygame, sys, json, tkinter
from tkinter import *
from tkinter import filedialog

# INITIAL_DIR = '/home/shubhendu/Documents/puttar/github-ssh/Level-Editor/data/autotile/8_bit_autotiling2.json'
INITIAL_DIR = '/home/shubhendu/Documents/puttar/godot/Action RPG/World/'

def get_open_filename():
    Tk().withdraw()
    filename = filedialog.askopenfilename(initialdir = INITIAL_DIR, defaultextension = '.png', filetypes = [('PNG', '*.png')])
    return filename

def get_save_filename():
    Tk().withdraw()
    filename = filedialog.asksaveasfilename(initialdir = INITIAL_DIR, defaultextension = '.json', filetypes = [('JSON', '*.json')])
    return filename

def add_tile_indicator(tile_indicators, position, tilesize, scale, scroll):
    original_tilesize_by_3 = original_tilesize/3
    new_position = [int(((position[0]+scroll[0])/scale)//original_tilesize_by_3*original_tilesize_by_3), int(((position[1]+scroll[1])/scale)//original_tilesize_by_3*original_tilesize_by_3)]

    if new_position not in tile_indicators:
        tile_indicators.append(new_position)

def remove_tile_indicator(tile_indicators, position, tilesize, scale, scroll):
    original_tilesize_by_3 = original_tilesize/3
    new_position = [int(((position[0]+scroll[0])/scale)//original_tilesize_by_3*original_tilesize_by_3), int(((position[1]+scroll[1])/scale)//original_tilesize_by_3*original_tilesize_by_3)]

    if new_position in tile_indicators:
        tile_indicators.remove(new_position)

def render_tile_indicators(screen, tile_indicators, tilesize, scale, scroll):
    surface = pygame.Surface(screen.get_size())
    surface.set_colorkey((0,0,0))
    for position in tile_indicators:
        pygame.draw.rect(surface, (255, 0, 0), (position[0]*scale-scroll[0], position[1]*scale-scroll[1], int(tilesize/3)+1, int(tilesize/3)+1))

    surface.set_alpha(128)
    screen.blit(surface, (0,0))

def render_lines(screen, tilesize, scale, scroll):
    surface = pygame.Surface(screen.get_size())
    surface.set_colorkey((0,0,0))

    for j in range(int(surface.get_width()/tilesize)):
        for i in range(int(surface.get_height()/tilesize)):
            pygame.draw.rect(surface, (0,0,255), (j*tilesize, i*tilesize, (j+1)*tilesize, (i+1)*tilesize), 1)

    surface.set_alpha(128)
    screen.blit(surface, (-scroll[0], -scroll[1]))

def save_data(tile_indicators, image, tilesize, scale):
    filename = get_save_filename()
    if filename == ():
        return

    tiles = {}
    for i in range(original_image.get_height()//original_tilesize):
        for j in range(original_image.get_width()//original_tilesize):
            tile_data = []
            for k in range(3):
                for l in range(3):
                    if k == 1 and l == 1:
                        continue
                    position = [(j*original_tilesize)+((original_tilesize//3)*k), (i*original_tilesize)+((original_tilesize//3)*l)]
                    if position in tile_indicators:
                        tile_data.append([k-1, l-1])
            tiles[(j, i)] = tile_data

    tile_data = {key:'00000000' for key in tiles.keys()}
    order = [[0,-1], [1,-1], [1,0], [1,1], [0,1], [-1,1], [-1,0], [-1,-1]]

    for tile in tile_data.keys():
        for i, direction in enumerate(order):
            if direction in tiles[tile]:
                tile_data[tile] = tile_data[tile][:i] + '1' + tile_data[tile][i+1:]

    new_data = {}

    for number in tile_data.values():
        position = list(tile_data.keys())[list(tile_data.values()).index(number)]
        index = position[0]+position[1]*original_image.get_width()//original_tilesize

        for i in range(len(number)):
            if i % 2 != 0:
                if number[i] == '0':
                    number = number[:i] + '2' + number[i+1:]
        new_data[number] = [index]

    json.dump(new_data, open(filename, 'w'), indent=4)

# scale = int(input('Pls enter the scale of the image to be loaded: '))
# original_tilesize = int(input('Pls enter the tilesize of the tileset: '))
scale = 3
original_tilesize = 16

screen = pygame.display.set_mode((1000, 700))
pygame.display.set_caption('Autotile Config Generator')

filename = get_open_filename()
original_image = pygame.image.load(filename)

scroll = [0,0]
scroll_vel = [0,0]

tile_indicators = []

mouse_states = {
    'left_held': False,
    'right_held': False
}

while True:
    tilesize = original_tilesize * scale
    image = pygame.transform.scale(original_image, (int(original_image.get_width()*scale), int(original_image.get_height()*scale)))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                scroll_vel[1] = -1
            if event.key == pygame.K_s:
                scroll_vel[1] = 1
            if event.key == pygame.K_a:
                scroll_vel[0] = -1
            if event.key == pygame.K_d:
                scroll_vel[0] = 1
            if event.key == pygame.K_SPACE:
                save_data(tile_indicators, image, tilesize, scale)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_w:
                scroll_vel[1] = 0
            if event.key == pygame.K_s:
                scroll_vel[1] = 0
            if event.key == pygame.K_a:
                scroll_vel[0] = 0
            if event.key == pygame.K_d:
                scroll_vel[0] = 0
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                mouse_states['left_held'] = True
            if event.button == 3:
                mouse_states['right_held'] = True
            if event.button == 4:
                scale += 0.1
            elif event.button == 5:
                scale -= 0.1
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                mouse_states['left_held'] = False
            if event.button == 3:
                mouse_states['right_held'] = False

    if mouse_states['left_held']:
        add_tile_indicator(tile_indicators, pygame.mouse.get_pos(), tilesize, scale, scroll)
    if mouse_states['right_held']:
        remove_tile_indicator(tile_indicators, pygame.mouse.get_pos(), tilesize, scale, scroll)

    scroll[0] += scroll_vel[0]
    scroll[1] += scroll_vel[1]

    screen.fill((0,0,0))

    screen.blit(image, (-scroll[0], -scroll[1]))
    render_tile_indicators(screen, tile_indicators, tilesize, scale, scroll)

    render_lines(screen, tilesize, scale, scroll)

    pygame.display.update()
