import pygame
import random
#enable text
pygame.font.init()
myfont = pygame.font.SysFont('Comic Sans MS', 60)
#variables
gap = 100
width = 4 * gap
height = 4 * gap
win = pygame.display.set_mode((width, height))
#color
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
#board
board = [[0 for i in range(4)] for i in range(4)]



#tiles
class tile():
    def __init__(self, val, x, y, color):
        self.val = val
        self.x = x
        self.y = y
        self.color = color
    
    def draw(self):
        pygame.draw.rect(win, red, (self.x, self.y, gap, gap))
        text_width, text_height = myfont.size(str(self.val))
        text = myfont.render(str(self.val), False, black)
        win.blit(text, ((self.x + (gap - text_width)//2),(self.y + (gap - text_height)//2)))



#generate random tile
def generate(value = 0):
    if value == 0:
        value = random.choice([2,4])
    x = random.randint(0, 3)
    y = random.randint(0, 3)
    if board[y][x] != 0:
        generate()
    else:
        board[y][x] = tile(value, x * gap, y * gap, red)

generate(2)
generate(2)



#check if row is empty
def isEmpty(row):
    for r in row:
        if r != 0:
            return False
    return True
    

#moving all tiles toward certain direction
def move(direction):
    #check if any tile is moved to decide whether to generate new tile
    moved = False
    #move to right
    if direction == 'r':
        for row in range(len(board)):
            if not isEmpty(board[row]):
                n = 3
                while n >= 0:
                    if board[row][n] != 0:
                        for i in range(n+1, 4):
                            #if right is empty
                            if board[row][i] == 0:
                                (board[row][i-1]).x += gap
                                board[row][i] = board[row][i-1]
                                board[row][i-1] = 0
                                moved = True
                            #if colide with tile with same value
                            elif board[row][i].val == board[row][i-1].val:
                                board[row][i-1] = 0
                                board[row][i].val = board[row][i].val * 2
                                board[row][i].color = green
                                print('draw')
                                board[row][i].draw()
                                board[row][i].color = red
                                moved = True
                            
                    n -= 1
    #move to left
    if direction == 'l':
        for row in range(len(board)):
            if not isEmpty(board[row]):
                for n in range(4):
                    if board[row][n] != 0:
                        i = n - 1
                        while i >= 0:
                            if board[row][i] == 0:
                                (board[row][i+1]).x -= gap
                                board[row][i] = board[row][i+1]
                                board[row][i+1] = 0
                                moved = True
                            elif board[row][i].val == board[row][i+1].val:
                                board[row][i+1] = 0
                                board[row][i].val = board[row][i].val * 2
                                moved = True
                            i -= 1

    #move upward
    if direction == 'u':
        for c in range(4):
            for row in range(4):
                if board[row][c] != 0:
                    i = row - 1
                    while i >= 0:
                        #if empty, move
                        if board[i][c] == 0:
                            board[i+1][c].y -= gap
                            board[i][c] = board[i+1][c]
                            board[i+1][c] = 0
                            moved = True
                        #if colide, add
                        elif board[i+1][c].val == board[i][c].val:
                            board[i+1][c] = 0
                            board[i][c].val = board[i][c].val * 2
                            moved = True
                        i -= 1
    #move downward
    if direction == 'd':
       for c in range(4):
            row = 3
            while row >= 0:
                if board[row][c] != 0:
                    for i in range(row+1, 4):
                        if board[i][c] == 0:
                            board[i-1][c].y += gap
                            board[i][c] = board[i-1][c]
                            board[i-1][c] = 0
                            moved = True
                        elif board[i][c].val == board[i-1][c].val:
                            board[i-1][c] = 0
                            board[i][c].val = board[i][c].val * 2
                            moved = True
                row -= 1

    #generate new tile after move
    if moved:
        generate()



            
            

                



#drawing grids
def grid():
    x = 0
    y = 0
    while x <= width:
        pygame.draw.line(win, black, (x, 0), (x, height))
        x += gap
    while y <= height:
        pygame.draw.line(win, black, (0, y), (width, y))
        y += gap

#drawing all tiles on board
def draw_tiles():
    #draw all tiles on board
    for row in board:
        for t in row:
            if t != 0:
                t.draw()

#refresh window
def redraw():
    win.fill(white)
    draw_tiles()
    grid()


#game loop
while True:
    pygame.time.Clock().tick(30)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                move('r')
            if event.key == pygame.K_LEFT:
                move('l')
            if event.key == pygame.K_UP:
                move('u')
            if event.key == pygame.K_DOWN:
                move('d')

    redraw()
    pygame.display.update()