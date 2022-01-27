import pygame,pygame.freetype,pygame.gfxdraw
import os, sys, traceback, random
from pygame.locals import K_UP,K_LEFT,K_DOWN,K_RIGHT,K_ESCAPE,K_SPACE

def sign(v:int):
    return (0 if v==0 else (v // abs(v)))

scriptpath = os.path.dirname(os.path.realpath(__file__))
clock = pygame.time.Clock()


CLR_BG = (0x14,0x1E,0x27)
CLR_FNT = (0xc0,0xdf,0x15)
CLR_GRID = (0x17,0x23,0x2e)
CLR_BODY = (0x60,0x8c,0x55)
CLR_HEAD = (0xad,0xb1,0x8b)
CLR_APPLE = (0xff,0x48,0x3d)


# game field size
SQUARE = 20
FW = 30
FH = 20

# game speed
FPS = 60
running = True
step_delay = 10 # game speed
step_rest = step_delay # step clock

dir = 1 # initial direction
dirs = [(0,-1),(1,0),(0,1),(-1,0)]

# create snake
bodylen = 5
body = [(2,FH//2)]
for i in range(1,bodylen):
    body.append((body[0][0]+i,body[0][1]));
body.reverse()


def point_in_body(p):
    for i in body: 
        if (i==p):
            return True
    return False

def create_apple():
    while True:
        a = (random.randint(0, FW-1), random.randint(0, FH-1))
        if not point_in_body(a):
            return a

apple = create_apple()

try:
    try:
        pygame.init()
        pygame.display.set_caption("Snake")
        surf_act = pygame.display.set_mode((FW*SQUARE, FH*SQUARE))
        #fnt = pygame.freetype.Font(os.path.join(scriptpath, 'app.ttf'), 10)

        while running:
            
            ###############################################################################
            #
            #   KEYS
            #
            ###############################################################################
            for event in pygame.event.get():
                if event.type == pygame.QUIT: sys.exit()
                
                # keys handler                       
                if event.type == pygame.KEYDOWN:
                    try:
                        key_index=[K_UP,K_RIGHT,K_DOWN,K_LEFT,K_ESCAPE,K_SPACE].index(event.key)
                        if (key_index<4): # check if new direction allowed
                            if ((key_index & 1) != (dir & 1)):
                                dir = key_index

                        if (key_index==4): running = False
                        
                    except ValueError: pass
                    else: pass
            
            ###############################################################################
            #
            #   STEP 
            #
            ###############################################################################
            if (step_rest == 0):
                step_rest = step_delay 
                next = (body[0][0] + dirs[dir][0], body[0][1] + dirs[dir][1]) #next head pos
                
                
                if point_in_body(next): # check eat itself
                   break 
                if ( (next[0]<0) or (next[1]<0) or (next[0]>=FW) or (next[1]>=FH) ): # check gamefield exit
                    break

                body.insert(0, next )
                if (next==apple):
                    bodylen += 1
                    apple = create_apple() 
                else:                    
                    body.pop(bodylen)
            step_rest -= 1    


            ###############################################################################
            #
            #   DRAW 
            #
            ###############################################################################

            # BG
            surf_act.fill(CLR_BG) 
            # grid
            for x in range(FW): pygame.draw.line(surf_act, CLR_GRID, (SQUARE*x,0 ), (SQUARE*x, SQUARE*FH), 1)
            for y in range(FH): pygame.draw.line(surf_act, CLR_GRID, (0, SQUARE*y ), (SQUARE*FW, SQUARE*y), 1)
            # snake body
            c = 0
            for i in body: 
                surf_act.fill(CLR_HEAD if c==0 else CLR_BODY,[i[0]*SQUARE+1,i[1]*SQUARE+1,SQUARE-1,SQUARE-1])
                c += 1
            # apple 
            surf_act.fill(CLR_APPLE,[apple[0]*SQUARE+1,apple[1]*SQUARE+1,SQUARE-1,SQUARE-1])
            # fps
            #fnt.render_to(surf_act, (10,10), str(step_rest), CLR_FNT) 

            pygame.display.flip()
            clock.tick(FPS)
    finally:
        pygame.quit()
       

except Exception as e:
    print()
    print("\n=-=-=- ERROR =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=\n")
    e = sys.exc_info()[1]
    print(e.args[0])
    traceback.print_exc()
    print("\n=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-\n")

