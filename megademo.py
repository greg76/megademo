import pyxel

# linear interpolation hurts my eyes, so here we go
def EaseIn(duration, current):
    if current <=0:
        return 0
    elif current >= duration:
        return 1
    else:
        deg = 270 + 90 * current / duration
        return pyxel.sin(deg) + 1

def EaseOut(duration, current):
    if current <=0:
        return 0
    elif current >= duration:
        return 1
    else:
        deg = 90 * current / duration
        return pyxel.sin(deg)

class DemoPart:
    TITLE_TEXT = None
    TITLE_COLOR = pyxel.COLOR_RED
    TITLE_SHADOW = pyxel.COLOR_BLACK
    TITLE_EASE = 15

    def __init__(self, duration=None):
        self.tick = 0
        self.duration = duration
        self.tock = None
        self.__finished__ = False

    def update(self):
        self.tick += 1

        # if there's a duration set for the part, we will also have a countdown version of the tick
        if self.duration:
            self.tock = self.duration - self.tick if self.tick <= self.duration else 0

            # the status will be set finished if the duration is met
            if self.tick >= self.duration:
                self.__finished__ = True

    def draw(self):

        # if theres a TITLE defined, let's ease it in-and-out
        if self.TITLE_TEXT:
            lines = self.TITLE_TEXT.split("\n")
            maxlen = max(len(line) for line in lines) * pyxel.FONT_WIDTH
            for i, line in enumerate(lines):
                w = len(line) * pyxel.FONT_WIDTH
                x = pyxel.width - w - 1 
                if self.tick <= self.TITLE_EASE:
                    x += maxlen * EaseIn(self.TITLE_EASE, self.TITLE_EASE - self.tick)
                elif self.duration and self.tock < self.TITLE_EASE:
                    x += maxlen * EaseIn(self.TITLE_EASE, self.TITLE_EASE - self.tock)
                y = i * pyxel.FONT_HEIGHT
                # put a thick shadow first, to ensure readability over any crazy background
                pyxel.text(x + 1, y + 1, line, self.TITLE_SHADOW)
                pyxel.text(x + 1, y + 0, line, self.TITLE_SHADOW)
                pyxel.text(x + 0, y + 1, line, self.TITLE_SHADOW)
                pyxel.text(x, y, line, self.TITLE_COLOR)

    def is_finished(self):
        return self.__finished__

class C64loader(DemoPart):

    BOARDER_WIDTH = 10

    def draw(self):
        if self.tick < 30:
            pyxel.cls(pyxel.COLOR_LIGHT_BLUE)
        else:
            for y in range(pyxel.height):
                pyxel.line(0, y, pyxel.width, y, pyxel.rndi(0, pyxel.NUM_COLORS-1))

        pyxel.rect(
            self.BOARDER_WIDTH, self.BOARDER_WIDTH,
            pyxel.width - self.BOARDER_WIDTH * 2, pyxel.height - self.BOARDER_WIDTH * 2,
            pyxel.COLOR_DARK_BLUE
        )

        pyxel.text(
            self.BOARDER_WIDTH + 1, self.BOARDER_WIDTH + 1,
            "READY.\nLOAD\"MEGADEMO\"\n\nSEARCHING FOR MEGADEMO\nLOADING\nREADY.\nRUN",
            pyxel.COLOR_LIGHT_BLUE)

