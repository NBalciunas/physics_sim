from abc import ABC, abstractmethod
import pygame
import time
import random
import re

VIEW_MODE = 0  # 0 - Regular, 1 - Temperature

SELECTED_MODEL = 1
AMOUNT_OF_MODELS = 8
MODEL_LENGTH = 17
PLACE_SIZE = 3

BUTTON_X = 140
BUTTON_Y = 40
BUTTON_X_SPACE = 20
BUTTON_Y_SPACE = 20
BUTTON_ROWS = 1

WIDTH = 10  # Single box width
HEIGHT = 10  # Single box height
MARGIN = 1
GRID_X = 50  # Amount of boxes in X axis
GRID_Y = 50  # Amount of boxes in Y axis
WIN_SIZE_X = WIDTH * GRID_X + MARGIN * (GRID_X + 1) + (BUTTON_X + 60) * BUTTON_ROWS
WIN_SIZE_Y = WIDTH * GRID_Y + MARGIN * (GRID_Y + 1)
WINDOW_SIZE = [WIN_SIZE_X, WIN_SIZE_Y]

pygame.init()

screen = pygame.display.set_mode(WINDOW_SIZE)
clock = pygame.time.Clock()


class Particle:
    def __init__(self, model=0):
        self.model = model
        file = open("models.txt", "r")
        models = file.readlines()
        file.close()
        for i in range(AMOUNT_OF_MODELS):
            if model == i:
                self.weight = int(models[2 + MODEL_LENGTH * i].strip())
                self.state = int(models[3 + MODEL_LENGTH * i].strip())
                self.viscosity = int(models[4 + MODEL_LENGTH * i].strip())
                color = []
                color_str = re.split(", ", (str(models[5 + MODEL_LENGTH * i])).strip())
                for j in color_str:
                    color.append(int(j))
                self.color = color
                self.harden_point = int(models[6 + MODEL_LENGTH * i].strip()) if models[
                                                                    6 + MODEL_LENGTH * i].strip() != "NaN" else None
                self.hardened_state = int(models[7 + MODEL_LENGTH * i].strip()) if models[
                                                                    7 + MODEL_LENGTH * i].strip() != "NaN" else None
                self.melting_point = int(models[8 + MODEL_LENGTH * i].strip()) if models[
                                                                    8 + MODEL_LENGTH * i].strip() != "NaN" else None
                self.melted_state = int(models[9 + MODEL_LENGTH * i].strip()) if models[
                                                                    9 + MODEL_LENGTH * i].strip() != "NaN" else None
                self.boiling_point = int(models[10 + MODEL_LENGTH * i].strip()) if models[
                                                                    10 + MODEL_LENGTH * i].strip() != "NaN" else None
                self.boiled_state = int(models[11 + MODEL_LENGTH * i].strip()) if models[
                                                                    11 + MODEL_LENGTH * i].strip() != "NaN" else None
                self.condensing_point = int(models[12 + MODEL_LENGTH * i].strip()) if models[
                                                                    12 + MODEL_LENGTH * i].strip() != "NaN" else None
                self.condensed_state = int(models[13 + MODEL_LENGTH * i].strip()) if models[
                                                                    13 + MODEL_LENGTH * i].strip() != "NaN" else None
                self.temperature = int(models[14 + MODEL_LENGTH * i].strip()) if models[
                                                                    14 + MODEL_LENGTH * i].strip() != "NaN" else None
                self.temperature_check = int(models[15 + MODEL_LENGTH * i].strip())

    def harden(self):
        self.model = self.hardened_state
        temp = self.temperature
        self.__init__(self.model)
        self.temperature = temp

    def melt(self):
        self.model = self.melted_state
        temp = self.temperature
        self.__init__(self.model)
        self.temperature = temp

    def evaporate(self):
        self.model = self.boiled_state
        temp = self.temperature
        self.__init__(self.model)
        self.temperature = temp

    def condense(self):
        self.model = self.condensed_state
        temp = self.temperature
        self.__init__(self.model)
        self.temperature = temp


