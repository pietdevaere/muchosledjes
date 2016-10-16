from displaytools import *
import random
import curses
from curses import wrapper
from collections import deque, Iterator
import time

f = Font('ledFont')
d = Display('10.23.5.143')

moves = {'r': (1, 0), 'l': (-1, 0), 'u': (0, -1), 'd': (0, 1)}

x_size = d.leds_on_row
y_size = d.lines * d.rows

def vector_to_string(vector):
    result = ''
    for el in vector:
        result += (str(el))
    return result

def array_to_strings(array):
    result = []
    for el in array:
        result.append(vector_to_string(el))
    return result

class Snake(object):
    def __init__(self, game, length, relative_keys):
        self.g = game
        self.direction = 'r'
        self.step = moves[self.direction]
        self.blocks = deque([(game.x//2 - length//2, game.y//4)])
        self.relative_keys = relative_keys
        for i in range(length - 1):
            self.eat()

    def __repr__(self):
        return str(self.blocks)

    def __len__(self):
        return len(self.blocks)

    def __iter__(self):
        return self.blocks.__iter__()
    
    def set_relative_keys(self, value):
        self.relative_keys = value

    def change_direction(self, direction):
        if self.relative_keys:
            if direction in ('u', 'd'):
                return
            if self.direction == 'r':
                if direction == 'r':
                    self.direction = 'd'
                elif direction == 'l':
                    self.direction = 'u'
            elif self.direction == 'l':
                if direction == 'r':
                    self.direction = 'u'
                elif direction == 'l':
                    self.direction = 'd'
            elif self.direction == 'u':
                if direction == 'r':
                    self.direction = 'r'
                elif direction == 'l':
                    self.direction = 'l'
            elif self.direction == 'd':
                if direction == 'r':
                    self.direction = 'l'
                elif direction == 'l':
                    self.direction = 'r'
        else:
            if self.direction == 'r':
                if direction in ('r', 'l'):
                    return
                else:
                    self.direction = direction
            elif self.direction == 'l':
                if direction in ('r', 'l'):
                    return
                else:
                    self.direction = direction
            elif self.direction == 'u':
                if direction in ('u', 'd'):
                    return 
                else:
                    self.direction = direction
            elif self.direction == 'd':
                if direction in ('u', 'd'):
                    return
                else:
                    self.direction = direction
        self.step = moves[self.direction]

    def on_snake(self, coordinates):
        for block in self.blocks:
            if block == coordinates:
                return True
        return False

    def collision(self):
        head = self.blocks[0]
        for i in range(1, len(self.blocks)):
            if head == self.blocks[i]:
                return True
        return False

    def move(self):
        new_x, new_y = self.blocks[0]
        new_x += self.step[0]
        new_y += self.step[1]
        self.blocks.appendleft((new_x, new_y))
        self.blocks.pop()

    def eat(self):
        new_x, new_y = self.blocks[0]
        new_x += self.step[0]
        new_y += self.step[1]
        self.blocks.appendleft((new_x, new_y))

    def head(self):
        return self.blocks[0]

class Game(object):
    def __init__(self, x, y, speed = 0.1, relative_keys = True):
        self.x = x
        self.y = y
        self.snake = Snake(self, 5, relative_keys)
        self.place_food()
        self.speed = speed

    def __repr__(self):
        strings = array_to_strings(self.array())
        result = ''
        for string in strings:
            result += string + '\n'
        result = result.replace('1', chr(9608))
        result = result.replace('0', 'x')
        return result

    def place_food(self):
        food_x = random.randrange(self.x)
        food_y = random.randrange(self.y)
        self.food = (food_x, food_y)
        if self.food in self.snake:
            self.place_food()

    def array(self):
        array = [[ 0 for x in range(self.x)] for y in range(self.y)]
        for block in self.snake:
            array[block[1]][block[0]] = '1'
        array[self.food[1]][self.food[0]] = '1'
        return array

    def increase_speed(self, delta = 0.95):
        self.speed *= delta

    def wait(self):
        if self.snake.direction in ('u', 'd'):
            time.sleep(self.speed * 2)
        else:
            time.sleep(self.speed)

    def take_step(self):
        if self.snake.head() == self.food:
            self.snake.eat()
            self.place_food()
            self.increase_speed()
        else: self.snake.move()
        return not self.dead()

    def dead(self):
        head_x, head_y = self.snake.head()
        if head_x >= self.x: return True
        if head_x < 0: return True
        if head_y >= self.y: return True
        if head_y < 0: return True
        if self.snake.collision(): return True
        return False

    def change_direction(self, direction):
        self.snake.change_direction(direction)

def main(screen):
    curses.curs_set(0)
    d.clear()
    StaticRow(d, f, 'Welcome to Snake').load(0)
    while True:
        screen.addstr(10, 10, 'Press space to start')
        StaticRow(d, f, 'PRESS SPACE').show(1)
        screen.nodelay(False)
        while True:
            char = screen.getch()
            if char == ord(' '):
                break
        
        screen.nodelay(True)
        myGame = Game(x_size, y_size, relative_keys = False)

        while True:
            char = screen.getch()
            if char == ord('q'): exit()
            elif char == curses.KEY_RIGHT:
                myGame.change_direction('r')
            elif char == curses.KEY_LEFT:
                myGame.change_direction('l')
            elif char == curses.KEY_UP:
                myGame.change_direction('u')
            elif char == curses.KEY_DOWN:
                myGame.change_direction('d')
            
            if not myGame.take_step():
                screen.clear()
                screen.addstr(9,10, 'GAME OVER')
                screen.refresh()
                StaticRow(d, f, 'GAME OVER').show(0)
                break
            d.load_array(myGame.array())
            d.update()
            screen.addstr(0, 0, str(myGame))
            screen.addstr(16, 0, 'speed is now {}'.format(myGame.speed))
            screen.addstr(17, 0, 'Direction is now {}'.format(myGame.snake.direction))
            screen.addstr(18, 0, 'Step is now {}'.format(myGame.snake.step))
            screen.refresh()
            myGame.wait()

wrapper(main)
