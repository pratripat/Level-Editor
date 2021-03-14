from settings import *
import json

class Image:
    def __init__(self, j, i, x, y):
        self.i = i
        self.j = j
        self.position = [x, y]
        self.image = selection['image'].image
        self.id = selection['image'].id
        self.index = selection['image'].index

        try:
            self.autotile_config = json.load(open(selection['image'].autotile_config_path, 'r'))
        except:
            self.autotile_config = None

    def show(self, surface=screen):
        #Renders the image according to the scroll
        surface.blit(self.image, [self.position[0]-scroll[0], self.position[1]-scroll[1]])

    def fill(self, images, depth=950):
        if depth == 0:
            return

        for dir in [(0,-1), (1,0), (0,1), (-1,0)]:
            i, j = self.i+dir[1], self.j+dir[0]

            if i-scroll[1]//res >= 0 and i-scroll[1]//res < rows+1 and j-scroll[0]//res >= 0 and j-scroll[0]//res < cols+1:
                neighbor = self.get_image_with_index(i, j, images)

                #If the neighbor is not yet defined, the neighbor becomes an image object and is put into the images list
                if not neighbor:
                    neighbor = Image(j, i, j*res, i*res)
                    images.append(neighbor)
                    neighbor.fill(images, depth-1)

    def autotile(self, images, selector_panel_images):
        if self.autotile_config:
            neighbors = self.get_neighbors(images)

            binary = '0000'

            #Sets binary according to the neighbors around the image
            for neighbor in neighbors:
                if neighbor and neighbor.id == self.id:
                    binary += '1'
                else:
                    binary += '0'

            #Gets the image according to the binary and the configuration file
            key = str(int(binary, 2))
            index = self.autotile_config[key]
            self.image = selector_panel_images[index].image
            self.index = index

    def get_neighbors(self, images):
        #Returns neighbor images
        neighbors = []

        for dir in [(0,-1), (1,0), (0,1), (-1,0)]:
            i, j = self.i+dir[1], self.j+dir[0]
            if i-scroll[1]//res >= 0 and i-scroll[1]//res < rows+1 and j-scroll[0]//res >= 0 and j-scroll[0]//res < cols+1:
                neighbor = self.get_image_with_index(i, j, images)
                neighbors.append(neighbor)

        return neighbors

    def get_image_with_index(self, i, j, images):
        #Returns image with the same given index (i, j)
        for image in images:
            if image.i == i and image.j == j:
                return image

        return None

    def within(self, starting, ending):
        #Returns image if it is within the rectangle dimension
        sx, sy = starting[0]+scroll[0], starting[1]+scroll[1]
        ex, ey = ending[0]+scroll[0], ending[1]+scroll[1]

        return (
            self.position[0] > sx and
            self.position[1] > sy and
            self.position[0]+self.get_width() < ex and
            self.position[1]+self.get_height() < ey
        )

    def get_width(self):
        #Returns image width
        return self.image.get_width()

    def get_height(self):
        #Returns image height
        return self.image.get_height()