class Manager(ABC):
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Manager, cls).__new__(cls)
        return cls._instance

    @abstractmethod
    def initialize(self):
        pass


class TemperatureColorManager(Manager):
    __TEMPERATURE_COLORS = []

    def initialize(self):
        file = open("temp_colors.txt", "r")
        color_file = file.readlines()
        file.close()
        for i in range(190):
            colors = []
            colors_str = re.split(", ", (str(color_file[i])).strip())
            for j in colors_str:
                colors.append(int(j))
            self.__TEMPERATURE_COLORS.append(colors)

    def color(self, temp):
        if temp is None:
            return None
        for i in range(190):
            if temp + 50 == i:
                return self.__TEMPERATURE_COLORS[i]


class GridManager(Manager):
    grid = []
    grid_size_x = GRID_X
    grid_size_y = GRID_Y

    def initialize(self):
        for row in range(self.grid_size_y):
            self.grid.append([])
            for column in range(self.grid_size_x):
                self.grid[row].append(Particle())

    def draw(self):
        color = (255, 255, 255)
        for row in range(self.grid_size_y):
            for column in range(self.grid_size_x):
                if VIEW_MODE == 0:
                    color = self.grid[row][column].color
                if VIEW_MODE == 1:
                    color = temp_color.color(self.grid[row][column].temperature)
                    if color is None and self.grid[row][column].state == 1:
                        color = (0, 0, 0)
                    if color is None and self.grid[row][column].state == 2:
                        color = (125, 125, 125)
                    elif color is None and self.grid[row][column].state == 0:
                        color = (255, 255, 255)
                pygame.draw.rect(screen, color,
                                 [(MARGIN + WIDTH) * column + MARGIN, (MARGIN + HEIGHT) * row + MARGIN, WIDTH, HEIGHT])


class Button:
    def __init__(self, x_coord, y_coord, x_length, y_length, text, text_color=(0, 0, 0), text_font=35):
        self._x_coord = x_coord
        self._y_coord = y_coord
        self._x_length = x_length
        self._y_length = y_length
        self._text = text
        self._text_color = text_color
        self._text_font = text_font

    def draw(self):
        pos = pygame.mouse.get_pos()
        text_style = pygame.font.SysFont('Corbel', self._text_font, True)
        text = text_style.render(self._text, True, self._text_color)

        if self._x_coord <= pos[0] <= (self._x_coord + self._x_length) and self._y_coord <= pos[1] <= (
                self._y_coord + self._y_length):
            pygame.draw.rect(screen, (170, 170, 170),
                             [self._x_coord, self._y_coord, self._x_length, self._y_length])
        else:
            pygame.draw.rect(screen, (100, 100, 100),
                             [self._x_coord, self._y_coord, self._x_length, self._y_length])

        screen.blit(text, ((self._x_coord + self._x_length / 8), (self._y_coord + self._y_length / 8)))

    def check_click(self):
        pos = pygame.mouse.get_pos()
        if self._x_coord <= pos[0] <= (self._x_coord + self._x_length) and self._y_coord <= pos[1] <= (
                self._y_coord + self._y_length):
            return True


class ButtonSmallText(Button):
    def __init__(self, x_coord, y_coord, x_length, y_length, text, text_color=(0, 0, 0), text_font=35, text_x_shift=0,
                 text_y_shift=0):
        super().__init__(x_coord, y_coord, x_length, y_length, text, text_color, text_font)
        self._x_coord = x_coord
        self._y_coord = y_coord
        self._x_length = x_length
        self._y_length = y_length
        self._text = text
        self._text_color = text_color
        self._text_font = text_font
        self.__text_x_shift = text_x_shift
        self.__text_y_shift = text_y_shift

    def draw(self):
        pos = pygame.mouse.get_pos()
        text_style = pygame.font.SysFont('Corbel', self._text_font, True)
        text = text_style.render(self._text, True, self._text_color)

        if self._x_coord <= pos[0] <= (self._x_coord + self._x_length) and self._y_coord <= pos[1] <= (
                self._y_coord + self._y_length):
            pygame.draw.rect(screen, (170, 170, 170),
                             [self._x_coord, self._y_coord, self._x_length, self._y_length])
        else:
            pygame.draw.rect(screen, (100, 100, 100),
                             [self._x_coord, self._y_coord, self._x_length, self._y_length])

        screen.blit(text, ((self._x_coord + self._x_length / 8 + self.__text_x_shift),
                           (self._y_coord + self._y_length / 8 + self.__text_y_shift)))


