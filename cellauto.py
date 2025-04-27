import random
import pygame

# yes i know, code is not good, it is lagging on my laptop

map_w = 64 # map width
map_h = 64 # map height

cell_w = 6 # cell width (for render)
cell_h = 6 # cell height (for render)

window_w = map_w * cell_w # window width (for render)
window_h = map_h * cell_h # window height (for render)

rule_b = [8,9,10] # neighbour counts for cell to birth
rule_s = [5,6,7,8,9,10] # neighbour counts for cell to keep alive

alive_color = (255, 255, 255) # color for alive cell
alive_hl_color_1 = (16, 128, 16) # color for neighbour area highlight
alive_hl_color_2 = (64, 128, 64)
bg_color_1 = (0, 0, 0) # color for dead cell (background)
bg_color_2 = (32, 32, 32)

def emptyMap(w, h):
    mm = []

    for i in range(w):
        mm.append([])
        for j in range(h):
            mm[i].append(0)

    return mm

def randMap(w, h):
    mm = []

    for i in range(w):
        mm.append([])
        for j in range(h):
            mm[i].append(random.randint(0,1))

    return mm

back_map = emptyMap(map_w, map_h)
main_map = randMap(map_w, map_h)

stable = False

def tick():
    global map_w, map_h, main_map, stability
    sec_map = emptyMap(map_w, map_h)

    for i in range(map_w):
        for j in range(map_h):
            n = 0
            for ofx in range(-2, 3):
                for ofy in range(-2, 3):
                    if ofx == 0 and ofy == 0:
                        continue
                    n += main_map[(i+ofx)%map_w][(j+ofy)%map_h]
            if n in rule_s:
                sec_map[i][j] = main_map[i][j]
            if n in rule_b:
                sec_map[i][j] = 1
	
    back_map = main_map
    main_map = sec_map

    if back_map == main_map:
        stable = True

pygame.init()
screen = pygame.display.set_mode((window_w, window_h))
done = False
running = True
cam_x = 0
cam_y = 0
 
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                print("ok. restarting map.")
                main_map = randMap(map_w, map_h)
                stability = False
            if event.key == pygame.K_SPACE:
                running = not running
                print('running:', running)
            if event.key == pygame.K_f:
                tick()
                print('going 1 frame forward')
            if event.key == pygame.K_UP:
                cam_y += 1
            if event.key == pygame.K_DOWN:
                cam_y -= 1
            if event.key == pygame.K_RIGHT:
                cam_x -= 1
            if event.key == pygame.K_LEFT:
                cam_x += 1

    if running: tick()

    for i in range(map_w):
        for j in range(map_h):
            if (i%2)==(j%2):
                pygame.draw.rect(screen, bg_color_2, pygame.Rect(((cam_x+i)%map_w)*cell_w, ((cam_y+j)%map_h)*cell_h, cell_w, cell_h))
            else:
                pygame.draw.rect(screen, bg_color_1, pygame.Rect(((cam_x+i)%map_w)*cell_w, ((cam_y+j)%map_h)*cell_h, cell_w, cell_h))

    for i in range(map_w):
        for j in range(map_h):
            if main_map[i][j] == 1:
                for hx in range(-2, 3):
                    for hy in range(-2, 3):
                        if (((i+hx)%map_w)%2)==(((j+hy)%map_h)%2):
                            pygame.draw.rect(screen, alive_hl_color_2, pygame.Rect(((i+hx+cam_x)%map_w)*cell_w, ((j+hy+cam_y)%map_h)*cell_h, cell_w, cell_h))
                        else:
                            pygame.draw.rect(screen, alive_hl_color_1, pygame.Rect(((i+hx+cam_x)%map_w)*cell_w, ((j+hy+cam_y)%map_h)*cell_h, cell_w, cell_h))
                
    for i in range(map_w):
        for j in range(map_h):
            if main_map[i][j] == 1:
                pygame.draw.rect(screen, alive_color, pygame.Rect(((cam_x+i)%map_w)*cell_w, ((cam_y+j)%map_h)*cell_h, cell_w, cell_h))
                
    pygame.display.flip()
        
    if stability:
        print("it stability now")
        main_map = randMap(map_w, map_h)
        stability = False
                
