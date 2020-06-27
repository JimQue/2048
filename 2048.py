import pygame
import random
#enable text
pygame.font.init()
myfont = pygame.font.SysFont('Comic Sans MS', 60)
#variables
gap = 100
width = 8 * gap
height = 8 * gap
win = pygame.display.set_mode((width, height))
#color
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
#board
board = [[0 for i in range(8)] for i in range(8)]



#tiles
class tile():
    def __init__(self, val, x, y):
        self.val = val
        self.x = x
        self.y = y
    
    def draw(self):
        pygame.draw.rect(win, red, (self.x, self.y, gap, gap))
        text_width, text_height = myfont.size(str(self.val))
        text = myfont.render(str(self.val), False, black)
        win.blit(text, ((self.x + (gap - text_width)//2),(self.y + (gap - text_height)//2)))



#generate random tile
def generate():
    value = random.choice([2, 4])
    x = random.randint(0, 7)
    y = random.randint(0, 7)
    if board[x][y] != 0:
        generate()
    else:
        board[y][x] = tile(value, x * gap, y * gap)

generate()
generate()
generate()
generate()
generate()
generate()
generate()
generate()


#check if row is empty
def isEmpty(row):
    for r in row:
        if r != 0:
            return False
    return True
    

#moving all tiles toward certain direction
def move(direction):
    #move to right
    if direction == 'r':
        for row in range(len(board)):
            while not isEmpty(board[row]) and board[row][-1] == 0:
                n = 7
                print(board)
                while n >= 0:
                    if board[row][n] != 0 and board[row][n+1] == 0:
                        
                        board[row][n].x += gap
                        board[row][n+1] = board[row][n]
                        board[row][n] = 0
                    n -= 1
            
            

                



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


#refresh window
def redraw():
    win.fill(white)
    grid()
    #draw all tiles on board
    for row in board:
        for t in row:
            if t != 0:
                t.draw()


#game loop
while True:
    pygame.time.Clock().tick(30)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                move('r')

    redraw()
    pygame.display.update()