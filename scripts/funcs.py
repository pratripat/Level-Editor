import pygame, math, random
from pathlib import Path

def resolve_path(filepath):
    """
    Resolve a file path relative to the base directory of the project.
    :param filepath: The relative path to resolve.
    :return: The absolute path.
    """
    if not filepath:
        print('Resolve path was called with filepath=None')
        return ''
    
    base_dir = Path(__file__).parent.parent.resolve()  # Adjust to your project's root directory
    return base_dir / filepath

def load_images_from_tilemap(filename, tile_size=32, skip_empty=True):
    """
    Load tile images from a spritesheet, optionally skipping empty tiles.

    :param filepath: Path to the spritesheet image.
    :param tile_size: Width and height of each tile (assumes square tiles).
    :param skip_empty: Whether to skip fully transparent or empty tiles.
    :return: List of Pygame Surfaces, one per non-empty tile.
    """
    spritesheet = pygame.image.load(filename).convert()
    sheet_width, sheet_height = spritesheet.get_size()

    tiles = []
    for y in range(0, sheet_height, tile_size):
        for x in range(0, sheet_width, tile_size):
            tile = pygame.Surface((tile_size, tile_size))
            tile.set_colorkey((0,0,0))
            tile.blit(spritesheet, (0, 0), (x, y, tile_size, tile_size))

            if skip_empty:
                # Check if the tile is completely transparent
                if not pygame.mask.from_surface(tile).count():
                    continue

            tiles.append(tile)

    return tiles


def load_images_from_spritesheet(filename):
    #Tries to load the file
    try:
        spritesheet = pygame.image.load(filename).convert()
    except Exception as e:
        print('LOADING SPRITESHEET ERROR: ', e)
        return []

    rows = []
    images = []

    for y in range(spritesheet.get_height()):
        pixil = spritesheet.get_at((0, y))
        if pixil[2] == 255:
            rows.append(y)

    for row in rows:
        for x in range(spritesheet.get_width()):
            start_position = []
            pixil = spritesheet.get_at((x, row))
            if pixil[0] == 255 and pixil[1] == 255 and pixil[2] == 0:
                start_position = [x+1, row+1]
                width = height = 0

                for rel_x in range(start_position[0], spritesheet.get_width()):
                    pixil = spritesheet.get_at((rel_x, start_position[1]))
                    if pixil[0] == 255 and pixil[1] == 0 and pixil[2] == 255:
                        width = rel_x - start_position[0]
                        break

                for rel_y in range(start_position[1], spritesheet.get_height()):
                    pixil = spritesheet.get_at((start_position[0], rel_y))
                    if pixil[0] == 255 and pixil[1] == 0 and pixil[2] == 255:
                        height = rel_y - start_position[1]
                        break

                image = pygame.Surface((width, height))
                image.set_colorkey((0,0,0))
                image.blit(spritesheet, (-start_position[0], -start_position[1]))

                images.append(image)

    return images
