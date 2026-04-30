import pygame

pygame.init()

paintings = []
timer = pygame.time.Clock()
fps = 60

active_color = (0, 0, 0)
active_shape = 0  

window_width, window_height = 800, 600
screen = pygame.display.set_mode([window_width, window_height])
pygame.display.set_caption("Drawing App")

def draw_display():
    pygame.draw.rect(screen, 'gray', [0, 0, window_width, 100])
    pygame.draw.line(screen, 'black', [0, 100], [window_width, 100])
    buttons = []
    pygame.draw.rect(screen, 'black', [10,10,80,80])
    pygame.draw.rect(screen, 'white', [20,20,60,60])
    buttons.append([pygame.Rect(10,10,80,80), 0])
    pygame.draw.rect(screen, 'black', [100,10,80,80])
    pygame.draw.circle(screen, 'white', [140,50], 30)
    buttons.append([pygame.Rect(100,10,80,80), 1])
    pygame.draw.rect(screen, 'black', [200,10,80,80])
    pygame.draw.polygon(screen, 'white', ((240,90),(210,50),(270,50)))
    buttons.append([pygame.Rect(200,10,80,80), 2])
    pygame.draw.rect(screen, 'black', [300,10,80,80])
    pygame.draw.polygon(screen, 'white', ((340,50),(380,90),(420,50),(380,10)))
    buttons.append([pygame.Rect(300,10,80,80), 3])
    pygame.draw.rect(screen, 'black', [400,10,80,80])
    pygame.draw.polygon(screen, 'white', ((420,90),(420,30),(480,90)))
    buttons.append([pygame.Rect(400,10,80,80), 4])
    
    colors = []
    color_positions = [(window_width-35,10,25,25,(0,0,255)), (window_width-35,35,25,25,(255,0,0)),
                       (window_width-60,10,25,25,(0,255,0)), (window_width-60,35,25,25,(255,255,0)),
                       (window_width-85,10,25,25,(0,0,0)), (window_width-85,35,25,25,(255,0,255))]
    for x,y,w,h,c in color_positions:
        pygame.draw.rect(screen, c, [x,y,w,h])
        colors.append([pygame.Rect(x,y,w,h), c])
    
    pygame.draw.rect(screen, (255,255,255), [window_width-150,20,25,25])
    colors.append([pygame.Rect(window_width-150,20,25,25), (255,255,255)])
    
    return colors, buttons

def draw_paintings(paints):
    for color, pos, shape in paints:
        if shape == 0:  # квадрат
            pygame.draw.rect(screen, color, [pos[0]-15, pos[1]-15, 30, 30])
        elif shape == 1:  # круг
            pygame.draw.circle(screen, color, pos, 15)
        elif shape == 2:  # равносторонний треугольник
            pygame.draw.polygon(screen, color, ((pos[0], pos[1]-15), (pos[0]-15, pos[1]+10), (pos[0]+15, pos[1]+10)))
        elif shape == 3:  # ромб
            pygame.draw.polygon(screen, color, ((pos[0], pos[1]-20), (pos[0]+20, pos[1]), (pos[0], pos[1]+20), (pos[0]-20, pos[1])))
        elif shape == 4:  # прямоугольный треугольник
            pygame.draw.polygon(screen, color, ((pos[0]-15, pos[1]+15), (pos[0]-15, pos[1]-15), (pos[0]+15, pos[1]+15)))

def draw_preview():
    if mouse_pos[1] > 100:
        if active_shape == 0:
            pygame.draw.rect(screen, active_color, [mouse_pos[0]-15, mouse_pos[1]-15, 30, 30])
        elif active_shape == 1:
            pygame.draw.circle(screen, active_color, mouse_pos, 15)
        elif active_shape == 2:
            pygame.draw.polygon(screen, active_color, ((mouse_pos[0], mouse_pos[1]-15), (mouse_pos[0]-15, mouse_pos[1]+10), (mouse_pos[0]+15, mouse_pos[1]+10)))
        elif active_shape == 3:
            pygame.draw.polygon(screen, active_color, ((mouse_pos[0], mouse_pos[1]-20), (mouse_pos[0]+20, mouse_pos[1]), (mouse_pos[0], mouse_pos[1]+20), (mouse_pos[0]-20, mouse_pos[1])))
        elif active_shape == 4:
            pygame.draw.polygon(screen, active_color, ((mouse_pos[0]-15, mouse_pos[1]+15), (mouse_pos[0]-15, mouse_pos[1]-15), (mouse_pos[0]+15, mouse_pos[1]+15)))

run = True
while run:
    timer.tick(fps)
    screen.fill('white')
    colors, shapes = draw_display()
    mouse_pos = pygame.mouse.get_pos()
    draw_preview()
    draw_paintings(paintings)
    
    if pygame.mouse.get_pressed()[0] and mouse_pos[1] > 100:
        paintings.append((active_color, mouse_pos, active_shape))
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            run = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            paintings = []
        if event.type == pygame.MOUSEBUTTONDOWN:
            for btn, val in colors:
                if btn.collidepoint(event.pos):
                    active_color = val
            for btn, val in shapes:
                if btn.collidepoint(event.pos):
                    active_shape = val
    
    pygame.display.flip()

pygame.quit()