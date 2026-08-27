import os
import sys
import glob
import ctypes

# Bootstrap shared library paths for Linux/NixOS if SDL/OpenGL libraries are not in LD_LIBRARY_PATH
if sys.platform.startswith('linux') and 'ENV_BOOTSTRAPPED' not in os.environ:
    needs_bootstrap = False
    try:
        ctypes.CDLL('libGL.so.1')
        ctypes.CDLL('libX11.so.6')
    except OSError:
        needs_bootstrap = True

    if needs_bootstrap:
        search_dirs = ['/run/opengl-driver/lib']
        pkgs = [
            'libglvnd', 'glu', 'mesa', 'libx11', 'libxext', 'libxcursor',
            'libxi', 'libxfixes', 'libxrandr', 'libxrender', 'wayland',
            'libxkbcommon', 'libdecor', 'dbus', 'alsa-lib', 'libpulseaudio'
        ]
        for pkg in pkgs:
            for p in glob.glob(f'/nix/store/*-{pkg}-*/lib'):
                search_dirs.append(p)
        
        if search_dirs:
            env = os.environ.copy()
            current_ld = env.get('LD_LIBRARY_PATH', '')
            env['LD_LIBRARY_PATH'] = ':'.join(search_dirs) + (':' + current_ld if current_ld else '')
            env['PYOPENGL_PLATFORM'] = 'glx'
            env['ENV_BOOTSTRAPPED'] = '1'
            os.execve(sys.executable, [sys.executable] + sys.argv, env)

if 'PYOPENGL_PLATFORM' not in os.environ:
    os.environ['PYOPENGL_PLATFORM'] = 'glx'

import math
import pygame
from OpenGL import GL
from OpenGL import GLU

INV_SQRT_2 = 1/math.sqrt(2)

def drawCuboid(minCorner, maxCorner, mode=GL.GL_LINE_LOOP, color=(1.0, 1.0, 1.0, 1.0)): # two 3-tuples (x, y, z)
    GL.glLineWidth(2)
    GL.glColor4fv(color)
    if mode == GL.GL_LINE_LOOP:
        GL.glDisable(GL.GL_DEPTH_TEST)
    else:
        GL.glEnable(GL.GL_DEPTH_TEST)
    GL.glBegin(mode)
    
    GL.glVertex3f(minCorner[0], minCorner[1], minCorner[2])
    GL.glVertex3f(maxCorner[0], minCorner[1], minCorner[2])
    GL.glVertex3f(maxCorner[0], maxCorner[1], minCorner[2])
    
    GL.glVertex3f(minCorner[0], minCorner[1], minCorner[2])
    GL.glVertex3f(minCorner[0], maxCorner[1], minCorner[2])
    GL.glVertex3f(maxCorner[0], maxCorner[1], minCorner[2])
    
    GL.glVertex3f(minCorner[0], minCorner[1], minCorner[2])
    GL.glVertex3f(maxCorner[0], minCorner[1], minCorner[2])
    GL.glVertex3f(maxCorner[0], minCorner[1], maxCorner[2])
    
    GL.glVertex3f(minCorner[0], minCorner[1], minCorner[2])
    GL.glVertex3f(minCorner[0], minCorner[1], maxCorner[2])
    GL.glVertex3f(maxCorner[0], minCorner[1], maxCorner[2])
    
    GL.glVertex3f(minCorner[0], minCorner[1], minCorner[2])
    GL.glVertex3f(minCorner[0], maxCorner[1], minCorner[2])
    GL.glVertex3f(minCorner[0], maxCorner[1], maxCorner[2])
    
    GL.glVertex3f(minCorner[0], minCorner[1], minCorner[2])
    GL.glVertex3f(minCorner[0], minCorner[1], maxCorner[2])
    GL.glVertex3f(minCorner[0], maxCorner[1], maxCorner[2])
    
    GL.glVertex3f(maxCorner[0], maxCorner[1], maxCorner[2])
    GL.glVertex3f(minCorner[0], maxCorner[1], maxCorner[2])
    GL.glVertex3f(minCorner[0], minCorner[1], maxCorner[2])
    
    GL.glVertex3f(maxCorner[0], maxCorner[1], maxCorner[2])
    GL.glVertex3f(maxCorner[0], minCorner[1], maxCorner[2])
    GL.glVertex3f(minCorner[0], minCorner[1], maxCorner[2])
    
    GL.glVertex3f(maxCorner[0], maxCorner[1], maxCorner[2])
    GL.glVertex3f(minCorner[0], maxCorner[1], maxCorner[2])
    GL.glVertex3f(minCorner[0], maxCorner[1], minCorner[2])
    
    GL.glVertex3f(maxCorner[0], maxCorner[1], maxCorner[2])
    GL.glVertex3f(maxCorner[0], maxCorner[1], minCorner[2])
    GL.glVertex3f(minCorner[0], maxCorner[1], minCorner[2])
    
    GL.glVertex3f(maxCorner[0], maxCorner[1], maxCorner[2])
    GL.glVertex3f(maxCorner[0], minCorner[1], maxCorner[2])
    GL.glVertex3f(maxCorner[0], minCorner[1], minCorner[2])
    
    GL.glVertex3f(maxCorner[0], maxCorner[1], maxCorner[2])
    GL.glVertex3f(maxCorner[0], maxCorner[1], minCorner[2])
    GL.glVertex3f(maxCorner[0], minCorner[1], minCorner[2])
        
    GL.glEnd()