class RasterBar(DemoPart):

    TITLE_TEXT = 'This is dedicated to\nCsico "raster bar" Laszlo'
    EASE_DURATION = 60

    # colors and width of lines that a single bar is composed of
    BAR = (
        (pyxel.COLOR_ORANGE, 1),
        (pyxel.COLOR_YELLOW, 2),
        (pyxel.COLOR_WHITE, 1),
        (pyxel.COLOR_YELLOW, 2),
        (pyxel.COLOR_ORANGE, 1)
    )

    def draw(self):
        pyxel.cls(pyxel.COLOR_BLACK)

        if self.tick < self.duration - self.EASE_DURATION:
            bar_height = pyxel.height * EaseIn(self.EASE_DURATION, self.tick)
        else:
            bar_height = pyxel.height * EaseIn(self.EASE_DURATION, self.tock)
        
        bar_start = pyxel.height - int(bar_height)

        for y in range(bar_start, pyxel.height):
            for i, streak in enumerate(self.BAR):
                for w in range(streak[1]):
                    x = pyxel.width // 2
                    x += pyxel.sin(self.tick * 4 + y*6) * 30
                    x += pyxel.sin(self.tick * 6 + 130 + y * 3) * 20
                    pyxel.line(x+i+w, y, x+i+w, pyxel.height, streak[0])

        super().draw()


class GuruMeditation(DemoPart):
    GURU_TEXT = ("Error. Press left mouse button", "GURU Meditation 2023.01")
    SCROLL_TEXT = "Just kidding! :) But you have to be old enough to get the joke..."
    DYCP_HEIGHT = 20
    SCROLL_DELAY = 90
    EASE_OUT_DURATION = 20
    STAR_SHADES = (pyxel.COLOR_NAVY, pyxel.COLOR_DARK_BLUE, pyxel.COLOR_LIGHT_BLUE)
    NO_OF_STARS = 100

    def __init__(self, duration=None):
        self.last_letter_x = None
        self.stars = list(
            (
                pyxel.rndi(0, pyxel.width - 1),
                pyxel.rndi(0, pyxel.height - 1),
                pyxel.rndi(1, len(self.STAR_SHADES))
            )
            for _ in range(self.NO_OF_STARS)
        )
        super().__init__(duration)

    def draw(self):
        pyxel.cls(pyxel.COLOR_BLACK)

        if self.tick > self.SCROLL_DELAY:
            for i, star in enumerate(self.stars):
                x, y, v = star

                if self.tick - self.SCROLL_DELAY < self.EASE_OUT_DURATION:
                    c = int((v - 1) * EaseIn(self.EASE_OUT_DURATION, self.tick - self.SCROLL_DELAY))
                else:
                    c = self.STAR_SHADES[v - 1]
                pyxel.pset(x, y, c)
                if x >= v:
                    x -= v
                    self.stars[i] = (x, y, v)
                elif self.last_letter_x is None or self.last_letter_x > pyxel.width:
                    x += pyxel.width
                    y = pyxel.rndi(0, pyxel.height - 1)
                    v = pyxel.rndi(1, len(self.STAR_SHADES))
                    self.stars[i] = (x, y, v)
                else:
                    del(self.stars[i])

            for i, letter in enumerate(self.SCROLL_TEXT):
                x = pyxel.width - self.tick + self.SCROLL_DELAY + i * pyxel.FONT_WIDTH

                # only draw the letter if any part of it is in the visible area
                if -pyxel.FONT_WIDTH < x < pyxel.width:
                    rot = (self.tick - i * 2) * 5
                    y = pyxel.height // 2 + self.DYCP_HEIGHT * pyxel.sin(rot)
                    # the first 2 color are fairly dark, let's use only rest of the 16 color palette
                    color = (self.tick + i) % 14 + 2
                    pyxel.text(x, y, letter, color)

                if i == len(self.SCROLL_TEXT) - 1:
                    self.last_letter_x = x                
                    if x <= -pyxel.FONT_WIDTH:
                        self.__finished__ = True

        if self.last_letter_x is not None and self.last_letter_x <= self.EASE_OUT_DURATION:
            current_delta = self.EASE_OUT_DURATION - self.last_letter_x
            box_y = int(-pyxel.FONT_HEIGHT * 3 * EaseIn(self.EASE_OUT_DURATION, current_delta))
        else:
            box_y = 0
        
        border_blink = self.tick // 15 % 2
        if border_blink == 0:
            pyxel.rectb(0, box_y, pyxel.width, pyxel.FONT_HEIGHT * 3, pyxel.COLOR_RED)

        for i, line in enumerate(self.GURU_TEXT):
            w = len(line) * pyxel.FONT_WIDTH
            x = (pyxel.width - w) // 2
            pyxel.text(
                x, box_y + 3 + i * pyxel.FONT_HEIGHT,
                line,
                pyxel.COLOR_RED
            )