def log_time(func):
    def inner(*args, **kwargs):
        start = time.time()
        returned_value = func(*args, **kwargs)
        print("Finished in " + str(time.time() - start) + " seconds")
        return returned_value

    return inner


def update_screen():
    screen.fill((0, 0, 0))
    grid.draw()
    for i in range(AMOUNT_OF_MODELS):
        model_buttons[i].draw()
    for i in range(7):
        slider_buttons[i].draw()
    temp_button.draw()
    snapshot_save_button.draw()
    snapshot_load_button.draw()
    pygame.display.update()
    clock.tick(60)
    pygame.display.flip()


def particle_oob_check(x, y, grid_x_size=GRID_X, grid_y_size=GRID_Y):
    return not (x >= grid_x_size or x < 0 or y >= grid_y_size or y < 0)


def place_particle(row, column, size):
    k = size
    for i in range(size):
        for j in range(k - size, size + 1 - k):
            if particle_oob_check(row + i - size, column + j):
                grid.grid[row + i - size][column + j] = Particle(SELECTED_MODEL)
        k -= 1

    for i in range(-size, size + 1):
        if particle_oob_check(row, column + i):
            grid.grid[row][column + i] = Particle(SELECTED_MODEL)

    k = size
    for i in range(size):
        for j in range(k - size, size + 1 - k):
            if particle_oob_check(row - i + size, column + j):
                grid.grid[row - i + size][column + j] = Particle(SELECTED_MODEL)
        k -= 1


@log_time
def take_snapshot():
    f = open("snapshot.txt", "w")
    for i in range(GRID_X):
        for j in range(GRID_Y):
            f.write(str(grid.grid[i][j].model))
        f.write("\n")
    f.close()


@log_time
def load_snapshot():
    file = open("snapshot.txt", "r")
    for i in range(GRID_X):
        for j in range(GRID_Y):
            t = file.read(1)
            while t.strip() == '':
                t = file.read(1)
            grid.grid[i][j] = Particle(int(t))
    f.close()


def gravity(grid_pos_x, grid_pos_y):
    if 0 < (grid_pos_x + 1) < GRID_X and grid.grid[grid_pos_x][grid_pos_y].model != 7:
        if grid.grid[grid_pos_x][grid_pos_y].weight > grid.grid[grid_pos_x + 1][grid_pos_y].weight and \
                grid.grid[grid_pos_x + 1][
                    grid_pos_y].state != 1:
            temp = grid.grid[grid_pos_x + 1][grid_pos_y]
            grid.grid[grid_pos_x + 1][grid_pos_y] = grid.grid[grid_pos_x][grid_pos_y]
            grid.grid[grid_pos_x][grid_pos_y] = temp
            return True
    else:
        return False


def wind(grid_pos_x, grid_pos_y):
    if 0 < (grid_pos_y + 1) < GRID_Y and grid.grid[grid_pos_x][grid_pos_y].state != 1:
        if random.randint(0, grid.grid[grid_pos_x][grid_pos_y].viscosity) > 5:
            if random.randint(0, 1) != 1 and grid.grid[grid_pos_x][grid_pos_y + 1].state != 1 and particle_oob_check(
                    grid_pos_x, grid_pos_y + 1):
                temp = grid.grid[grid_pos_x][grid_pos_y + 1]
                grid.grid[grid_pos_x][grid_pos_y + 1] = grid.grid[grid_pos_x][grid_pos_y]
                grid.grid[grid_pos_x][grid_pos_y] = temp
                return True
            if random.randint(0, 1) == 1 and grid.grid[grid_pos_x][grid_pos_y - 1].state == 0 and particle_oob_check(
                    grid_pos_x, grid_pos_y - 1):
                temp = grid.grid[grid_pos_x][grid_pos_y - 1]
                grid.grid[grid_pos_x][grid_pos_y - 1] = grid.grid[grid_pos_x][grid_pos_y]
                grid.grid[grid_pos_x][grid_pos_y] = temp
                return True
    return False