def drawInputOverlay(action, width, height):
    GL.glMatrixMode(GL.GL_PROJECTION)
    GL.glPushMatrix()
    GL.glLoadIdentity()
    
    GLU.gluOrtho2D(0, width, height, 0)
    
    GL.glMatrixMode(GL.GL_MODELVIEW)
    GL.glPushMatrix()
    GL.glLoadIdentity()
    GL.glDisable(GL.GL_DEPTH_TEST)

    GL.glBegin(GL.GL_TRIANGLES)
    
    # space bar
    if action & 1:
        GL.glColor4fv((1.0, 1.0, 1.0, 0.5))
    else:
        GL.glColor4fv((0.5, 0.5, 0.5, 0.5))
    
    GL.glVertex2f(width-230, height-50)
    GL.glVertex2f(width-130, height-50)
    GL.glVertex2f(width-130, height-30)
    
    GL.glVertex2f(width-230, height-50)
    GL.glVertex2f(width-230, height-30)
    GL.glVertex2f(width-130, height-30)
    
    # a
    if action & 2:
        GL.glColor4fv((1.0, 1.0, 1.0, 0.5))
    else:
        GL.glColor4fv((0.5, 0.5, 0.5, 0.5))    
        
    GL.glVertex2f(width-295, height-100)
    GL.glVertex2f(width-275, height-100)
    GL.glVertex2f(width-275, height-80)
    
    GL.glVertex2f(width-295, height-100)
    GL.glVertex2f(width-295, height-80)
    GL.glVertex2f(width-275, height-80)
    
    # d
    if action & 4:
        GL.glColor4fv((1.0, 1.0, 1.0, 0.5))
    else:
        GL.glColor4fv((0.5, 0.5, 0.5, 0.5))    
        
    GL.glVertex2f(width-245, height-100)
    GL.glVertex2f(width-225, height-100)
    GL.glVertex2f(width-225, height-80)
    
    GL.glVertex2f(width-245, height-100)
    GL.glVertex2f(width-245, height-80)
    GL.glVertex2f(width-225, height-80)
    
    # w
    if action & 8:
        GL.glColor4fv((1.0, 1.0, 1.0, 0.5))
    else:
        GL.glColor4fv((0.5, 0.5, 0.5, 0.5))    
        
    GL.glVertex2f(width-270, height-125)
    GL.glVertex2f(width-250, height-125)
    GL.glVertex2f(width-250, height-105)
    
    GL.glVertex2f(width-270, height-125)
    GL.glVertex2f(width-270, height-105)
    GL.glVertex2f(width-250, height-105)
    
    # s
    if action & 16:
        GL.glColor4fv((1.0, 1.0, 1.0, 0.5))
    else:
        GL.glColor4fv((0.5, 0.5, 0.5, 0.5))    
        
    GL.glVertex2f(width-270, height-100)
    GL.glVertex2f(width-250, height-100)
    GL.glVertex2f(width-250, height-80)
    
    GL.glVertex2f(width-270, height-100)
    GL.glVertex2f(width-270, height-80)
    GL.glVertex2f(width-250, height-80)
    
    # left arrow
    if action & 32:
        GL.glColor4fv((1.0, 1.0, 1.0, 0.5))
    else:
        GL.glColor4fv((0.5, 0.5, 0.5, 0.5))    
        
    GL.glVertex2f(width-80, height-40)
    GL.glVertex2f(width-60, height-40)
    GL.glVertex2f(width-60, height-30)
    
    GL.glVertex2f(width-80, height-40)
    GL.glVertex2f(width-80, height-30)
    GL.glVertex2f(width-60, height-30)
    
    # right arrow
    if action & 64:
        GL.glColor4fv((1.0, 1.0, 1.0, 0.5))
    else:
        GL.glColor4fv((0.5, 0.5, 0.5, 0.5))    
        
    GL.glVertex2f(width-30, height-40)
    GL.glVertex2f(width-10, height-40)
    GL.glVertex2f(width-10, height-30)
    
    GL.glVertex2f(width-30, height-40)
    GL.glVertex2f(width-30, height-30)
    GL.glVertex2f(width-10, height-30)
    
    GL.glEnd()
    
    GL.glPopMatrix()
    GL.glMatrixMode(GL.GL_PROJECTION)
    GL.glPopMatrix()
    GL.glMatrixMode(GL.GL_MODELVIEW)