class Interference(DemoPart):
    TITLE_TEXT = "Waves clash and intersect,\n" \
                 "Interference patterns form,\n" \
                 "Chaos in motion."
    GAP_SIZE = 3
    PART_DURATION = 200
    EASE_DURATION = 15
    SHADES = (
        pyxel.COLOR_NAVY,
        pyxel.COLOR_PURPLE,
        pyxel.COLOR_BROWN,
        pyxel.COLOR_ORANGE,
        pyxel.COLOR_YELLOW,
        pyxel.COLOR_WHITE
    )

    def __init__(self, duration=None):
        self.CIRCLES = pyxel.width // self.GAP_SIZE
        self.AMPLITUDE = pyxel.width // 4
        return super().__init__(duration)

    def draw(self):
        pyxel.cls(pyxel.COLOR_BLACK)

        if self.tick < self.EASE_DURATION:
            shade = len(self.SHADES) * self.tick // self.EASE_DURATION
            color = self.SHADES[shade]
        elif self.duration and self.tock < self.EASE_DURATION:
            shade = len(self.SHADES) * self.tock // self.EASE_DURATION
            color = self.SHADES[shade]
        else:
            color = pyxel.COLOR_WHITE

        centers = [
            (
                pyxel.width//2  + self.AMPLITUDE * pyxel.sin(self.tick * 3 * (i + 1) ),
                pyxel.height//2 - self.AMPLITUDE * pyxel.cos(self.tick * 2 * (i + 1) )
            )
            for i in range(2)
        ]

        for j,(x,y) in enumerate(centers):
            for i in range(self.CIRCLES, -1, -1):
                if i % 2 or i == 0:
                    pyxel.image(j).circ(x, y, i * self.GAP_SIZE, color)
                else:
                    pyxel.image(j).circ(x, y, i * self.GAP_SIZE, pyxel.COLOR_BLACK)
            pyxel.blt(0, 0, j, 0, 0, pyxel.width, pyxel.height, pyxel.COLOR_BLACK)

        super().draw()
        

