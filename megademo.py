import pyxel

def EaseIn(duration, current):
    if current <=0:
        return 0
    elif current >= duration:
        return 1
    else:
        deg = 270 + 90 * current / duration
        return pyxel.sin(deg) + 1

class DemoPart:
    def __init__(self, duration=None):
        self.tick = 0
        self.duration = duration
        self.__finished__ = False

    def update(self):
        self.tick += 1
        if self.duration and self.tick >= self.duration:
            self.__finished__ = True

    def draw(self):
        pass

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

    TEXT = 'This is dedicated to\nCsico "raster bar" Laszlo'
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
            text_x = pyxel.width * EaseIn(self.EASE_DURATION, self.tick) + 1 - pyxel.width
        else:
            countdown = self.duration - self.tick
            bar_height = pyxel.height * EaseIn(self.EASE_DURATION, countdown)
            text_x = pyxel.width * EaseIn(self.EASE_DURATION, countdown) + 1 - pyxel.width

        
        bar_start = pyxel.height - int(bar_height)

        for y in range(bar_start, pyxel.height):
            for i, streak in enumerate(self.BAR):
                for w in range(streak[1]):
                    x = pyxel.width // 2
                    x += pyxel.sin(self.tick * 4 + y*6) * 30
                    x += pyxel.sin(self.tick * 6 + 130 + y * 3) * 20
                    pyxel.line(x+i+w, y, x+i+w, pyxel.height, streak[0])

        pyxel.text(text_x, 1, self.TEXT, pyxel.COLOR_RED)


class GuruMeditation(DemoPart):
    GURU_TEXT = ("Error. Press left mouse button", "GURU Meditation 2023.01")
    SCROLL_TEXT = "Just kidding! :) But you have to be old enough to get the joke..."
    DYCP_HEIGHT = 20
    SCROLL_DELAY = 90
    EASE_OUT_DURATION = 20
    last_letter_x = None

    def draw(self):
        pyxel.cls(pyxel.COLOR_BLACK)

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

        if self.tick > self.SCROLL_DELAY:
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

class Interference(DemoPart):
    GAP_SIZE = 4
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

    def __init__(self):
        self.CIRCLES = pyxel.width // self.GAP_SIZE
        self.AMPLITUDE = pyxel.width // 6
        return super().__init__()

    def draw(self):
        pyxel.cls(pyxel.COLOR_BLACK)

        if self.tick < self.EASE_DURATION:
            shade = len(self.SHADES) * self.tick // self.EASE_DURATION
            color = self.SHADES[shade]
        elif self.duration and self.tick > self.duration - self.EASE_DURATION:
            countdown = self.duration - self.tick if self.tick <= self.duration else 0
            shade = len(self.SHADES) * countdown // self.EASE_DURATION
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

        for x,y in centers:
            for i in range(self.CIRCLES):
                pyxel.circb(x, y, i* self.GAP_SIZE, color)

        if self.tick >= self.PART_DURATION:
            self.__finished__ = False
        

class MandelBrot(DemoPart):
    def __init__(self):
        max_iteration = 1000
        x_center = -1.0
        y_center =  0.0
        size = 128

        self.data = []
        for i in range(size):
            row = []
            for j in range(size):
                x = x_center + 4.0*float(i-size/2)/size
                y = y_center + 4.0*float(j-size/2)/size

                a,b = (0.0, 0.0)
                iteration = 0

                while (a**2 + b**2 <= 4.0 and iteration < max_iteration):
                    a,b = a**2 - b**2 + x, 2*a*b + y
                    iteration += 1
                if iteration == max_iteration:
                    value = 255
                else:
                    value = iteration*10 % 256

                row.append(value)
            self.data.append(row)

        super().__init__()

    def draw(self):
        for x, column in enumerate(self.data):
            for y, value in enumerate(column):
                pyxel.pset(x,y, value // 16)

class App:
    def __init__(self):
        pyxel.init(128, 128, title="megademo", display_scale=4)

        self.demo_parts = [
            #MandelBrot(),
            C64loader(120),
            GuruMeditation(),
            RasterBar(240),
            Interference(),
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