class Player:
    COLOR = (1.0, 0.0, 1.0, 1.0)
    WIDTH = 100
    HEIGHT = 500
    LENGTH = 100
    MOVE_ACCEL = 3
    FALL_ACCEL = 3
    JUMP_ACCEL = 80
    FRIC_MULT = 0.85
    
    def __init__(self, x, y, z, direction):
        self.x = x
        self.y = y
        self.z = z
        self.velX = 0
        self.velY = 0
        self.velZ = 0
        self.direction = direction # 0 = 360 = -z axis
        self.coyoteTime = 0 # 5 frames of coyote time
    
    # binary actions
    # 0000001 - jump
    # 0000010 - left
    # 0000100 - right
    # 0001000 - forward
    # 0010000 - back
    # 0100000 - turnLeft
    # 1000000 - turnRight
    
    def doTick(self, action, objectList, winpad):
        oldX = self.x
        oldY = self.y
        oldZ = self.z
        
        jumpAtt = action & 1
        leftAtt = action & 2
        rightAtt = action & 4
        forwardAtt = action & 8
        backAtt = action & 16
        turnLeftAtt = action & 32
        turnRightAtt = action & 64
        
        if leftAtt and rightAtt:
            leftAtt = False
            rightAtt = False
        if forwardAtt and backAtt:
            forwardAtt = False
            backAtt = False
        if turnLeftAtt and turnRightAtt:
            turnLeftAtt = False
            turnRightAtt = False
            
        if turnLeftAtt:
            self.direction -= 4
            if self.direction > 360:
                self.direction -= 360
        elif turnRightAtt:
            self.direction += 4
            if self.direction < 0:
                self.direction += 360
        
        # x, z
        forwardVector = (math.sin(math.radians(self.direction)), -math.cos(math.radians(self.direction)))
        rightVector = (-forwardVector[1], forwardVector[0])
        forwardRightVector = (INV_SQRT_2*forwardVector[0]-INV_SQRT_2*forwardVector[1], INV_SQRT_2*forwardVector[0]+INV_SQRT_2*forwardVector[1])
        forwardLeftVector = (forwardRightVector[1], -forwardRightVector[0])
        
        lrMove = False
        fbMove = False
        if leftAtt or rightAtt:
            lrMove = True
        if forwardAtt or backAtt:
            fbMove = True
        
        if leftAtt and not fbMove:
            self.velX -= Player.MOVE_ACCEL * rightVector[0]
            self.velZ -= Player.MOVE_ACCEL * rightVector[1]
        elif rightAtt and not fbMove:
            self.velX += Player.MOVE_ACCEL * rightVector[0]
            self.velZ += Player.MOVE_ACCEL * rightVector[1]
        elif backAtt and not lrMove:
            self.velX -= Player.MOVE_ACCEL * forwardVector[0]
            self.velZ -= Player.MOVE_ACCEL * forwardVector[1]
        elif forwardAtt and not lrMove:
            self.velX += Player.MOVE_ACCEL * forwardVector[0]
            self.velZ += Player.MOVE_ACCEL * forwardVector[1]
        elif leftAtt and forwardAtt:
            self.velX += Player.MOVE_ACCEL * forwardLeftVector[0]
            self.velZ += Player.MOVE_ACCEL * forwardLeftVector[1]
        elif rightAtt and backAtt:
            self.velX -= Player.MOVE_ACCEL * forwardLeftVector[0]
            self.velZ -= Player.MOVE_ACCEL * forwardLeftVector[1]
        elif rightAtt and forwardAtt:
            self.velX += Player.MOVE_ACCEL * forwardRightVector[0]
            self.velZ += Player.MOVE_ACCEL * forwardRightVector[1]
        elif leftAtt and backAtt:
            self.velX -= Player.MOVE_ACCEL * forwardRightVector[0]
            self.velZ -= Player.MOVE_ACCEL * forwardRightVector[1]
        
        self.velX *= Player.FRIC_MULT
        self.velZ *= Player.FRIC_MULT
        self.velY -= Player.FALL_ACCEL
        self.x += self.velX
        self.y += self.velY
        self.z += self.velZ
        
        uncheckedCol = True
        checkOverload = 100
        while uncheckedCol and checkOverload > 0:
            uncheckedCol = False
            checkOverload -= 1

            for obj in objectList:
                xCollide = (self.x<(obj.x+obj.length)) and (obj.x<(self.x+Player.LENGTH))
                yCollide = (self.y<(obj.y+obj.height)) and (obj.y<(self.y+Player.HEIGHT))
                zCollide = (self.z<(obj.z+obj.width)) and (obj.z<(self.z+Player.WIDTH))
                
                if xCollide and yCollide and zCollide:
                    uncheckedCol = True
                    if oldY >= (obj.y+obj.height):
                        self.y = obj.y+obj.height
                        self.velY = 0
                        self.coyoteTime = 4
                    elif (oldX+Player.LENGTH) <= obj.x:
                        self.x = obj.x-Player.LENGTH
                        self.velX = 0
                    elif (oldZ+Player.WIDTH) <= obj.z:
                        self.z = obj.z-Player.WIDTH
                        self.velZ = 0
                    elif oldX >= (obj.x+obj.length):
                        self.x = obj.x+obj.length
                        self.velX = 0
                    elif oldZ >= (obj.z+obj.width):
                        self.z = obj.z+obj.width
                        self.velZ = 0
                    else:
                        self.y = obj.y-Player.HEIGHT
                        self.velY = 0
        
        if self.coyoteTime > 0:
            if jumpAtt:
                self.velY = Player.JUMP_ACCEL
                self.coyoteTime = 0
            else:
                self.coyoteTime -= 1
        
        xCollide = (self.x<(winpad.x+winpad.length)) and (winpad.x<(self.x+Player.LENGTH))
        yCollide = (self.y<(winpad.y+winpad.height)) and (winpad.y<(self.y+Player.HEIGHT))
        zCollide = (self.z<(winpad.z+winpad.width)) and (winpad.z<(self.z+Player.WIDTH))
        
        if xCollide and yCollide and zCollide:
            return 1
        else:
            return 0
    
    def clone(self):
        clonedPlayer = Player(self.x, self.y, self.z, self.direction)
        clonedPlayer.velX = self.velX
        clonedPlayer.velY = self.velY
        clonedPlayer.velZ = self.velZ
        clonedPlayer.coyoteTime = self.coyoteTime
        return clonedPlayer
    
class Object:
        
    def __init__(self, x, y, z, length, height, width, color=(1.0, 1.0, 1.0, 1.0)):
        self.x = x
        self.y = y
        self.z = z
        self.length = length
        self.height = height
        self.width = width
        self.color = color
    
class Human:
    
    def __init__(self):
        pass
    
    def getAction(self):
        action = 0
        
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            action += 1
        if keys[pygame.K_a]:
            action += 2
        if keys[pygame.K_d]:
            action += 4
        if keys[pygame.K_w]:
            action += 8
        if keys[pygame.K_s]:
            action += 16
        if keys[pygame.K_LEFT]:
            action += 32
        if keys[pygame.K_RIGHT]:
            action += 64
        
        return action
    
class InputString:
    
    def __init__(self, string=None, fromText=False):
        self.string = ""
        if fromText:
            with open(string, 'r') as file:
                self.string = file.read()
        elif string:
            self.string = string
    
    def getAction(self):
        global time
        if len(self.string) > time*3:
            return int(self.string[time*3:time*3+3])
        else:
            return 0
            
def loadBasicJumps():
    winpadColor = (0.0, 1.0, 0.0, 1.0)
    baseColor = (1.0, 0.65, 0.0, 1.0)
    
    player = Player(100, 0, 100, 90)
    winpad = Object(5000, -100, 0, 500, 100, 500, winpadColor)
    objectList = []
    objectList.append(Object(0, -100, 0, 500, 100, 500, baseColor))
    objectList.append(Object(1100, -100, 0, 500, 100, 500, baseColor))
    objectList.append(Object(1300, 0, 0, 100, 1000, 500, baseColor))
    objectList.append(Object(2300, -100, 0, 500, 100, 500, baseColor))
    objectList.append(Object(3600, -100, 0, 500, 100, 500, baseColor))
    objectList.append(Object(3800, 0, 0, 100, 1500, 500, baseColor))
    
    
    return player, objectList, winpad
    
