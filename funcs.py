from settings import *

def load_images_from_spritesheet(filename):
    #Tries to load the file
    try:
        spritesheet = pygame.image.load(filename)
    except:
        print('file not found...')
        return []

    images = []

    start_position = []
    dimensions = [None, None]

    for i in range(spritesheet.get_height()):
        for j in range(spritesheet.get_width()):
            r,g,b,a = spritesheet.get_at((j, i))
            r1,g1,b1 = colors['yellow']
            r2,g2,b2 = colors['pink']

            #If yellow pixil is found, the next pixil down and right is set to the starting position for image
            if r == r1 and g == g1 and b == b1:
                start_position = [j+1, i+1]

            #If pink pixil is found, one of the dimensions is set (width or height)
            if r == r2 and g == g2 and b == b2:
                if dimensions[0] == None:
                    dimensions[0] = j - start_position[0]
                else:
                    dimensions[1] = i - start_position[1]

                    #Renders the image from spritesheet onto another surface
                    image = pygame.Surface(dimensions)
                    image.set_colorkey(colors['black'])
                    image.blit(spritesheet, (start_position[0]-2, -start_position[1]))

                    #Adds the image to the images list
                    images.append(image)

                    #Clears the start position and the dimensions
                    start_position.clear()
                    dimensions = [None, None]

    #Returns all the found images
    return images
