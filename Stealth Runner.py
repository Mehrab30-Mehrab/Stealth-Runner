# stealth_runner_game.py
# Main game logic for "Stealth Runner"

import curses
import random
import time

# Constants
PLAYER_CHAR = "[1;32m@[0m"  # Green '@'
GUARD_CHAR = "[1;31mG[0m"   # Red 'G'
WALL_CHAR = "#"
FLOOR_CHAR = "."
VAULT_CHAR = "[1;34m$[0m"  # Blue '$'
FOG_CHAR = " "
MAP_WIDTH = 20
MAP_HEIGHT = 10

class Game:
    def __init__(self, stdscr):
        self.stdscr = stdscr
        self.player_pos = [1, 1]
        self.vault_pos = [MAP_WIDTH - 2, MAP_HEIGHT - 2]
        self.guard_pos = [MAP_WIDTH // 2, MAP_HEIGHT // 2]
        self.fog = True
        self.map = self.generate_map()
        self.running = True

    def generate_map(self):
        game_map = [[FLOOR_CHAR for _ in range(MAP_WIDTH)] for _ in range(MAP_HEIGHT)]
        for x in range(MAP_WIDTH):
            game_map[0][x] = WALL_CHAR
            game_map[MAP_HEIGHT - 1][x] = WALL_CHAR
        for y in range(MAP_HEIGHT):
            game_map[y][0] = WALL_CHAR
            game_map[y][MAP_WIDTH - 1] = WALL_CHAR
        game_map[self.vault_pos[1]][self.vault_pos[0]] = VAULT_CHAR
        return game_map

    def render(self):
        self.stdscr.clear()
        for y in range(MAP_HEIGHT):
            for x in range(MAP_WIDTH):
                if self.fog and abs(x - self.player_pos[0]) > 3 or abs(y - self.player_pos[1]) > 3:
                    char = FOG_CHAR
                else:
                    if [x, y] == self.player_pos:
                        char = PLAYER_CHAR
                    elif [x, y] == self.guard_pos:
                        char = GUARD_CHAR
                    else:
                        char = self.map[y][x]
                self.stdscr.addstr(y, x * 2, char)
        self.stdscr.refresh()

    def move_player(self, dx, dy):
        nx, ny = self.player_pos[0] + dx, self.player_pos[1] + dy
        if self.map[ny][nx] != WALL_CHAR:
            self.player_pos = [nx, ny]

    def move_guard(self):
        px, py = self.player_pos
        gx, gy = self.guard_pos
        dx = 1 if px > gx else -1 if px < gx else 0
        dy = 1 if py > gy else -1 if py < gy else 0
        nx, ny = gx + dx, gy + dy
        if self.map[ny][nx] != WALL_CHAR:
            self.guard_pos = [nx, ny]

    def check_game_over(self):
        if self.player_pos == self.guard_pos:
            return "Caught! Game Over."
        elif self.player_pos == self.vault_pos:
            return "Success! You stole the data!"
        return None

    def game_loop(self):
        self.stdscr.nodelay(True)
        while self.running:
            self.render()
            key = self.stdscr.getch()
            if key == curses.KEY_UP:
                self.move_player(0, -1)
            elif key == curses.KEY_DOWN:
                self.move_player(0, 1)
            elif key == curses.KEY_LEFT:
                self.move_player(-1, 0)
            elif key == curses.KEY_RIGHT:
                self.move_player(1, 0)
            elif key == ord("q"):
                self.running = False

            self.move_guard()
            status = self.check_game_over()
            if status:
                self.render()
                self.stdscr.addstr(MAP_HEIGHT + 1, 0, status)
                self.stdscr.refresh()
                time.sleep(3)
                self.running = False

            time.sleep(0.2)

def main(stdscr):
    curses.curs_set(0)
    game = Game(stdscr)
    game.game_loop()

if __name__ == "__main__":
    curses.wrapper(main)
