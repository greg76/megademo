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
    def __init__(self):
        self.tick = 0
        self.__finished__ = False

    def update(self):
        self.tick += 1

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

        if self.tick >= 30 * 4:
            self.__finished__ = True

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

        bar_height = 7 * pyxel.height / 8 * EaseIn(self.EASE_DURATION, self.tick)
        bar_start = pyxel.height - int(bar_height)

        for y in range(bar_start, pyxel.height):
            for i, streak in enumerate(self.BAR):
                for w in range(streak[1]):
                    x = pyxel.width // 2
                    x += pyxel.sin(self.tick * 4 + y*6) * 30
                    x += pyxel.sin(self.tick * 6 + 130 + y * 3) * 20
                    pyxel.line(x+i+w, y, x+i+w, pyxel.height, streak[0])

        text_x = pyxel.width * EaseIn(self.EASE_DURATION, self.tick) + 1 - pyxel.width
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

class App:
    def __init__(self):
        pyxel.init(128, 128, title="megademo", display_scale=4)

        self.demo_parts = [
            C64loader(),
            GuruMeditation(),
            RasterBar(),
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