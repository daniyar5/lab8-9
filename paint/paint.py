import pygame

pygame.init()


#screen
WIDTH = 800
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
base_layer = pygame.Surface((WIDTH, HEIGHT))

#colors
colorRED = (255, 0, 0)
colorBLUE = (0, 0, 255)
colorWHITE = (255, 255, 255)
colorBLACK = (0, 0, 0)
colorGREEN = (0, 255, 0)
colors = [colorRED, colorBLUE, colorWHITE, colorBLACK, colorGREEN]
current_color = (0, 0, 0)

#bools
LMBpressed = False
done = False
line = False
rect = False
circle = False
eraser = False
square = False
triangle_r = False
triangle_e = False

THICKNESS = 5
currX = 0
currY = 0
prevX = 0
prevY = 0

def calculate_rect(x1, y1, x2, y2):
    return pygame.Rect(min(x1, x2), min(y1, y2), abs(x1 - x2), abs(y1 - y2))



def calculate_square(x1, y1, x2, y2):
    a = min(abs(x1 - x2), abs(y1 - y2))
    if x2 < x1:
        x1 = x1 - a
    if y2 < y1:
        y1 = y1 - a
    return pygame.Rect(x1, y1, a, a)



while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

        if rect == True or circle == True or square == True:
            if LMBpressed:
                screen.blit(base_layer, (0, 0))

        #mouse button down
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            LMBpressed = True
            if (rect == True or circle == True or square == True):
                prevX = event.pos[0]
                prevY = event.pos[1]
            elif (line == True or eraser == True):
                currX = event.pos[0]
                currY = event.pos[1]
                prevX = event.pos[0]
                prevY = event.pos[1]


        #mouse button in motion
        if event.type == pygame.MOUSEMOTION:
            if LMBpressed:
                currX = event.pos[0]
                currY = event.pos[1]
                if line:
                    pygame.draw.line(screen, current_color, (prevX, prevY), (currX, currY), THICKNESS)
                elif rect:
                    pygame.draw.rect(screen, current_color, calculate_rect(prevX, prevY, currX, currY), THICKNESS)
                elif circle:
                    pygame.draw.ellipse(screen, current_color, calculate_rect(prevX, prevY, currX, currY), THICKNESS)
                elif eraser:
                    pygame.draw.line(screen, colors[3], (prevX, prevY), (currX, currY), THICKNESS)
                elif square:
                    pygame.draw.rect(screen, current_color, calculate_square(prevX, prevY, currX, currY), THICKNESS)

        #mouse button up
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            print("LMB released!")
            print(line, eraser)
            LMBpressed = False
            currX = event.pos[0]
            currY = event.pos[1]
            if line:
                pygame.draw.line(screen, current_color, (prevX, prevY), (currX, currY), THICKNESS)
            elif rect:
                pygame.draw.rect(screen, current_color, calculate_rect(prevX, prevY, currX, currY), THICKNESS)
            elif circle:
                pygame.draw.ellipse(screen, current_color, calculate_rect(prevX, prevY, currX, currY), THICKNESS)
            elif eraser:
                pygame.draw.line(screen, colors[3], (prevX, prevY), (currX, currY), THICKNESS)
            elif square:
                pygame.draw.rect(screen, current_color, calculate_square(prevX, prevY, currX, currY), THICKNESS)

            base_layer.blit(screen, (0, 0))

                    
        

        #keys
        if event.type == pygame.KEYDOWN: 
            if event.key == pygame.K_EQUALS:
                print("increased thickness")
                THICKNESS += 1
            if event.key == pygame.K_MINUS:
                print("reduced thickness")
                THICKNESS -= 1
            if event.key == pygame.K_l:
                line = True
                rect = False
                circle = False
                eraser = False
                square = False
            if event.key == pygame.K_r:
                rect = True
                circle = False
                line = False
                eraser = False
                square = False
            if event.key == pygame.K_c:
                circle = True
                rect = False
                line = False
                eraser = False
                square = False
            if event.key == pygame.K_e:
                eraser = True
                rect = False
                circle = False
                line = False
                square = False
            if event.key == pygame.K_s:
                square = True
                eraser = False
                rect = False
                circle = False
                line = False
            if event.key == pygame.K_g:
                current_color = colors[4]
            if event.key == pygame.K_b:
                current_color = colors[1]
            if event.key == pygame.K_w:
                current_color = colors[2]

    #set up points for line and eraser
    if line == True or eraser == True:
        prevX = currX
        prevY = currY

    pygame.display.flip()
