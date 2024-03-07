import pygame
from sys import exit
from pygame.sprite import Group
from service.minMax import MinMax
minmax = MinMax([[0 for _ in range(19)] for _ in range(19)])

def get_font(size): # Returns Press-Start-2P in the desired size
    return pygame.font.Font(r"D:\UBB\a10-Annddu\Gomoku\images\font.ttf", size)

class Button():
	def __init__(self, image, pos, text_input, font, base_color, hovering_color):
		self.image = image
		self.x_pos = pos[0]
		self.y_pos = pos[1]
		self.font = font
		self.base_color, self.hovering_color = base_color, hovering_color
		self.text_input = text_input
		self.text = self.font.render(self.text_input, True, self.base_color)
		if self.image is None:
			self.image = self.text
		self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
		self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))

	def update(self, screen):
		if self.image is not None:
			screen.blit(self.image, self.rect)
		screen.blit(self.text, self.text_rect)

	def checkForInput(self, position):
		if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
			return True
		return False

	def changeColor(self, position):
		if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
			self.text = self.font.render(self.text_input, True, self.hovering_color)
		else:
			self.text = self.font.render(self.text_input, True, self.base_color)

class Title(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__()
        self.sprites = []
        self.sprites.append(pygame.image.load(r"D:\UBB\a10-Annddu\Gomoku\images\title1.png"))
        self.image = self.sprites[0]
        self.rect = self.image.get_rect()
        self.rect.center = [pos_x, pos_y]
        self.target_pos = [1200 // 2, 800 // 2 -99]  # replace with actual screen dimensions
        self.speed = 0.5  # adjust to desired speed

    #make update fade in
    def update(self):
        dx = self.target_pos[0] - self.rect.centerx
        dy = self.target_pos[1] - self.rect.centery
        distance = (dx**2 + dy**2)**0.4
        if distance > self.speed:
            direction_x = dx / distance
            direction_y = dy / distance
            self.rect.centerx += self.speed * direction_x
            self.rect.centery += self.speed * direction_y
        
class Mesaj(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, andu):
        super().__init__()
        self.sprites = []
        self.sprites.append(pygame.image.load(r"D:\UBB\a10-Annddu\Gomoku\images\mesaj.png"))
        self.image = self.sprites[0]
        self.rect = self.image.get_rect()
        self.rect.bottomleft = [pos_x, pos_y]
        self.andu = andu
    
    def update(self):
        if self.andu.rect.x == 100:
            self.image = self.sprites[0]
        else:
            self.image = pygame.Surface((0,0))
                 
class Andu(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__()
        self.sprites = []
        self.sprites.append(pygame.image.load(r"D:\UBB\a10-Annddu\Gomoku\images\stanga1.png"))
        self.sprites.append(pygame.image.load(r"D:\UBB\a10-Annddu\Gomoku\images\stanga3.png"))
        self.sprites.append(pygame.image.load(r"D:\UBB\a10-Annddu\Gomoku\images\stanga2.png"))
        self.sprites.append(pygame.image.load(r"D:\UBB\a10-Annddu\Gomoku\images\stanga3.png"))
        self.sprites.append(pygame.image.load(r"D:\UBB\a10-Annddu\Gomoku\images\fata.png"))
        self.current_sprite = 0
        self.image = self.sprites[self.current_sprite]
        
        self.rect = self.image.get_rect()
        self.rect.bottomleft = [pos_x, pos_y]
        self.pause_until = 0

    def update(self):
        if self.rect.x != 100:
            self.current_sprite += 0.05
            
            if self.current_sprite >= len(self.sprites) - 1:
                self.current_sprite = 0
            
            self.image = self.sprites[int(self.current_sprite)]
        else:
            if pygame.time.get_ticks() > self.pause_until:
                self.image = self.sprites[4] 
                self.pause_until = pygame.time.get_ticks() + 3500
        
    def update_position(self, x, y):
        self.rect.topleft = [x, y]

    def move_left(self, speed):
        if pygame.time.get_ticks() > self.pause_until:
            self.rect.x -= speed
        
        if self.rect.x < -128:
            self.pause_until = pygame.time.get_ticks() + 3500
            self.rect.x = 1200
    
pygame.init()
pygame.mixer.init()
music = pygame.mixer.music.load(r"D:\UBB\a10-Annddu\Gomoku\images\bcmusic.mp3")
win = pygame.mixer.Sound(r"D:\UBB\a10-Annddu\Gomoku\images\win.mp3")
lose = pygame.mixer.Sound(r"D:\UBB\a10-Annddu\Gomoku\images\lose.mp3")
board = pygame.mixer.Sound(r"D:\UBB\a10-Annddu\Gomoku\images\board.mp3")
enter = pygame.mixer.Sound(r"D:\UBB\a10-Annddu\Gomoku\images\pew.mp3")
back = pygame.mixer.Sound(r"D:\UBB\a10-Annddu\Gomoku\images\fart.mp3")
pygame.mixer.music.set_volume(0.2)
pygame.mixer.music.play(-1)

screen_width = 1200
screen_height = 750
screen = pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption("Pixel")
clock = pygame.time.Clock()

andu_left_one = pygame.image.load(r"D:\UBB\a10-Annddu\Gomoku\images\stanga1.png").convert_alpha()
andu_left_two = pygame.image.load(r"D:\UBB\a10-Annddu\Gomoku\images\stanga2.png").convert_alpha()
background = pygame.image.load(r"D:\UBB\a10-Annddu\Gomoku\images\backgroud.png").convert_alpha()
title_image = pygame.image.load(r"D:\UBB\a10-Annddu\Gomoku\images\title1.png").convert_alpha()

x_andu = 1200
y_andu = 750
moving_andu = pygame.sprite.Group()
andu = Andu(x_andu, y_andu)
moving_andu.add(andu)

x_title = 600
y_title = 0
moving_title = pygame.sprite.Group()
title = Title(x_title, y_title)
moving_title.add(title)

x_mesaj = 200
y_mesaj = 640
moving_mesaj = pygame.sprite.Group()
mesaj = Mesaj(x_mesaj, y_mesaj, andu)
moving_mesaj.add(mesaj)

speed = 4
    
def fade(width, height):
    fade_surface = pygame.Surface((width, height))
    fade_surface.fill((0,0,0))
    for alpha in range(0, 255):
        fade_surface.set_alpha(alpha)
        screen.blit(fade_surface, (0,0))
        pygame.display.update()
        pygame.time.delay(4) 
        
def fade_in(width, height, background, buttons):
    fade_surface = pygame.Surface((width, height))
    fade_surface.fill((0,0,0))
    for alpha in range(255, -1, -1):  # Start from 255 and go down to 0
        fade_surface.set_alpha(alpha)
        screen.blit(background, (0,0))
        for button in buttons:
            button.update(screen)
        screen.blit(fade_surface, (0,0))
        pygame.display.update()
        pygame.time.delay(-400)

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

def draw_grid():
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
                pygame.draw.circle(screen, "#008080", (x_pos*35 + start_x + 18, y_pos*35 + start_y + 18), 15, 25)	
            if y == 2:
                pygame.draw.circle(screen, (0, 0, 0), (x_pos*35 + start_x + 18, y_pos*35 + start_y + 18), 15, 25)
            y_pos += 1
        x_pos += 1
  
def get_winning_markers():
    inverted_board = get_inverted_board(markers)
    winning_markers = []
    for i in range(19):
        for j in range(19):
            if j < 15 and all(inverted_board[i][j+k] == 1 for k in range(5)):
                winning_markers.append([(i, j+k) for k in range(5)])
                winner = 1
            if i < 15 and all(inverted_board[i+k][j] == 1 for k in range(5)):
                winning_markers.append([(i+k, j) for k in range(5)])
                winner = 1
            if i < 15 and j < 15 and all(inverted_board[i+k][j+k] == 1 for k in range(5)):
                winning_markers.append([(i+k, j+k) for k in range(5)])
                winner = 1
            if i < 15 and j >= 4 and all(inverted_board[i+k][j-k] == 1 for k in range(5)):
                winning_markers.append([(i+k, j-k) for k in range(5)])
                winner = 1
    for i in range(19):
        for j in range(19):
            if j < 15 and all(inverted_board[i][j+k] == 2 for k in range(5)):
                winning_markers.append([(i, j+k) for k in range(5)])
                winner = 2
            if i < 15 and all(inverted_board[i+k][j] == 2 for k in range(5)):
                winning_markers.append([(i+k, j) for k in range(5)])
                winner = 2
            if i < 15 and j < 15 and all(inverted_board[i+k][j+k] == 2 for k in range(5)):
                winning_markers.append([(i+k, j+k) for k in range(5)])
                winner = 2
            if i < 15 and j >= 4 and all(inverted_board[i+k][j-k] == 2 for k in range(5)):
                winning_markers.append([(i+k, j-k) for k in range(5)])
                winner = 2
    print(winning_markers)
    return winning_markers, winner
    
def highlight_winning_markers(start_x, start_y):
    winning_markers ,winner = get_winning_markers()
    for marker in winning_markers:
        for x, y in marker:
            if winner == 1:
                pygame.draw.circle(screen, red, (x*35 + start_x + 18, y*35 + start_y + 18), 15, 3)
            else:
                pygame.draw.circle(screen, green, (x*35 + start_x + 18, y*35 + start_y + 18), 15, 3)

start_x = (screen_width - 35*19) // 2
start_y = (screen_height - 35*19) // 2

def reset():
    for x in range(19):
        for y in range(19):
            markers[x][y] = 0
    minmax.reset()

def ckeck_if_full():
    for x in range(19):
        for y in range(19):
            if markers[x][y] == 0:
                return False
    return True

def play(difficulty, easy_win_player, easy_win_computer, medium_win_player, medium_win_computer, hard_win_player, hard_win_computer):
    fade_in(1200, 750, background, [])
    clicked = False  
    player = 2        
    run = True
    moves = 0
    while run:
            
        draw_grid()
        draw_markers(start_x, start_y)
        if difficulty == 1:
            wins = font.render("EASY - Player wins: " + str(easy_win_player) + " - AI wins: " + str(easy_win_computer), True, (0, 0, 0))
            screen.blit(wins, (10, 10))
        elif difficulty == 2:
            wins = font.render("MEDIUM - Player wins: " + str(medium_win_player) + " - AI wins: " + str(medium_win_computer), True, (0, 0, 0))
            screen.blit(wins, (10, 10))
        elif difficulty == 3:
            wins = font.render("HARD - Player wins: " + str(hard_win_player) + " - AI wins: " + str(hard_win_computer), True, (0, 0, 0))
            screen.blit(wins, (10, 10))
        
        if moves == 19*19:
            outline_color = (0, 0, 0)  # Black
            text_color = "#FFFF00"
            text_position = (555, 10)

            # Render the black outline
            for x in range(-3, 4):
                for y in range(-3, 4):
                    outline = font.render("Draw", True, outline_color)
                    screen.blit(outline, (text_position[0] + x, text_position[1] + y))

            # Render the main text
            text = font.render("Draw", True, text_color)
            screen.blit(text, text_position)
            run = False
        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                if event.type == pygame.MOUSEBUTTONDOWN and clicked == False:  # If mouse button is pressed
                    clicked = True
                if event.type == pygame.MOUSEBUTTONUP and clicked == True:  # If mouse button is released
                    clicked = False
                    pos = pygame.mouse.get_pos()
                    if pos[0] >= start_x and pos[0] <= start_x + 35*19 and pos[1] >= start_y and pos[1] <= start_y + 35*19:
                        cell_x = (pos[0] - start_x) // 35
                        cell_y = (pos[1] -  start_y) // 35
                        try:
                            if markers[cell_y][cell_x] == 0:
                                markers[cell_y][cell_x] = 2
                                minmax.__setitem__((cell_y, cell_x), 2)
                                moves += 1
                                pygame.mixer.Sound.play(board)
                                player = 1
                                if minmax.check_win(2):
                                    if difficulty == 1:
                                        easy_win_player += 1
                                    elif difficulty == 2:
                                        medium_win_player += 1
                                    elif difficulty == 3:
                                        hard_win_player += 1
                                    draw_markers(start_x, start_y)
                                    highlight_winning_markers(start_x, start_y)
                                    outline_color = (0, 0, 0)  # Black
                                    text_color = (0, 255, 0)  # Green
                                    text_position = (555, 10)

                                    # Render the black outline
                                    for x in range(-3, 4):
                                        for y in range(-3, 4):
                                            outline = font.render("You win", True, outline_color)
                                            screen.blit(outline, (text_position[0] + x, text_position[1] + y))

                                    # Render the main text
                                    text = font.render("You win", True, text_color)
                                    screen.blit(text, text_position)
                                    pygame.display.update()
                                    pygame.mixer.Sound.play(win)
                                    run = False
                        except IndexError:
                            pass
                            
                else:     
                    if player == 1:
                        y, x = minmax.min_max()
                        minmax.__setitem__((y, x), 1)
                        moves += 1
                        pygame.mixer.Sound.play(board)
                        markers[y][x] = 1
                        player = 2
                        if minmax.check_win(1):
                            if difficulty == 1:
                                easy_win_computer += 1
                            elif difficulty == 2:
                                medium_win_computer += 1
                            elif difficulty == 3:
                                hard_win_computer += 1
                            draw_markers(start_x, start_y)
                            highlight_winning_markers(start_x, start_y)
                            outline_color = (0, 0, 0)  # Black
                            text_color = red
                            text_position = (555, 10)

                            # Render the black outline
                            for x in range(-3, 4):
                                for y in range(-3, 4):
                                    outline = font.render("AI wins", True, outline_color)
                                    screen.blit(outline, (text_position[0] + x, text_position[1] + y))

                            # Render the main text
                            text = font.render("AI wins", True, text_color)
                            screen.blit(text, text_position)
                            pygame.display.update()
                            pygame.mixer.Sound.play(lose)
                            run = False
        pygame.display.update()
    pygame.time.delay(5000)
    reset()
    return easy_win_player, easy_win_computer, medium_win_player, medium_win_computer, hard_win_player, hard_win_computer
    
def play_options(easy_win_player, easy_win_computer, medium_win_player, medium_win_computer, hard_win_player, hard_win_computer):
    menu_moouse_pos = pygame.mouse.get_pos()
    
    EASY_BUTTON = Button(image=pygame.image.load(r"D:\UBB\a10-Annddu\Gomoku\images\play.png"), pos=(600, 404), 
                        text_input="EASY", font=get_font(55), base_color="Black", hovering_color="#00BE13")
    MEDIUM_BUTTON = Button(image=pygame.image.load(r"D:\UBB\a10-Annddu\Gomoku\images\play.png"), pos=(600, 484), 
                        text_input="MEDIUM", font=get_font(55), base_color="Black", hovering_color="#BE8E00")
    HARD_BUTTON = Button(image=pygame.image.load(r"D:\UBB\a10-Annddu\Gomoku\images\play.png"), pos=(600, 564), 
                        text_input="HARD", font=get_font(55), base_color="Black", hovering_color="#BE0000")
    BACK_BUTTON = Button(image=pygame.image.load(r"D:\UBB\a10-Annddu\Gomoku\images\play.png"), pos=(600, 644), 
                        text_input="BACK", font=get_font(55), base_color="Black", hovering_color="#C54949")
    
    buttons = [EASY_BUTTON, MEDIUM_BUTTON, HARD_BUTTON, BACK_BUTTON]
    
    #combine backgroud with title
    
    combined_surface = pygame.Surface((1200, 750))
    combined_surface.blit(background, (0,0))
    combined_surface.blit(title_image, (200, 245))
    
    
    for button in buttons:
        button.changeColor(menu_moouse_pos)
        button.update(screen)
    
    fade_in(1200, 750, combined_surface, buttons)
    while True:
        menu_moouse_pos = pygame.mouse.get_pos()
        
        EASY_BUTTON = Button(image=pygame.image.load(r"D:\UBB\a10-Annddu\Gomoku\images\play.png"), pos=(600, 404), 
                            text_input="EASY", font=get_font(55), base_color="Black", hovering_color="#00BE13")
        MEDIUM_BUTTON = Button(image=pygame.image.load(r"D:\UBB\a10-Annddu\Gomoku\images\play.png"), pos=(600, 484), 
                            text_input="MEDIUM", font=get_font(55), base_color="Black", hovering_color="#BE8E00")
        HARD_BUTTON = Button(image=pygame.image.load(r"D:\UBB\a10-Annddu\Gomoku\images\play.png"), pos=(600, 564), 
                            text_input="HARD", font=get_font(55), base_color="Black", hovering_color="#BE0000")
        BACK_BUTTON = Button(image=pygame.image.load(r"D:\UBB\a10-Annddu\Gomoku\images\play.png"), pos=(600, 644), 
                            text_input="BACK", font=get_font(55), base_color="Black", hovering_color="#C54949")
        
        screen.blit(background, (0,0))
        
        for button in [EASY_BUTTON, MEDIUM_BUTTON, HARD_BUTTON, BACK_BUTTON]:
            button.changeColor(menu_moouse_pos)
            button.update(screen)
        
        screen.blit(title_image, (200, 245))
                
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if BACK_BUTTON.checkForInput(menu_moouse_pos):
                    pygame.mixer.Sound.play(enter)
                    fade(1200, 750)
                    return easy_win_player, easy_win_computer, medium_win_player, medium_win_computer, hard_win_player, hard_win_computer
                    
                    
                if EASY_BUTTON.checkForInput(menu_moouse_pos):
                    minmax.difficulty(1)
                    pygame.mixer.Sound.play(enter)
                    fade(1200, 750)
                    easy_win_player, easy_win_computer, medium_win_player, medium_win_computer, hard_win_player, hard_win_computer = play(1, easy_win_player, easy_win_computer, medium_win_player, medium_win_computer, hard_win_player, hard_win_computer)
                    
                if MEDIUM_BUTTON.checkForInput(menu_moouse_pos):
                    minmax.difficulty(2)
                    pygame.mixer.Sound.play(enter)
                    fade(1200, 750)
                    easy_win_player,  easy_win_computer, medium_win_player, medium_win_computer, hard_win_player, hard_win_computer = play(2, easy_win_player, easy_win_computer, medium_win_player, medium_win_computer, hard_win_player, hard_win_computer)
                    
                if HARD_BUTTON.checkForInput(menu_moouse_pos):
                    minmax.difficulty(3)
                    pygame.mixer.Sound.play(enter)
                    fade(1200, 750)
                    easy_win_player, easy_win_computer, medium_win_player, medium_win_computer, hard_win_player, hard_win_computer = play(3, easy_win_player, easy_win_computer, medium_win_player, medium_win_computer, hard_win_player, hard_win_computer)
                    
        pygame.display.update()
        clock.tick(60)
    
def main_menu():
    menu_moouse_pos = pygame.mouse.get_pos()
    easy_win_player, easy_win_computer, medium_win_player, medium_win_computer, hard_win_player, hard_win_computer = 0, 0, 0, 0, 0, 0
    
    PLAY_BUTTON = Button(image=pygame.image.load(r"D:\UBB\a10-Annddu\Gomoku\images\play.png"), pos=(600, 404),
                        text_input="PLAY", font=get_font(55), base_color="Black", hovering_color="#8DC549")
    EXIT_BUTTON = Button(image=pygame.image.load(r"D:\UBB\a10-Annddu\Gomoku\images\play.png"), pos=(600, 484),
                        text_input="EXIT", font=get_font(55), base_color="Black", hovering_color="#C54949") 
    
    buttons = [PLAY_BUTTON, EXIT_BUTTON]
    
    screen.blit(background, (0,0))
    
    for button in buttons:
        button.changeColor(menu_moouse_pos)
        button.update(screen)
        
    fade_in(1200, 750, background, buttons)
    
    while True: 
        menu_moouse_pos = pygame.mouse.get_pos()
        
        PLAY_BUTTON = Button(image=pygame.image.load(r"D:\UBB\a10-Annddu\Gomoku\images\play.png"), pos=(600, 404), 
                            text_input="PLAY", font=get_font(55), base_color="Black", hovering_color="#8DC549")
        EXIT_BUTTON = Button(image=pygame.image.load(r"D:\UBB\a10-Annddu\Gomoku\images\play.png"), pos=(600, 484), 
                            text_input="EXIT", font=get_font(55), base_color="Black", hovering_color="#C54949")
        
        
        screen.blit(background, (0,0))
        #screen.blit(menu_text, menu_rect)
        
        for button in [PLAY_BUTTON, EXIT_BUTTON]:
            button.changeColor(menu_moouse_pos)
            button.update(screen)
                
        andu.move_left(speed)
        moving_andu.draw(screen)
        moving_andu.update()
        
        moving_title.draw(screen)
        moving_title.update()
        
        moving_mesaj.draw(screen)
        moving_mesaj.update()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(menu_moouse_pos):
                    pygame.mixer.Sound.play(enter)
                    fade(1200, 750)
                    easy_win_player, easy_win_computer, medium_win_player, medium_win_computer, hard_win_player, hard_win_computer = play_options(easy_win_player, easy_win_computer, medium_win_player, medium_win_computer, hard_win_player, hard_win_computer)
                    
                if EXIT_BUTTON.checkForInput(menu_moouse_pos):
                    pygame.mixer.Sound.play(enter)
                    pygame.time.delay(500)
                    pygame.quit()
                    exit()
        
        pygame.display.update()
        clock.tick(60)


main_menu()