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
#check if any tile has been moved to decide whether to generate new tile
moved = False
#list of tiles that collide
collision = []


#tiles
class tile():
    #moved_x , moved_y are position after moved
    def __init__(self, val, x, y, color):
        self.val = val
        self.x = x
        self.y = y
        self.moved_x = x
        self.moved_y = y
        self.color = color
        self.width = gap
        self.height = gap
        self.moved_val = val
    
    def draw(self):
        global moved, collide
        #moving animation
        if self.x < self.moved_x:
            self.x += gap//4
        if self.x > self.moved_x:
            self.x -= gap//4
        if self.y < self.moved_y:
            self.y += gap//4
        if self.y > self.moved_y:
            self.y -= gap//4
        #generate new tile after the moving is done
        if self.x == self.moved_x and self.y == self.moved_y:
            if self.val != self.moved_val:
                board[self.y//gap][self.x//gap].val = self.moved_val
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height))
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



#moving all tiles toward certain direction
def move(direction):
    global moved, collision
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
                                (board[row][i-1]).moved_x += gap
                                board[row][i] = board[row][i-1]
                                board[row][i-1] = 0
                                moved = True
                            #if colide with tile with same value
                            elif board[row][i].moved_val == board[row][i-1].moved_val:
                                (board[row][i-1]).moved_x += gap
                                collision.append(board[row][i-1])
                                board[row][i-1] = 0
                                board[row][i].moved_val = 2 * board[row][i].moved_val
                                moved = True
                                break
                            
                            
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
                                (board[row][i+1]).moved_x -= gap
                                board[row][i] = board[row][i+1]
                                board[row][i+1] = 0
                                moved = True
                            elif board[row][i].moved_val == board[row][i+1].moved_val:
                                (board[row][i+1]).moved_x -= gap
                                collision.append(board[row][i+1])
                                board[row][i+1] = 0
                                board[row][i].moved_val = 2 * board[row][i].moved_val
                                moved = True
                                break
                                
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
                            board[i+1][c].moved_y -= gap
                            board[i][c] = board[i+1][c]
                            board[i+1][c] = 0
                            moved = True
                        #if colide, add
                        elif board[i+1][c].moved_val == board[i][c].moved_val:
                            board[i+1][c].moved_y -= gap
                            collision.append(board[i+1][c])
                            board[i+1][c] = 0
                            board[i][c].moved_val = 2 * board[i][c].moved_val
                            moved = True
                            break
                           
                        i -= 1
    #move downward
    if direction == 'd':
       for c in range(4):
            row = 3
            while row >= 0:
                if board[row][c] != 0:
                    for i in range(row+1, 4):
                        if board[i][c] == 0:
                            board[i-1][c].moved_y += gap
                            board[i][c] = board[i-1][c]
                            board[i-1][c] = 0
                            moved = True
                        elif board[i][c].moved_val == board[i-1][c].moved_val:
                            board[i-1][c].moved_y += gap
                            collision.append(board[i-1][c])
                            board[i-1][c] = 0
                            board[i][c].moved_val = 2 * board[i][c].moved_val
                            moved = True
                            break
                row -= 1


            
#check if tiles have all been moved
def all_moved():
    global collision
    for row in board:
        for t in row:
            if t.x != t.moved_x or t.y != t.moved_y:
                return False
    for t in collision:
        if t.x != t.moved_x or t.y != t.moved_y:
                return False
    collision = []
    return True


#check if row is empty
def isEmpty(row):
    for r in row:
        if r != 0:
            return False
    return True
          



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
    global moved
    for t in collision:
        if t.moved_x != t.x or t.moved_y != t.y:
            t.draw()
    for row in board:
        for t in row:
            if t != 0:
                t.draw()
    #generate new tile after every tile is in place
    if moved and all_moved:
        moved = False
        generate()

#refresh window
def redraw():
    win.fill(white)
    draw_tiles()
    grid()


#game loop
while True:
    pygame.time.Clock().tick(60)
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