class MandelBrot(DemoPart):
    EASE_DURATION = 60
    SIZE = 64
    SHADES = (
        (32,  pyxel.COLOR_NAVY),
        (48,  pyxel.COLOR_PURPLE),
        (96, pyxel.COLOR_RED),
        (255, pyxel.COLOR_ORANGE),
        (256, pyxel.COLOR_YELLOW),
    )
    TITLE_TEXT = "I have to confess\n" \
                 "Always faked voxel landscapes\n" \
                 "This time it's for real"

    def __init__(self, duration = None):
        # parameters for centering and precision of the mandelbrot
        max_iteration = 1000
        x_center =  -0.65
        y_center =  0.0

        # pre-calc the mandelbrot
        self.reference_data = []
        for i in range(self.SIZE):
            for j in range(self.SIZE):
                x = x_center + 2.8*float(i-self.SIZE/2)/self.SIZE
                y = y_center + 2.8*float(j-self.SIZE/2)/self.SIZE

                a,b = (0.0, 0.0)
                iteration = 0

                while (a**2 + b**2 <= 4.0 and iteration < max_iteration):
                    a,b = a**2 - b**2 + x, 2*a*b + y
                    iteration += 1
                if iteration == max_iteration:
                    value = 255
                else:
                    value = iteration*10 % 256

                self.reference_data.append((i, j, value))

        self.rotated_data = self.reference_data

        super().__init__(duration)

    def update(self):

        rot = self.tick % 360

        # create rotated copy of the mandelbrot set
        self.rotated_data = [
        (
            pyxel.cos(rot) * (x - self.SIZE // 2) - pyxel.sin(rot) * (y - self.SIZE // 2) + self.SIZE // 2,
            pyxel.sin(rot) * (x - self.SIZE // 2) + pyxel.cos(rot) * (y - self.SIZE // 2) + self.SIZE // 2,
            v
        )
        for x, y, v in self.reference_data    
        ]

        return super().update()

    def draw(self):
        pyxel.cls(pyxel.COLOR_BLACK)

        # ease in-out displacement
        if self.tick < self.EASE_DURATION:
            d = pyxel.height * (1 - EaseIn(self.EASE_DURATION, self.tick))
        elif self.duration and self.tock < self.EASE_DURATION:
            d = pyxel.height * (1 - EaseOut(self.EASE_DURATION, self.tock))
        else:
            d = 0

        # render voxel columns for each rotated point
        for x, y, value in sorted(self.rotated_data, key=lambda p: p[1]*500 + p[0], reverse=True):
            x *= 128 / self.SIZE
            y *= 128 / self.SIZE
            h = value // 4 + (y + d) // 2
            i, c = next((i, shade[1]) for i, shade in enumerate(self.SHADES) if shade[0] > value)
            highlight = self.SHADES[i + 1][1] if i < len(self.SHADES) - 1 else pyxel.COLOR_WHITE 
            pyxel.rect(x, pyxel.height - h + d * 2, 2,  h + d * 2, c)
            pyxel.rect(x, pyxel.height - h + d * 2, 2, 2, highlight)

        super().draw()

class Bouncy(DemoPart):
    PLATES = 16
    WAVE_LENGTH = 4
    SPEED = -6
    COLOR_SHADES = (
        (pyxel.COLOR_NAVY, pyxel.COLOR_DARK_BLUE, pyxel.COLOR_CYAN),
        (pyxel.COLOR_BROWN, pyxel.COLOR_ORANGE, pyxel.COLOR_YELLOW)
    )
    EASE_DURATION = 60
    TITLE_TEXT = "demoscene =\nsin() + cos()"

    def draw(self):
        pyxel.cls(pyxel.COLOR_BLACK)
        
        for i in range(self.PLATES):
            for j in range(self.PLATES):
                # distance of the current point from the center
                d = abs( (i - self.PLATES / 2)**2 + (j - self.PLATES / 2)**2 )
                # height/size of the plate is dependent on time and distance from center: we are sending waves from the middle
                h = pyxel.sin( d * self.WAVE_LENGTH + self.tick * self.SPEED)
                # normalise h, so 0 <= h <= 1
                h = (h + 1) / 2
                # gradually elevate up/down during phase in/out
                if self.tick < self.EASE_DURATION:
                    tmp = h - 1 + EaseIn(self.EASE_DURATION, self.tick)
                    h =  tmp if tmp > 0 else 0
                elif self.duration and self.tock < self.EASE_DURATION:
                    tmp = h - 1 + EaseIn(self.EASE_DURATION, self.tock)
                    h =  tmp if tmp > 0 else 0

                # distance between tiles
                spacing = pyxel.width / self.PLATES
                # width of a given tile
                w = int(spacing * h)
                # color is picked as if were a chess board
                color = self.COLOR_SHADES[(i + j) % 2]
                # shade is dependent on the height/size of the tile
                idx = int(len(color)*h)
                capped_idx =  idx if idx < len(color) else len(color)-1
                shade = color[capped_idx]
                # need to center the tiles that change size
                x = int( (i + 0.5) * spacing - w / 2 )
                y = int( (j + 0.5) * spacing - w / 2 )
                pyxel.rect(x, y, w, w, shade)

        super().draw()
        
class AmigaBall(DemoPart):
    
    TITLE_TEXT = "When I first saw an Amiga\nI was tripping balls!"

    class Object3D():

        class Face():
            def __init__(self, edges, color = None) -> None:
                self.edges = edges
                self.color = color

        RADIUS = 30
        LONGITUDES = 16
        LATITUDES = 7
        CAMERA_DISTANCE = 100

        def __init__(self):
            # vertex generation
            self.VERTICES_ORIG = [(0, -self.RADIUS, 0)]
            for j in range(self.LATITUDES):
                lat = (j+1) * 180 / (self.LATITUDES + 1)
                for i in range(self.LONGITUDES):
                    degree = i * 360 / self.LONGITUDES
                    x = self.RADIUS * pyxel.sin(degree) * pyxel.sin(lat)
                    y = - self.RADIUS * pyxel.cos(lat)
                    z = self.RADIUS * pyxel.cos(degree) * pyxel.sin(lat)
                    self.VERTICES_ORIG.append((x, y, z))
            self.VERTICES_ORIG.append((0, self.RADIUS, 0))

            # face generation
            self.FACES = []
            color_idx = 0
            for i in range(self.LONGITUDES):
                color = pyxel.COLOR_WHITE if color_idx % 2 else pyxel.COLOR_RED
                color_idx += 1
                if i < self.LONGITUDES - 1:
                    self.FACES.append(
                        self.Face((0, i+1, i+2), color),
                    )
                else:
                    self.FACES.append(
                        self.Face((0, i+1, 1), color)
                    )

            for j in range(self.LATITUDES - 1):
                color_idx += 1
                for i in range(self.LONGITUDES):
                    color = pyxel.COLOR_WHITE if color_idx % 2 else pyxel.COLOR_RED
                    color_idx += 1
                    if i < self.LONGITUDES - 1:
                        a = j * self.LONGITUDES + i + 1
                        b = j * self.LONGITUDES + i + 2
                        c = (j+1) * self.LONGITUDES + i + 1
                        d = (j+1) * self.LONGITUDES + i + 2
                    else:
                        a = j * self.LONGITUDES + i + 1
                        b = j * self.LONGITUDES + 1
                        c = (j+1) * self.LONGITUDES + i + 1
                        d = (j+1) * self.LONGITUDES + 1
                    self.FACES.append(self.Face((c, b, a), color))
                    self.FACES.append(self.Face((c, d, b), color))                        

            last_vertex = len(self.VERTICES_ORIG) - 1

            for i in range(self.LONGITUDES):
                color_idx += 1
                color = pyxel.COLOR_WHITE if color_idx % 2 else pyxel.COLOR_RED
                if i < self.LONGITUDES - 1:
                    self.FACES.append(
                        self.Face((last_vertex, last_vertex - i - 1, last_vertex - i - 2), color),
                    )
                else:
                    self.FACES.append(
                        self.Face((last_vertex, last_vertex - self.LONGITUDES, last_vertex - 1), color)
                    )

            self.alpha = 0
            self.beta = 0
            self.gamma = 15
            self.rotate()

        def update(self):
            self.beta += 360/10/10
            self.rotate()

        def rotate(self):
            # setting up rotation matrix https://en.wikipedia.org/wiki/Rotation_matrix
            rot = [
                [pyxel.cos(self.beta)*pyxel.cos(self.gamma), pyxel.sin(self.alpha)*pyxel.sin(self.beta)*pyxel.cos(self.gamma)-pyxel.cos(self.alpha)*pyxel.sin(self.gamma), pyxel.cos(self.alpha)*pyxel.sin(self.beta)*pyxel.cos(self.gamma)+pyxel.sin(self.alpha)*pyxel.sin(self.gamma)],
                [pyxel.cos(self.beta)*pyxel.sin(self.gamma), pyxel.sin(self.alpha)*pyxel.sin(self.beta)*pyxel.sin(self.gamma)+pyxel.cos(self.alpha)*pyxel.cos(self.gamma), pyxel.cos(self.alpha)*pyxel.sin(self.beta)*pyxel.sin(self.gamma)-pyxel.sin(self.alpha)*pyxel.cos(self.gamma)],
                [-pyxel.sin(self.beta), pyxel.sin(self.alpha)*pyxel.cos(self.beta), pyxel.cos(self.alpha)*pyxel.cos(self.beta)]
            ]
            # apply rotation matrix to get the current position of vertices
            self.vertices = tuple(
                (
                    sum([i*j for (i,j) in zip(vertex, rot[0])]),
                    sum([i*j for (i,j) in zip(vertex, rot[1])]),
                    sum([i*j for (i,j) in zip(vertex, rot[2])])
                )
                for vertex in self.VERTICES_ORIG
            )
            # calculate face normals
            self.normals = tuple(
                (
                    # V = P1-P0, W = P2-P0
                    # Nz = Vx*Wy-Vy*Wx = (p1x-p0x) * (p2y-p0y) - (p1y-p0y) * (p2x-p0x)
                    (self.vertices[face.edges[1]][0] - self.vertices[face.edges[0]][0]) * (self.vertices[face.edges[2]][1] - self.vertices[face.edges[0]][1]) -
                    (self.vertices[face.edges[1]][1] - self.vertices[face.edges[0]][1]) * (self.vertices[face.edges[2]][0] - self.vertices[face.edges[0]][0])
                )
                for face in self.FACES
            )
            
            # projection of 3d coordinates to 2d display plane https://en.wikipedia.org/wiki/3D_projection
            self.vertices2d = tuple(
                (
                    vertex[0] * self.CAMERA_DISTANCE / (vertex[2] + self.CAMERA_DISTANCE),
                    vertex[1] * self.CAMERA_DISTANCE / (vertex[2] + self.CAMERA_DISTANCE)
                )
                for vertex in self.vertices
            )

    def __init__(self, duration=None):
        self.BOUNCE_HEIGHT = pyxel.height // 2
        self.BOUNCE_SPEED = 3 * 360 / 300
        self.obj = self.Object3D()
        self.dx = -self.obj.RADIUS
        self.bounce_direction = 1
        super().__init__(duration)
    def update(self):
        self.obj.update()
        return super().update()
    
    def draw(self):
        pyxel.cls(pyxel.COLOR_BLACK)

        self.dx += self.bounce_direction
        if self.dx >= pyxel.width - self.obj.RADIUS:
            self.bounce_direction = -1
        if self.bounce_direction == -1 and self.dx < -self.obj.RADIUS:
            print(self.tick)

        dy = pyxel.height - self.BOUNCE_HEIGHT * abs(pyxel.sin(self.tick * self.BOUNCE_SPEED)) - self.obj.RADIUS

        # pyxel.circ(self.dx + 7, dy + 4, self.obj.RADIUS * 1.1, 1)

        for face, normal in zip(self.obj.FACES, self.obj.normals):
            if normal > 15: # there's something phishy here, should be compared to zero, so the given object face is looking towards the camera
                if face.color:
                    pyxel.tri(
                        self.obj.vertices2d[face.edges[0]][0] + self.dx,
                        self.obj.vertices2d[face.edges[0]][1] + dy,
                        self.obj.vertices2d[face.edges[1]][0] + self.dx,
                        self.obj.vertices2d[face.edges[1]][1] + dy,
                        self.obj.vertices2d[face.edges[2]][0] + self.dx,
                        self.obj.vertices2d[face.edges[2]][1] + dy,
                        face.color
                    )
                else:
                    pyxel.trib(
                        self.obj.vertices2d[face.edges[0]][0] + dx,
                        self.obj.vertices2d[face.edges[0]][1] + dy,
                        self.obj.vertices2d[face.edges[1]][0] + dx,
                        self.obj.vertices2d[face.edges[1]][1] + dy,
                        self.obj.vertices2d[face.edges[2]][0] + dx,
                        self.obj.vertices2d[face.edges[2]][1] + dy,
                        pyxel.COLOR_GRAY
                    )
        return super().draw()

class ShadeBobs(DemoPart):
    SHADES = (pyxel.COLOR_BLACK, pyxel.COLOR_NAVY, pyxel.COLOR_PURPLE, pyxel.COLOR_RED, pyxel.COLOR_ORANGE, pyxel.COLOR_YELLOW)
    MASK = (
        (0,0,0,1,1,1,0,0,0),
        (0,0,1,1,1,1,1,0,0),
        (0,1,1,1,1,1,1,1,0),
        (1,1,1,1,1,1,1,1,1),
        (1,1,1,1,1,1,1,1,1),
        (1,1,1,1,1,1,1,1,1),
        (0,1,1,1,1,1,1,1,0),
        (0,0,1,1,1,1,1,0,0),
        (0,0,0,1,1,1,0,0,0),
    )
    MASK_HEIGHT = len(MASK)
    MASK_WIDTH = len(MASK[0])
    NO_OF_BLOBS = 2
    TITLE_TEXT = "2xSin ShadeBobs,\nA Mesmerizing Effect,\nSimple Joys In Life."
    EASE_DURATION = 30

    def __init__(self, duration=None):
        pyxel.image(0).cls(pyxel.COLOR_BLACK)
        self.AMPLITUDE = pyxel.width // 5
        super().__init__(duration)

    def draw(self):
        coords = [
            (
                pyxel.width//2  + self.AMPLITUDE * pyxel.sin(self.tick * 4 * (i + 1)) + self.AMPLITUDE * pyxel.cos(self.tick * 5 * (i + 2)),
                pyxel.height//2 - self.AMPLITUDE * pyxel.cos(self.tick * 7 * (i + 2)) + self.AMPLITUDE * pyxel.sin(self.tick * 3 * (i + 1))
            )
            for i in range(self.NO_OF_BLOBS)
        ]

        # if we have multiple "bobs" we repeat the effect multiple times
        for x, y in coords:
            # per each bob, you will process the shading line by line
            for i, row in enumerate(self.MASK):
                # and you need to read and modify the color pixel-by-pixel
                for j, value in enumerate(row):
                    # calculate pixel coordinates
                    px = x + j - self.MASK_WIDTH // 2
                    py = y + i - self.MASK_HEIGHT // 2
                    # read current color
                    color = pyxel.pget(px, py)
                    # adjust shade based on the look-up table 
                    index = self.SHADES.index(color)
                    # if already reached lightest shade, cycle back to a dark one
                    index = index + value if index + value < len(self.SHADES) else 1
                    # we draw the shadebob in the image bank, not the frame buffer!
                    # this way we limit the amount of pixel level read/write operations we manually do
                    pyxel.image(0).pset(px, py, self.SHADES[index])

        # displacement when easying out the background
        d = pyxel.height * (1 - EaseOut(self.EASE_DURATION, self.tock)) if self.duration and self.tock < self.EASE_DURATION else 0
        pyxel.cls(pyxel.COLOR_BLACK)
        pyxel.blt(0,d,0,0,0,pyxel.width,pyxel.height)

        # text animation is handled by parent class
        super().draw()

class App:
    def __init__(self):
        pyxel.init(128, 128, title="megademo", display_scale=4)

        self.demo_parts = [
            C64loader(120),
            GuruMeditation(),
            ShadeBobs(240),
            RasterBar(240),
            Interference(240),
            Bouncy(240),
            AmigaBall(260),
            MandelBrot(),
        ]

        self.active_part = self.demo_parts.pop(0)

        pyxel.run(self.update, self.draw)

    def update(self):
        if self.active_part.is_finished():
            if len(self.demo_parts) > 0:
                self.active_part = self.demo_parts.pop(0)
            else:
                print("Eventually, every adventure comes to an end...")
                exit(0)

        self.active_part.update()

    def draw(self):
        self.active_part.draw()

App()