import pygame
import random
from collections import deque
from copy import deepcopy

class Game():
    def __init__(self):
        pygame.init()

        pygame.display.set_caption("TETRIS")
        pygame.display.set_icon(pygame.image.load("images/logo.png"))

        self.TILE = 45 # size of a tile in px
        self.W = 10 # width of the playing field in tiles
        self.H = 20 # height of the playing field in tiles
        self.RES = 750, 940
        self.GAME_RES = self.W * self.TILE, self.H * self.TILE 
        self.FPS = 120

        self.game_screen = pygame.Surface((self.GAME_RES))
        self.screen = pygame.display.set_mode(self.RES)
        self.backgound = pygame.image.load('images/background.png').convert()
        self.GRID = [(x * self.TILE, y * self.TILE, self.TILE, self.TILE) for x in range(self.W) for y in range(self.H)]
        self.FIELD = [[0 for i in range(self.W)] for j in range(self.H)]

         # Red, Orange, Yellow, Green, Cyan, Violet, Purple
        self.block_colors = [(255, 45, 45), (255, 100, 0), (255, 255, 0), (45, 255, 45), (0, 255, 255), (160, 50, 255), (255, 50, 255)]

        self.FONT = pygame.font.Font('fonts/font.ttf', 65)

        self.dx = 0
        self.dy = 0
        self.speed_y = 2
        self.boost_y = 1
        self.score = 0
        self.record = self.get_record()
        self.next_score = 1000

        self.block_list = deque(maxlen=4)
        for i in range(4):
            self.block_list.append(random.randint(0, 6))
            
        self.running = True

        self.spawnBlock()


    def spawnBlock(self):
        self.blocks_positions = [[(-1, 0), (-2, 0), (0, 0), (1, 0)], # I-Block
                            [(0, -1), (-1, -1), (-1, 0), (0, 0)], # O-Block
                            [(-1, 0), (-1, 1), (0, 0), (0, -1)], # Z-Block
                            [(0, 0), (-1, 0), (0, 1), (-1, -1)], # S-Block
                            [(0, 0), (0, -1), (0, 1), (-1, -1)], # L-Block
                            [(-1, 0), (-1, -1), (-1, 1), (0, -1)], # J-Block
                            [(0, 0), (0, -1), (0, 1), (-1, 0)]] # T-Block

        self.blocks = [[pygame.Rect(x + self.W // 2, y + 1, 1, 1) for x, y in block_pos] for block_pos in self.blocks_positions]
        self.blocks_next = [[pygame.Rect(x + self.W // 2, y + 1, 1, 1) for x, y in block_pos] for block_pos in self.blocks_positions]

        self.block_rect = pygame.Rect(0, 0, self.TILE - 2, self.TILE - 2)

        self.block_next_rect_1 = pygame.Rect(0, 0, self.TILE - 2, self.TILE - 2)
        self.block_next_rect_2 = pygame.Rect(0, 0, self.TILE - 2, self.TILE - 2)
        self.block_next_rect_3 = pygame.Rect(0, 0, self.TILE - 2, self.TILE - 2)

        self.block = (self.blocks[self.block_list[0]])

        self.block_next_1 = (self.blocks_next[self.block_list[1]])
        self.block_next_2 = (self.blocks_next[self.block_list[2]])
        self.block_next_3 = (self.blocks_next[self.block_list[3]])

    def checkBordersX(self, i):
        if min(self.block).x < 0 or max(self.block).x > self.W - 1 or self.FIELD[self.block[i].y][self.block[i].x]:
            return False
        return True


    def checkBordersY(self):
        for i in range(4):
            if self.block[i].y >= self.H - 1 or self.FIELD[self.block[i].y+1][self.block[i].x]:
                return False
        return True


    def MoveBlocks(self):
        # Falling speed
        self.dy += ((self.speed_y/120)*self.boost_y)

        # Move X
        self.block_old = deepcopy(self.block)
        for i in range(4):
            self.block[i].x += self.dx
            if not self.checkBordersX(i):
                self.block = deepcopy(self.block_old)
                break
        self.dx = 0

        # Move Y
        if int(self.dy) >= 1:
            if self.checkBordersY():
                for i in range(4):
                    self.block[i].y += 1
            else:
                self.putOnField()
                self.score += 20
                self.boost_y = 1
            self.dy = 0

        # Draw
        for i in range(4):
            self.block_rect.x = self.block[i].x * self.TILE
            self.block_rect.y = self.block[i].y * self.TILE
            pygame.draw.rect(self.game_screen, (self.block_colors[self.block_list[0]]), self.block_rect)


    def speedUp(self):
        if self.score >= self.next_score:
            self.speed_y += 1
            self.next_score += 1000


    def rotateBlock(self):
        center = self.block[0]
        self.block_old = deepcopy(self.block)
        for i in range(4):
            x = self.block[i].y - center.y
            y = self.block[i].x - center.x
            self.block[i].x = center.x - x
            self.block[i].y = center.y + y
            if not self.checkBordersX(i):
                self.block = deepcopy(self.block_old)
                break


    def nextBlock(self):
        # 1
        for i in range(4):
            self.block_next_rect_1.x = self.block_next_1[i].x * self.TILE + 380
            self.block_next_rect_1.y = self.block_next_1[i].y * self.TILE + 85
            pygame.draw.rect(self.screen, (self.block_colors[self.block_list[1]]), self.block_next_rect_1)
        # 2
        for i in range(4):
            self.block_next_rect_2.x = self.block_next_2[i].x * self.TILE + 380
            self.block_next_rect_2.y = self.block_next_2[i].y * self.TILE + 285
            pygame.draw.rect(self.screen, (self.block_colors[self.block_list[2]]), self.block_next_rect_2)
        # 3
        for i in range(4):
            self.block_next_rect_3.x = self.block_next_3[i].x * self.TILE + 380
            self.block_next_rect_3.y = self.block_next_3[i].y * self.TILE + 485
            pygame.draw.rect(self.screen, (self.block_colors[self.block_list[3]]), self.block_next_rect_3)


    def userInput(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                break

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                    break
                elif event.key == pygame.K_UP:
                    self.rotateBlock()
                elif event.key == pygame.K_LEFT:
                    self.dx = -1
                elif event.key == pygame.K_RIGHT:
                    self.dx = 1
                elif event.key == pygame.K_DOWN:
                    self.boost_y = 20
                elif event.key == pygame.K_SPACE:
                    self.boost_y = 500

            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_DOWN:
                    self.boost_y = 1


    def removeLines(self):
        line = self.H - 1
        for row in range(self.H - 1, -1, -1):
            count = 0
            for i in range(self.W):
                if self.FIELD[row][i]:
                    count += 1
                self.FIELD[line][i] = self.FIELD[row][i]
            if count < self.W:
                line -= 1
            else:
                self.score += 100


    def putOnField(self):
        self.block_old = self.block
        for i in range(4):
            self.FIELD[self.block_old[i].y][self.block_old[i].x] = self.block_colors[self.block_list[0]]
        self.block_list.append(random.randint(0, 6))
        self.spawnBlock()


    def DrawField(self):
        for y, raw in enumerate(self.FIELD):
            for x, col in enumerate(raw):
                self.block_rect.x, self.block_rect.y = x * self.TILE, y * self.TILE
                pygame.draw.rect(self.game_screen, col, self.block_rect)
    
    def GameOver(self):
        for i in range(self.W):
            if self.FIELD[0][i]:
                self.running = False

    def get_record(self):
        try:
            with open('record') as f:
                return f.readline()
        except FileNotFoundError:
            with open('record', 'w') as f:
                f.write('0')


    def set_record(self):
        if self.score > int(self.record):
            with open('record', 'w') as f:
                f.write(str(self.score))
        self.record = self.get_record()


    def render(self):
        self.screen.blit(self.backgound, (0, 0))
        self.screen.blit(self.game_screen, (20, 20))
        # Draw grid
        [pygame.draw.rect(self.game_screen,(40,40,40),i_rect,1) for i_rect in self.GRID]

        self.screen.blit(self.FONT.render("Level:", True, pygame.Color('purple')), (500, 620))
        self.screen.blit(self.FONT.render(str(1), True, pygame.Color('white')), (500, 670))

        self.screen.blit(self.FONT.render("Score:", True, pygame.Color('purple')), (500, 720))
        self.screen.blit(self.FONT.render(str(self.score), True, pygame.Color('white')), (500, 770))

        self.screen.blit(self.FONT.render("Record:", True, pygame.Color('purple')), (500, 820))
        self.screen.blit(self.FONT.render(str(self.record), True, pygame.Color('white')), (500, 870))

        self.DrawField()
        self.userInput()
        self.MoveBlocks()
        self.removeLines()
        self.speedUp()
        self.nextBlock()
        self.set_record()
        self.GameOver()
        pygame.display.update()


    def run(self):    
        while self.running:
            self.render()
            pygame.time.Clock().tick(self.FPS)


game = Game()
game.run()