def loadSNFA():
    winpadColor = (0.0, 1.0, 0.0, 1.0)
    floor1Color = (0.98, 0.5, 0.45, 1.0)
    floor2Color = (0.14, 0.24, 0.6, 1.0)
        
    player = Player(-7000, 500, 1000, 270)
    winpad = Object(3699, 10299, 1820, 500, 100, 500, winpadColor)
    objectList = []
    
    objectList.append(Object(-9900, 14799, -4779, 200, 400, 1100, floor2Color))
    objectList.append(Object(-10100, 14799, -3679, 200, 400, 1300, floor2Color))
    objectList.append(Object(-5400, 16499, -5979, 300, 100, 1500, floor2Color))
    objectList.append(Object(-8800, 12799, 620, 300, 300, 200, floor2Color))
    objectList.append(Object(-8000, 13399, 520, 300, 300, 400, floor2Color))
    objectList.append(Object(-8500, 12499, 520, 300, 300, 400, floor2Color))
    objectList.append(Object(-5500, 16499, -5979, 100, 1100, 1300, floor2Color))
    objectList.append(Object(-8600, 14799, -5979, 1000, 1700, 1100, floor2Color))
    objectList.append(Object(-10100, 13699, -979, 3400, 1600, 1000, floor2Color))
    objectList.append(Object(-6700, 15599, -5979, 600, 400, 1300, floor2Color))
    objectList.append(Object(-10100, 10099, -6079, 10000, 10000, 100, floor2Color))
    objectList.append(Object(-10100, 15899, -2979, 500, 2000, 200, floor2Color))
    objectList.append(Object(-7700, 13699, 20, 300, 300, 800, floor2Color))
    objectList.append(Object(-5400, 17099, -5979, 300, 100, 800, floor2Color))
    objectList.append(Object(-8600, 14799, -4879, 200, 400, 200, floor2Color))
    objectList.append(Object(-7400, 13699, 20, 300, 300, 400, floor2Color))
    objectList.append(Object(-10200, 10099, -5979, 100, 10000, 10000, floor2Color))
    objectList.append(Object(-5100, 16499, -5979, 100, 1100, 1300, floor2Color))
    objectList.append(Object(-7700, 12899, -1979, 1000, 1600, 1000, floor2Color))
    objectList.append(Object(-10100, 15199, -2379, 200, 400, 1000, floor2Color))
    objectList.append(Object(-8800, 14799, -5979, 200, 400, 1300, floor2Color))
    objectList.append(Object(-6700, 12299, -979, 1000, 1600, 1000, floor2Color))
    objectList.append(Object(-8500, 15299, -979, 200, 1600, 1000, floor2Color))
    objectList.append(Object(-7600, 14799, -5979, 200, 400, 1300, floor2Color))
    objectList.append(Object(-10100, 10099, 4020, 10000, 10000, 100, floor2Color))
    objectList.append(Object(-9900, 14799, -3679, 200, 400, 200, floor2Color))
    objectList.append(Object(-8750, 12800, 1720, 1100, 100, 400, floor2Color))
    objectList.append(Object(-10100, 11924, 1320, 200, 100, 400, floor2Color))
    objectList.append(Object(-10100, 12199, 1720, 300, 300, 400, floor2Color))
    objectList.append(Object(-7200, 15199, -5979, 200, 400, 1300, floor2Color))
    objectList.append(Object(-8200, 14799, -4879, 200, 1700, 100, floor2Color))
    objectList.append(Object(-4850, 12000, 820, 300, 300, 900, floor2Color))
    objectList.append(Object(-9700, 14799, -4779, 200, 400, 200, floor2Color))
    objectList.append(Object(-7800, 14799, -4879, 200, 400, 200, floor2Color))
    objectList.append(Object(-100, 99, -5979, 100, 10000, 10000, floor1Color))
    objectList.append(Object(3799, 199, -5279, 500, 9900, 500, floor1Color))
    objectList.append(Object(-1500, 6000, -829, 500, 100, 900, floor1Color))
    objectList.append(Object(-10100, 11924, 2120, 200, 100, 400, floor2Color))
    objectList.append(Object(-5900, 4600, -5979, 200, 2000, 200, floor1Color))
    objectList.append(Object(-200, 0, -5379, 100, 4800, 600, floor1Color))
    objectList.append(Object(-10100, 100, -1979, 10000, 200, 2000, floor1Color))
    objectList.append(Object(-9300, 4000, 2520, 800, 100, 600, floor1Color))
    objectList.append(Object(3899, 10399, -1829, 100, 1400, 100, floor2Color))
    objectList.append(Object(-3900, 100, -5979, 300, 4000, 600, floor1Color))
    objectList.append(Object(-5200, 4900, 3520, 1200, 1300, 500, floor1Color))
    objectList.append(Object(-4400, 16499, -5379, 800, 1400, 700, floor2Color))
    objectList.append(Object(3399, 11399, -479, 1000, 500, 100, floor2Color))
    objectList.append(Object(-2100, 18399, -5279, 100, 1700, 500, floor2Color))
    objectList.append(Object(-6400, 4600, -5479, 700, 2000, 100, floor1Color))
    objectList.append(Object(-2000, 19999, -5279, 1900, 100, 500, floor2Color))
    objectList.append(Object(-7050, 10600, 1720, 400, 400, 400, floor2Color))
    objectList.append(Object(3799, 7799, -4079, 500, 5600, 400, floor1Color))
    objectList.append(Object(-3600, 18299, -4779, 1600, 500, 100, floor2Color))
    objectList.append(Object(-5250, 10700, 2120, 300, 300, 300, floor2Color))
    objectList.append(Object(-4500, 100, -5679, 300, 6500, 1000, floor1Color))
    objectList.append(Object(-8200, 3300, -3779, 700, 100, 300, floor1Color))
    objectList.append(Object(-9450, 10600, 1720, 400, 400, 400, floor2Color))
    objectList.append(Object(-10100, 99, -6079, 10000, 10000, 100, floor1Color))
    objectList.append(Object(-3500, 4000, 320, 300, 500, 100, floor1Color))
    objectList.append(Object(-8400, 3900, -3979, 400, 100, 700, floor1Color))
    objectList.append(Object(-3450, 9900, 120, 100, 100, 200, floor1Color))
    objectList.append(Object(0, 19999, -5279, 1900, 100, 500, floor2Color))
    objectList.append(Object(-3450, 8300, -1079, 100, 100, 200, floor1Color))
    objectList.append(Object(-8850, 10600, 1720, 100, 2300, 400, floor2Color))
    objectList.append(Object(-4900, 4600, -5979, 700, 2000, 100, floor1Color))
    objectList.append(Object(-4850, 9100, -879, 1500, 1100, 1000, floor1Color))
    objectList.append(Object(-3500, 200, -2879, 300, 4300, 300, floor1Color))
    objectList.append(Object(-5300, 4400, -3379, 100, 1900, 1300, floor1Color))
    objectList.append(Object(-2500, 18399, -5079, 100, 1000, 100, floor2Color))
    objectList.append(Object(-3900, 6400, -679, 1000, 100, 600, floor1Color))
    objectList.append(Object(3699, 10299, -3679, 700, 400, 400, floor2Color))
    objectList.append(Object(-7600, 4000, 2520, 800, 100, 600, floor1Color))
    objectList.append(Object(-3500, 4000, -2579, 300, 500, 100, floor1Color))
    objectList.append(Object(-8000, -299, -5579, 100, 6900, 2100, floor1Color))
    objectList.append(Object(3699, 7999, -1979, 500, 2400, 400, floor1Color))
    objectList.append(Object(-6000, 4100, 3720, 100, 2100, 300, floor1Color))
    objectList.append(Object(-100, 10099, -5979, 100, 10000, 10000, floor2Color))
    objectList.append(Object(-10100, 10999, 2120, 300, 300, 400, floor2Color))
    objectList.append(Object(-8200, 0, -5979, 200, 4600, 2500, floor1Color))
    objectList.append(Object(-4950, 6500, -579, 100, 1800, 400, floor1Color))
    objectList.append(Object(-7100, 4600, -5979, 400, 2000, 300, floor1Color))
    objectList.append(Object(-3450, 7200, -1079, 100, 1100, 1400, floor1Color))
    objectList.append(Object(-3450, 8300, 120, 100, 100, 200, floor1Color))
    objectList.append(Object(-3200, 100, -5979, 300, 4000, 600, floor1Color))
    objectList.append(Object(-400, -399, -1979, 300, 5800, 900, floor1Color))
    objectList.append(Object(-200, 0, -5979, 100, 6500, 600, floor1Color))
    objectList.append(Object(-3500, 4000, 420, 300, 500, 100, floor1Color))
    objectList.append(Object(-3500, 4000, -2479, 300, 500, 100, floor1Color))
    objectList.append(Object(-4550, 10700, 820, 900, 1600, 900, floor2Color))
    objectList.append(Object(-3450, 9100, 120, 100, 100, 200, floor1Color))
    objectList.append(Object(-6550, 6500, -679, 100, 1800, 600, floor1Color))
    objectList.append(Object(-4950, 500, -1179, 100, 7800, 400, floor1Color))
    objectList.append(Object(-1650, 5400, -979, 800, 100, 1200, floor1Color))
    objectList.append(Object(-4800, 4600, -5779, 100, 2000, 100, floor1Color))
    objectList.append(Object(-3500, 4000, -2379, 300, 500, 100, floor1Color))
    objectList.append(Object(-3500, 4000, 520, 300, 500, 100, floor1Color))
    objectList.append(Object(-8200, 3400, -3779, 200, 1100, 300, floor1Color))
    objectList.append(Object(-3500, 4000, 720, 300, 500, 300, floor1Color))
    objectList.append(Object(-4950, 500, 20, 100, 7800, 400, floor1Color))
    objectList.append(Object(-4750, 11000, 1220, 200, 1000, 100, floor2Color))
    objectList.append(Object(-3600, 18299, -5379, 1600, 500, 100, floor2Color))
    objectList.append(Object(-200, 4700, -4779, 100, 100, 2100, floor1Color))
    objectList.append(Object(-6400, 4600, -5779, 300, 2000, 300, floor1Color))
    objectList.append(Object(-200, 4700, -2079, 100, 1799, 100, floor1Color))
    objectList.append(Object(-7000, 3300, -3279, 700, 100, 500, floor1Color))
    objectList.append(Object(-3450, 6500, -279, 100, 700, 600, floor1Color))
    objectList.append(Object(-5700, 3300, -3079, 900, 100, 700, floor1Color))
    objectList.append(Object(-3200, 18299, -5279, 1200, 100, 500, floor2Color))
    objectList.append(Object(-4250, 8300, -429, 200, 800, 100, floor1Color))
    objectList.append(Object(-3500, 4000, -2279, 300, 500, 100, floor1Color))
    objectList.append(Object(-10100, 10999, 1320, 300, 300, 400, floor2Color))
    objectList.append(Object(-10100, 3300, 2420, 800, 800, 800, floor1Color))
    objectList.append(Object(-2300, 100, -5579, 600, 4500, 200, floor1Color))
    objectList.append(Object(-4250, 18699, -5279, 500, 1100, 500, floor2Color))
    objectList.append(Object(-2900, 100, -5979, 600, 4500, 600, floor1Color))
    objectList.append(Object(-8750, 10600, 1620, 1100, 100, 600, floor2Color))
    objectList.append(Object(-3500, 4000, -2179, 300, 500, 2500, floor1Color))
    objectList.append(Object(-10100, 100, -3979, 10000, 100, 2000, floor1Color))
    objectList.append(Object(3699, -200, -1579, 500, 10600, 1900, floor1Color))
    objectList.append(Object(1799, 10099, -5279, 100, 9900, 500, floor2Color))
    objectList.append(Object(-3500, 4000, 620, 300, 500, 100, floor1Color))
    objectList.append(Object(-10200, 99, -5979, 100, 10000, 10000, floor1Color))
    objectList.append(Object(-6750, 200, -1279, 300, 7200, 300, floor1Color))
    objectList.append(Object(3799, 7799, -3279, 500, 5600, 400, floor1Color))
    objectList.append(Object(-4850, 10700, 820, 300, 300, 900, floor2Color))
    objectList.append(Object(-3450, 9125, -1079, 100, 100, 200, floor1Color))
    objectList.append(Object(-8000, 100, -5979, 1300, 4500, 300, floor1Color))
    objectList.append(Object(3699, 10299, -3279, 100, 400, 400, floor2Color))
    objectList.append(Object(-6050, 10400, 2420, 200, 200, 200, floor2Color))
    objectList.append(Object(-4900, 100, -5979, 1000, 4500, 600, floor1Color))
    objectList.append(Object(-7650, 10600, 1720, 100, 2300, 400, floor2Color))
    objectList.append(Object(-4200, 17899, -5179, 400, 1100, 300, floor2Color))
    objectList.append(Object(-9550, 10600, 1720, 100, 2300, 400, floor2Color))
    objectList.append(Object(-3450, 9900, -1079, 100, 100, 200, floor1Color))
    objectList.append(Object(-4850, 8200, -479, 1400, 100, 200, floor1Color))
    objectList.append(Object(-1750, 6500, -679, 100, 1800, 600, floor1Color))
    objectList.append(Object(-5400, 6400, -679, 1000, 100, 600, floor1Color))
    objectList.append(Object(-7150, 10600, 1720, 100, 2300, 400, floor2Color))
    objectList.append(Object(-5300, 4400, -2879, 1800, 100, 300, floor1Color))
    objectList.append(Object(-6700, 100, -5979, 1000, 4500, 600, floor1Color))
    objectList.append(Object(1799, 199, -5279, 100, 9900, 500, floor1Color))
    objectList.append(Object(-900, 100, -5979, 800, 4500, 200, floor1Color))
    objectList.append(Object(-3500, 4000, 1020, 300, 100, 1400, floor1Color))
    objectList.append(Object(-2200, 6400, -679, 1000, 100, 600, floor1Color))
    objectList.append(Object(-3450, 6500, -1079, 100, 700, 600, floor1Color))
    objectList.append(Object(-4850, 10200, -179, 300, 300, 300, floor2Color))
    objectList.append(Object(-10100, 10999, 1720, 300, 300, 400, floor2Color))
    objectList.append(Object(-3500, 4100, 1020, 300, 2000, 300, floor1Color))
    objectList.append(Object(-200, 0, -2679, 100, 4800, 600, floor1Color))
    objectList.append(Object(-7000, 6400, -679, 1000, 100, 600, floor1Color))
    objectList.append(Object(3699, 10299, -4079, 100, 400, 400, floor2Color))
    objectList.append(Object(-6450, 8200, -579, 1500, 100, 400, floor1Color))
    objectList.append(Object(3699, -200, 800, 500, 10600, 500, floor1Color))
    objectList.append(Object(-10100, 900, 3220, 800, 800, 800, floor1Color))
    objectList.append(Object(-5399, 600, 2520, 600, 100, 600, floor1Color))
    objectList.append(Object(-10100, 99, 4020, 10000, 10000, 100, floor1Color))
    objectList.append(Object(3699, 12799, -2029, 500, 400, 500, floor2Color))
    objectList.append(Object(-10100, 1900, 2420, 800, 400, 800, floor1Color))
    objectList.append(Object(-6800, 4000, 3720, 2800, 100, 300, floor1Color))
    objectList.append(Object(4299, 10299, -3279, 100, 400, 400, floor2Color))
    objectList.append(Object(-10100, 2700, 3220, 800, 400, 800, floor1Color))
    objectList.append(Object(-4000, 4000, 2720, 300, 100, 1300, floor1Color))
    objectList.append(Object(-10100, 0, -5979, 10000, 100, 10000, floor1Color))
    objectList.append(Object(-4000, 4000, 2420, 800, 100, 300, floor1Color))
    objectList.append(Object(-10100, 100, 2020, 10000, 800, 2000, floor1Color))
    objectList.append(Object(-10100, 100, 20, 10000, 400, 2000, floor1Color))
    objectList.append(Object(-7100, 4000, 3120, 300, 100, 900, floor1Color))
    objectList.append(Object(-5100, 4100, 3920, 1000, 800, 100, floor1Color))
    objectList.append(Object(4299, 10299, -4079, 100, 400, 400, floor2Color))
    objectList.append(Object(-10100, 3100, 3220, 200, 700, 800, floor1Color))

    return player, objectList, winpad
    