def temperature(grid_pos_x, grid_pos_y):
    temp = grid.grid[grid_pos_x][grid_pos_y].temperature
    function_used = False

    if 0 < (grid_pos_y + 1) <= GRID_Y and grid.grid[grid_pos_x][grid_pos_y].temperature_check == 1:
        if particle_oob_check(grid_pos_x+1, grid_pos_y) and grid.grid[grid_pos_x+1][grid_pos_y].temperature_check == 1:
            temp_xp = grid.grid[grid_pos_x + 1][grid_pos_y].temperature
            if temp > temp_xp and random.randint(0, temp - temp_xp) > 5:
                grid.grid[grid_pos_x][grid_pos_y].temperature -= 1
                grid.grid[grid_pos_x + 1][grid_pos_y].temperature += 1
                function_used = True

        if particle_oob_check(grid_pos_x-1, grid_pos_y) and grid.grid[grid_pos_x-1][grid_pos_y].temperature_check == 1:
            temp_xm = grid.grid[grid_pos_x - 1][grid_pos_y].temperature
            if temp > temp_xm and random.randint(0, temp - temp_xm) > 5:
                grid.grid[grid_pos_x][grid_pos_y].temperature -= 1
                grid.grid[grid_pos_x - 1][grid_pos_y].temperature += 1
                function_used = True

        if particle_oob_check(grid_pos_x, grid_pos_y+1) and grid.grid[grid_pos_x][grid_pos_y+1].temperature_check == 1:
            temp_yp = grid.grid[grid_pos_x][grid_pos_y + 1].temperature
            if temp > temp_yp and random.randint(0, temp - temp_yp) > 5:
                grid.grid[grid_pos_x][grid_pos_y].temperature -= 1
                grid.grid[grid_pos_x][grid_pos_y + 1].temperature += 1
                function_used = True

        if particle_oob_check(grid_pos_x, grid_pos_y-1) and grid.grid[grid_pos_x][grid_pos_y-1].temperature_check == 1:
            temp_ym = grid.grid[grid_pos_x][grid_pos_y - 1].temperature
            if temp > temp_ym and random.randint(0, temp - temp_ym) > 5:
                grid.grid[grid_pos_x][grid_pos_y].temperature -= 1
                grid.grid[grid_pos_x][grid_pos_y - 1].temperature += 1
                function_used = True

    if function_used:
        return True
    else:
        return False


def change_of_state(grid_pos_x, grid_pos_y):
    if grid.grid[grid_pos_x][grid_pos_y].temperature is not None:
        if grid.grid[grid_pos_x][grid_pos_y].harden_point is not None and grid.grid[grid_pos_x][
            grid_pos_y].temperature < \
                grid.grid[grid_pos_x][grid_pos_y].harden_point and grid.grid[grid_pos_x][grid_pos_y].state == 2:
            grid.grid[grid_pos_x][grid_pos_y].harden()
            return True
        if grid.grid[grid_pos_x][grid_pos_y].melting_point is not None and grid.grid[grid_pos_x][
            grid_pos_y].temperature > \
                grid.grid[grid_pos_x][grid_pos_y].melting_point and grid.grid[grid_pos_x][grid_pos_y].state == 1:
            grid.grid[grid_pos_x][grid_pos_y].melt()
            return True
        if grid.grid[grid_pos_x][grid_pos_y].boiling_point is not None and grid.grid[grid_pos_x][
            grid_pos_y].temperature > \
                grid.grid[grid_pos_x][grid_pos_y].boiling_point and grid.grid[grid_pos_x][grid_pos_y].state == 2:
            grid.grid[grid_pos_x][grid_pos_y].evaporate()
            return True
        if grid.grid[grid_pos_x][grid_pos_y].condensing_point is not None and grid.grid[grid_pos_x][
            grid_pos_y].temperature < \
                grid.grid[grid_pos_x][grid_pos_y].condensing_point and grid.grid[grid_pos_x][grid_pos_y].state == 0:
            grid.grid[grid_pos_x][grid_pos_y].condense()
            return True
    return False


