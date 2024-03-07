import pygame 
from pygame.locals import *


from service.minMax import MinMax
minmax = MinMax([[0 for _ in range(19)] for _ in range(19)])


pygame.init()

screen_width = 1200
screen_height = 750

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Gomoku")

#variables
line_width = 2
markers = []
clicked = False
pos = []
player = 2
font = pygame.font.Font(None, 36)  # Change the size as needed

#define colors
green = (0, 255, 0)
red = (255, 0, 0)

def check_win(board, player):
    for i in range(19):
        for j in range(19):
            if j < 15 and all(board[i][j+k] == player for k in range(5)):
                return True
            if i < 15 and all(board[i+k][j] == player for k in range(5)):
                return True
            if i < 15 and j < 15 and all(board[i+k][j+k] == player for k in range(5)):
                return True
            if i < 15 and j >= 4 and all(board[i+k][j-k] == player for k in range(5)):
                return True
    return False  # Return False if no win condition is found in the entire board

def draw_grid():
    # bg = (255, 255, 200)
    # grid = (50, 50, 50)
    # screen.fill(bg)
    # for i in range(0, 19):
    #     pygame.draw.line(screen, grid, (0, i*42), (screen_width, i*42), line_width)
    #     pygame.draw.line(screen, grid, (i*42, 0), (i*42, screen_height), line_width)
    
    bg = pygame.image.load(r"D:\UBB\a10-Annddu\Gomoku\images\backgroud.png")
    screen.blit(bg, (0, 0))
    
    cell_size = 35  # Size of each cell in pixels
    grid_size = 19  # Number of cells in the grid

    # Calculate the total width and height of the grid
    grid_width = cell_size * grid_size
    grid_height = cell_size * grid_size

    # Calculate the starting x and y coordinates for the grid
    start_x = (screen_width - grid_width) // 2
    start_y = (screen_height - grid_height) // 2

    # Draw the grid
    for i in range(grid_size + 1):
        pygame.draw.line(screen, (0, 0 ,0), (start_x, start_y + i * cell_size), (start_x + grid_width, start_y + i * cell_size), line_width)
        pygame.draw.line(screen, (0, 0 ,0), (start_x + i * cell_size, start_y), (start_x + i * cell_size, start_y + grid_height), line_width) 

for x in range(19):
    row = [0] * 19
    markers.append(row)
    
def get_inverted_board(markers):
    inverted_board = [[0 for _ in range(19)] for _ in range(19)]
    for i in range(19):
        for j in range(19):
            inverted_board[i][j] = markers[j][i]
    return inverted_board
    
def draw_markers(start_x, start_y):
    inverted_board = get_inverted_board(markers)
    x_pos = 0
    for x in inverted_board:
        y_pos = 0
        for y in x:
            if y == 1:
                pygame.draw.circle(screen, (255, 255, 255), (x_pos*35 + start_x + 18, y_pos*35 + start_y + 18), 15, 25)	
            if y == 2:
                pygame.draw.circle(screen, (0, 0, 0), (x_pos*35 + start_x + 18, y_pos*35 + start_y + 18), 15, 25)
            y_pos += 1
        x_pos += 1
  
start_x = (screen_width - 35*19) // 2
start_y = (screen_height - 35*19) // 2
                
run = True
while run:
    draw_grid()
    draw_markers(start_x, start_y)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN and clicked == False:  # If mouse button is pressed
            clicked = True
        if event.type == pygame.MOUSEBUTTONUP:  # If mouse button is released
            clicked = False
            pos = pygame.mouse.get_pos()
            if pos[0] >= start_x and pos[0] <= start_x + 35*19 and pos[1] >= start_y and pos[1] <= start_y + 35*19:
                cell_x = (pos[0] - start_x) // 35
                cell_y = (pos[1] -  start_y) // 35
                try:
                    if markers[cell_y][cell_x] == 0:
                        markers[cell_y][cell_x] = 2
                        minmax.__setitem__((cell_y, cell_x), 2)
                        player = 1
                        if minmax.check_win(2):
                            draw_markers(start_x, start_y)
                except IndexError:
                    pass
                    
        else:     
            if player == 1:
                y, x = minmax.min_max()
                minmax.__setitem__((y, x), 1)
                markers[y][x] = 1
                player = 2
                if minmax.check_win(1):
                    draw_markers(start_x, start_y)
                    text = font.render("Computer wins", True, (0, 0, 0))  # Change the color as needed
                    screen.blit(text, (10, 10))  # Change the position as needed
                    pygame.display.update()
                    run = False
                    
            
    
    pygame.display.update()

pygame.display.update()
pygame.time.wait(3000)

pygame.quit()
for i in range(19):
    print(markers[i])