def loadToFG():
    pass

def tas(loadString=None):
    global time
    GHOST_COLOR = (0.0, 1.0, 1.0, 0.2)
    
    level = loadBasicJumps
    controller = Human()
    
    player, objectList, winpad = level()
    # rip ram what is this goofy ahh method
    inputArr = [0 for i in range(0, 100000)]
    stateArr = [player.clone() for i in range(0, 100000)]
    ghostStateArr = []
    
    if loadString is not None:
        loadIS = InputString(loadString, True)
        for i in range(0, len(loadIS.string)/3):
            inputArr[i] = int(loadIS.string[i*3:i*3+3])
        
    pygame.init()
    screen = pygame.display.set_mode((0, 0), pygame.DOUBLEBUF | pygame.OPENGL | pygame.FULLSCREEN)
    width, height = screen.get_size()
    clock = pygame.time.Clock()
    
    GL.glEnable(GL.GL_DEPTH_TEST)
    GL.glDisable(GL.GL_CULL_FACE)
    
    active = True

    verticalDirection = 90
    VERT_MIN = -90
    VERT_MAX = 90
    zoom = 1000
    zoomThirdPerson = True
    ZOOM_MIN = 400
    ZOOM_MAX = 20000
    
    ghostString = ""
    tasGhost = [Player(player.x, player.y, player.z, player.direction), InputString("tas1.txt", True)]
    
    # computing ghost state
    
    ghostWon = False
    time = 0
    ghostStateArr.append(tasGhost[0].clone())
    
    while not (ghostWon or time > 99999):
        ghostAction = tasGhost[1].getAction()
        ghostWon = tasGhost[0].doTick(ghostAction, objectList, winpad)
        time += 1
        ghostStateArr.append(tasGhost[0].clone())
    
    won = False
    printing = True
    
    time = 0
    
    while active:
        write = False
        continueFlag = False
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                active = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    write = True
                if event.key == pygame.K_PERIOD:
                    won = player.doTick(inputArr[time], objectList, winpad)
                    time += 1
                    stateArr[time] = player.clone()
                    continueFlag = True
                    if won:
                        active = False
                        ghostString = ""
                        for inp in inputArr:
                            ghostString += f"{inp:03d}"
                        ghostString = ghostString.rstrip('0')
                        with open("ghost.txt", "w") as file:
                            file.write(ghostString)
                if event.key == pygame.K_COMMA:
                    time -= 1
                    if time < 0:
                        time = 0
                    player = stateArr[time].clone()
                    continueFlag = True
                if event.key == pygame.K_q:
                    active = False
                if event.key == pygame.K_p:
                    ghostString = ""
                    for inp in inputArr:
                        ghostString += f"{inp:03d}"
                    ghostString = ghostString.rstrip('0')
                    with open("ghost.txt", 'w') as file:
                        file.write(ghostString)
                if event.key == pygame.K_j:
                    continueFlag = True
                    notFinished = True
                    
                    while notFinished:
                        won = player.doTick(inputArr[time], objectList, winpad)
                        time += 1
                        stateArr[time] = player.clone()
                        if inputArr[time] == 0:
                            notFinished = False
                if event.key == pygame.K_0:
                    time = 0
                    player = stateArr[time].clone()
                    continueFlag = True
                if event.key == pygame.K_1:
                    time -= 10
                    if time < 0:
                        time = 0
                    player = stateArr[time].clone()
                    continueFlag = True
                if event.key == pygame.K_2:
                    time -= 100
                    if time < 0:
                        time = 0
                    player = stateArr[time].clone()
                    continueFlag = True
                if event.key == pygame.K_3:
                    time -= 1000
                    if time < 0:
                        time = 0
                    player = stateArr[time].clone()
                    continueFlag = True

                # inputs 
                if event.key == pygame.K_SPACE:
                    inputArr[time] ^= 1
                if event.key == pygame.K_a:
                    inputArr[time] ^= 2
                if event.key == pygame.K_d:
                    inputArr[time] ^= 4
                if event.key == pygame.K_w:
                    inputArr[time] ^= 8
                if event.key == pygame.K_s:
                    inputArr[time] ^= 16
                if event.key == pygame.K_LEFT:
                    inputArr[time] ^= 32
                if event.key == pygame.K_RIGHT:
                    inputArr[time] ^= 64
        
        if continueFlag:
            continue
        
        keys = pygame.key.get_pressed()
        if keys[pygame.K_MINUS]:
            if zoomThirdPerson:
                zoom *= 1.04
                if zoom > ZOOM_MAX:
                    zoom = ZOOM_MAX
            else:
                zoomThirdPerson = True
        if keys[pygame.K_EQUALS]:
            if zoomThirdPerson:
                zoom *= 0.961
                if zoom < ZOOM_MIN:
                    zoom = ZOOM_MIN
                    zoomThirdPerson = False
        if keys[pygame.K_DOWN]:
            verticalDirection += 2
            if verticalDirection > VERT_MAX:
                verticalDirection = VERT_MAX
        if keys[pygame.K_UP]:
            verticalDirection -= 2
            if verticalDirection < VERT_MIN:
                verticalDirection = VERT_MIN
        
        action = inputArr[time]
        
        GL.glLoadIdentity()
        GLU.gluPerspective(45, width/height, 0.1, 1000000.0)
        GL.glRotatef(verticalDirection, 1, 0, 0)
        GL.glRotatef(player.direction, 0, 1, 0)
        
        if zoomThirdPerson:
        #x, z
            backVector = (-math.sin(math.radians(player.direction)), math.cos(math.radians(player.direction)))
            backComponent = math.cos(math.radians(verticalDirection))
            yComponent = math.sin(math.radians(verticalDirection))
        
            xShift = zoom * backVector[0] * backComponent
            yShift = zoom * yComponent
            zShift = zoom * backVector[1] * backComponent
        
            GL.glTranslatef(-player.x-xShift-50, -player.y-yShift-250, -player.z-zShift-50)
        else:
            GL.glTranslatef(-player.x-50, -player.y-250, -player.z-50)
    
        GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)
        
        if time < len(ghostStateArr):
            ghostMinCorner = (ghostStateArr[time].x, ghostStateArr[time].y, ghostStateArr[time].z)
            ghostMaxCorner = (ghostStateArr[time].x+Player.LENGTH, ghostStateArr[time].y+Player.HEIGHT, ghostStateArr[time].z+Player.WIDTH)
            drawCuboid(ghostMinCorner, ghostMaxCorner, GL.GL_TRIANGLES, GHOST_COLOR)
        
        if zoomThirdPerson:
            playerMinCorner = (player.x, player.y, player.z)
            playerMaxCorner = (player.x+Player.LENGTH, player.y+Player.HEIGHT, player.z+Player.WIDTH)
            drawCuboid(playerMinCorner, playerMaxCorner, GL.GL_TRIANGLES, Player.COLOR)

        winpadMinCorner = (winpad.x, winpad.y, winpad.z)
        winpadMaxCorner = (winpad.x+winpad.length, winpad.y+winpad.height, winpad.z+winpad.width)
        drawCuboid(winpadMinCorner, winpadMaxCorner, GL.GL_TRIANGLES, winpad.color)
        for obj in objectList:
            objMinCorner = (obj.x, obj.y, obj.z)
            objMaxCorner = (obj.x+obj.length, obj.y+obj.height, obj.z+obj.width)
            drawCuboid(objMinCorner, objMaxCorner, GL.GL_TRIANGLES, obj.color)
        
        if zoomThirdPerson:
            drawCuboid(playerMinCorner, playerMaxCorner, color=(0.0, 0.0, 0.0, 1.0))

        if time < len(ghostStateArr):
            ghostMinCorner = (ghostStateArr[time].x, ghostStateArr[time].y, ghostStateArr[time].z)
            ghostMaxCorner = (ghostStateArr[time].x+Player.LENGTH, ghostStateArr[time].y+Player.HEIGHT, ghostStateArr[time].z+Player.WIDTH)
            drawCuboid(ghostMinCorner, ghostMaxCorner, color=(0.0, 0.0, 0.0, 1.0))

        drawCuboid(winpadMinCorner, winpadMaxCorner)
        for obj in objectList:
            objMinCorner = (obj.x, obj.y, obj.z)
            objMaxCorner = (obj.x+obj.length, obj.y+obj.height, obj.z+obj.width)
            drawCuboid(objMinCorner, objMaxCorner)
        
        drawInputOverlay(action, width, height)
        
        pygame.display.flip()   
        clock.tick(60)