def run_checklist():
    check = False
    for row in range(GRID_Y):
        for column in range(GRID_X):
            if gravity(column, row):
                check = True
            if wind(column, row):
                check = True
            if temperature(column, row):
                check = True
            if change_of_state(column, row):
                check = True
    if check:
        update_screen()
        time.sleep(1 / 1000)


if __name__ == '__main__':
    f = open("models.txt", "r")
    models = f.readlines()
    f.close()
    model_buttons = []
    for i in range(AMOUNT_OF_MODELS):
        colors = []
        colors_str = re.split(", ", (str(models[5 + MODEL_LENGTH * i])).strip())
        for j in colors_str:
            colors.append(int(j))
        model_buttons.append(
            Button((WIN_SIZE_X - BUTTON_X - BUTTON_X_SPACE), (BUTTON_Y_SPACE + (BUTTON_Y + BUTTON_Y_SPACE / 2) * i),
                   BUTTON_X, BUTTON_Y, models[1 + MODEL_LENGTH * i].strip(), colors))

    slider_buttons = []
    for i in range(7):
        slider_buttons.append(
            Button((WIN_SIZE_X - BUTTON_X - 25 + i * 21), (WIN_SIZE_Y - 60), 15, 40, str(i + 1), (255, 255, 255), 20))

    temp_button = ButtonSmallText(WIN_SIZE_X - BUTTON_X - BUTTON_X_SPACE, WIN_SIZE_Y - 115, 60, BUTTON_Y, "Temp",
                                  (100, 250, 0), 20, text_y_shift=6)

    snapshot_save_button = ButtonSmallText(WIN_SIZE_X - BUTTON_X - BUTTON_X_SPACE + 70, WIN_SIZE_Y - 115, 20, BUTTON_Y,
                                           "S",
                                           (255, 255, 255), 20, text_y_shift=6)
    snapshot_load_button = ButtonSmallText(WIN_SIZE_X - BUTTON_X - BUTTON_X_SPACE + 100, WIN_SIZE_Y - 115, 20, BUTTON_Y,
                                           "L",
                                           (255, 255, 255), 20, text_y_shift=6)

    temp_color = TemperatureColorManager()
    temp_color.initialize()

    random.seed(time.time())

    pygame.display.set_caption("falling sand simulation")

    grid = GridManager()
    grid.initialize()

    done = False
    holding = False
    while not done:
        pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            elif event.type == pygame.MOUSEBUTTONUP:
                holding = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                holding = True
            if holding:
                for i in range(AMOUNT_OF_MODELS):
                    if model_buttons[i].check_click():
                        SELECTED_MODEL = i
                        holding = False

                for i in range(7):
                    if slider_buttons[i].check_click():
                        PLACE_SIZE = i

                if temp_button.check_click():
                    if VIEW_MODE == 0:
                        VIEW_MODE = 1
                    else:
                        VIEW_MODE = 0
                    holding = False

                if snapshot_save_button.check_click():
                    take_snapshot()
                    holding = False

                if snapshot_load_button.check_click():
                    load_snapshot()
                    holding = False

                column = pos[0] // (WIDTH + MARGIN)
                row = pos[1] // (HEIGHT + MARGIN)
                if row < GRID_X and column < GRID_Y:
                    place_particle(row, column, PLACE_SIZE)

        run_checklist()
        update_screen()

    pygame.quit()