def play():
    GHOST_COLOR = (0.0, 1.0, 1.0, 0.2)
    
    global time
    level = loadSNFA
    player, objectList, winpad = level()
    controller = Human()
    
    pygame.init()
    screen = pygame.display.set_mode((0, 0), pygame.DOUBLEBUF | pygame.OPENGL | pygame.FULLSCREEN)
    width, height = screen.get_size()
    clock = pygame.time.Clock()
    
    GL.glEnable(GL.GL_DEPTH_TEST)
    GL.glDisable(GL.GL_CULL_FACE)
    
    active = True
    reset = False
    
    time = 0
    verticalDirection = 90
    VERT_MIN = -90
    VERT_MAX = 90
    zoom = 1000
    zoomThirdPerson = True
    ZOOM_MIN = 400
    ZOOM_MAX = 20000
    
    ghostString = ""
    ghostList = []
    for i in range(1, 6):
        ghostList.append([Player(player.x, player.y, player.z, player.direction), InputString(f"towerpbs/pbtower{i}.txt", True)])
    
    won = False
    printing = True
    
    while active:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                active = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    reset = True
                if event.key == pygame.K_q:
                    active = False
                if event.key == pygame.K_p:
                    with open("ghost.txt", 'w') as file:
                        file.write(ghostString)
        
        if reset:
            reset = False
            player, objectList, winpad = level()
            time = 0
            won = False
            printing = True
            ghostString = ""
            for ghost in ghostList:
                ghost[0] = Player(player.x, player.y, player.z, player.direction)
            continue
        
        keys = pygame.key.get_pressed()
        if keys[pygame.K_MINUS]:
            if zoomThirdPerson:
                zoom *= 1.04
                if zoom > ZOOM_MAX:
                    zoom = ZOOM_MAX
            else:
                zoomThirdPerson = True
        if keys[pygame.K_EQUALS]:
            if zoomThirdPerson:
                zoom *= 0.961
                if zoom < ZOOM_MIN:
                    zoom = ZOOM_MIN
                    zoomThirdPerson = False
        if keys[pygame.K_DOWN]:
            verticalDirection += 2
            if verticalDirection > VERT_MAX:
                verticalDirection = VERT_MAX
        if keys[pygame.K_UP]:
            verticalDirection -= 2
            if verticalDirection < VERT_MIN:
                verticalDirection = VERT_MIN
        
        for ghost in ghostList:
            ghostAction = ghost[1].getAction()
            finished = ghost[0].doTick(ghostAction, objectList, winpad)
            if finished:
                ghost[0].x = -999999
        
        action = controller.getAction()
        ghostString += f"{action:03d}"
        time += 1
        won = player.doTick(action, objectList, winpad)
        
        GL.glLoadIdentity()
        GLU.gluPerspective(45, width/height, 0.1, 1000000.0)
        GL.glRotatef(verticalDirection, 1, 0, 0)
        GL.glRotatef(player.direction, 0, 1, 0)
        
        if zoomThirdPerson:
        #x, z
            backVector = (-math.sin(math.radians(player.direction)), math.cos(math.radians(player.direction)))
            backComponent = math.cos(math.radians(verticalDirection))
            yComponent = math.sin(math.radians(verticalDirection))
        
            xShift = zoom * backVector[0] * backComponent
            yShift = zoom * yComponent
            zShift = zoom * backVector[1] * backComponent
        
            GL.glTranslatef(-player.x-xShift-50, -player.y-yShift-250, -player.z-zShift-50)
        else:
            GL.glTranslatef(-player.x-50, -player.y-250, -player.z-50)
    
        GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)
        
        for ghost in ghostList:
            ghostMinCorner = (ghost[0].x, ghost[0].y, ghost[0].z)
            ghostMaxCorner = (ghost[0].x+Player.LENGTH, ghost[0].y+Player.HEIGHT, ghost[0].z+Player.WIDTH)
            drawCuboid(ghostMinCorner, ghostMaxCorner, GL.GL_TRIANGLES, GHOST_COLOR)
        
        if zoomThirdPerson:
            playerMinCorner = (player.x, player.y, player.z)
            playerMaxCorner = (player.x+Player.LENGTH, player.y+Player.HEIGHT, player.z+Player.WIDTH)
            drawCuboid(playerMinCorner, playerMaxCorner, GL.GL_TRIANGLES, Player.COLOR)
        winpadMinCorner = (winpad.x, winpad.y, winpad.z)
        winpadMaxCorner = (winpad.x+winpad.length, winpad.y+winpad.height, winpad.z+winpad.width)
        drawCuboid(winpadMinCorner, winpadMaxCorner, GL.GL_TRIANGLES, winpad.color)
        for obj in objectList:
            objMinCorner = (obj.x, obj.y, obj.z)
            objMaxCorner = (obj.x+obj.length, obj.y+obj.height, obj.z+obj.width)
            drawCuboid(objMinCorner, objMaxCorner, GL.GL_TRIANGLES, obj.color)
        
        if zoomThirdPerson:
            drawCuboid(playerMinCorner, playerMaxCorner, color=(0.0, 0.0, 0.0, 1.0))
        for ghost in ghostList:
            ghostMinCorner = (ghost[0].x, ghost[0].y, ghost[0].z)
            ghostMaxCorner = (ghost[0].x+Player.LENGTH, ghost[0].y+Player.HEIGHT, ghost[0].z+Player.WIDTH)
            drawCuboid(ghostMinCorner, ghostMaxCorner, color=(0.0, 0.0, 0.0, 1.0))
        drawCuboid(winpadMinCorner, winpadMaxCorner)
        for obj in objectList:
            objMinCorner = (obj.x, obj.y, obj.z)
            objMaxCorner = (obj.x+obj.length, obj.y+obj.height, obj.z+obj.width)
            drawCuboid(objMinCorner, objMaxCorner)
        
        drawInputOverlay(action, width, height)
        
        if won:
            with open("ghost.txt", 'w') as file:
                file.write(ghostString)
            active = False
        
        pygame.display.flip()   
        clock.tick(60)
    
def main():
    play()

if __name__ == "__main__":
    main()


