import pygame
import time as t # bum used time as a var
import json
import socket

class Player:
  WIDTH = 100
  HEIGHT = 100
  MOVE_ACCEL = 4
  FALL_ACCEL = 3
  JUMP_ACCEL = 45
  FRIC_MULT = 0.85

  __slots__ = ("x", "y", "velX", "velY")

  def __init__(self, x, y):
    self.x = x
    self.y = y
    self.velX = 0
    self.velY = 0
    
# actions
# 0 - nothing
# 1 - jump
# 2 - left
# 3 - jump left
# 4 - right
# 5 - jump right

  def doTick(self, action, objectList, winpad):
    oldX = self.x
    oldY = self.y
    jumpAttempted = action & 1
    if jumpAttempted:
      action -= 1
    if action == 2:
      self.velX -= Player.MOVE_ACCEL
    elif action == 4:
      self.velX += Player.MOVE_ACCEL
        
    self.velX = int(self.velX * Player.FRIC_MULT)
    self.velY -= Player.FALL_ACCEL
    self.x += self.velX
    self.y += self.velY
        
    uncheckedCollisions = True
    collisionCap = 10
    while uncheckedCollisions and collisionCap > 0:
      collisionCap -= 1
      uncheckedCollisions = False
      for obj in objectList:
      # AABB check
            
        xCollide = (self.x < (obj.x + obj.width)) and (obj.x < (self.x + Player.WIDTH))
        yCollide = (self.y < (obj.y + obj.height)) and (obj.y < (self.y + Player.HEIGHT))
              
        if xCollide and yCollide:
          uncheckedCollisions = True
          if oldY >= (obj.y+obj.height):
            self.y = obj.y+obj.height
            self.velY = 0
            if jumpAttempted:
              self.velY = Player.JUMP_ACCEL
          elif (oldX+Player.WIDTH) <= obj.x:
            self.x = obj.x-Player.WIDTH
            self.velX = 0
          elif oldX >= (obj.x+obj.width):
            self.x = obj.x+obj.width
            self.velX = 0
          else:
            self.y = obj.y-Player.HEIGHT
            self.velY = 0

    xCollide = (self.x <= (winpad.x + winpad.width)) and (winpad.x <= (self.x + Player.WIDTH))
    yCollide = (self.y <= (winpad.y + winpad.height)) and (winpad.y <= (self.y + Player.HEIGHT))
    if xCollide and yCollide:
      return 1
    else:
      return 0
  
  def clone(self):
    playerClone = Player(self.x, self.y)
    playerClone.velX = self.velX
    playerClone.velY = self.velY
    return playerClone

class Object:
    
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

class Human:
    
    def __init__(self):
        pass
    
    def getAction(self):
        action = 0

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            action = 2
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            if action == 2:
                action = 0
            else:
                action = 4
        if keys[pygame.K_SPACE] or keys[pygame.K_UP]:
            action += 1
            
        return action
    
class InputString:

    def __init__(self, string=None, fromText=False):
      self.string = ""
      if fromText:
        with open(string, 'r') as file:
            self.string = file.read()
      elif string:
        self.string = string
    
    def loadStringFromTxt(self, filename):
        with open(filename, 'r') as file:
            self.string = file.read()

    def getAction(self):
        global time
        if len(self.string) > time:
            return int(self.string[time])
        else:
            return 0
    
    
def loadTrivial1():
    player = Player(0, 0)
    winpad = Object(200, 0, 200, 1000)
    objectList = []
    objectList.append(Object(-1000, -1000, 2000, 1000))
    objectList.append(Object(-1100, -1000, 100, 2000))
    return player, objectList, winpad

def loadTrivial2():
    player = Player(0, 0)
    winpad = Object(2000, 0, 200, 1000)
    objectList = []
    objectList.append(Object(-10000, -1000, 20000, 1000))
    objectList.append(Object(-10100, -1000, 100, 2000))
    objectList.append(Object(300, 0, 500, 150))
    objectList.append(Object(1300, 0, 500, 150))
    return player, objectList, winpad

def loadSemiTrivial1():
  player = Player(0, 0)
  winpad = Object(1500, 500, 200, 1000)
  objectList = []
  objectList.append(Object(-10000, -1000, 20000, 1000))
  objectList.append(Object(-10100, -1000, 100, 2000))
  objectList.append(Object(700, 0, 200, 500))
  objectList.append(Object(600, 150, 100, 100))
  objectList.append(Object(900, 300, 1000, 200))
  return player, objectList, winpad

def loadSemiTrivial2():
  player = Player(0, 0)
  winpad = Object(1500, 700, 200, 1000)
  objectList = []
  objectList.append(Object(-10000, -1000, 20000, 1000))
  objectList.append(Object(-10100, -1000, 100, 2000))
  objectList.append(Object(1000, 0, 200, 700))
  objectList.append(Object(1200, 500, 1000, 200))
  objectList.append(Object(200, 350, 200, 3000))
  objectList.append(Object(800, 100, 200, 100))
  objectList.append(Object(400, 350, 200, 100))
  objectList.append(Object(800, 600, 200, 100))
  return player, objectList, winpad

def loadNonTrivial1():
  player = Player(0, 0)
  winpad = Object(10000, 0, 200, 1000)
  objectList = []
  objectList.append(Object(-1000, -200, 105000, 200))
  objectList.append(Object(-1000, 0, 200, 1000))
  objectList.append(Object(8000, 0, 200, 2050))
  objectList.append(Object(2000, 200, 400, 50))
  objectList.append(Object(2800, 400, 400, 50))
  objectList.append(Object(2900, 450, 200, 200))
  objectList.append(Object(3150, 0, 50, 400))
  objectList.append(Object(3200, 150, 50, 50))
  objectList.append(Object(3300, 700, 50, 1000))
  objectList.append(Object(3350, 700, 4000, 50))
  objectList.append(Object(7350, 700, 50, 3000))
  objectList.append(Object(3400, 500, 400, 50))
  objectList.append(Object(4000, 400, 300, 50))
  objectList.append(Object(4500, 400, 500, 50))
  objectList.append(Object(4650, 400, 50, 180))
  objectList.append(Object(4850, 400, 50, 180))
  objectList.append(Object(5200, 300, 500, 50))
  objectList.append(Object(5180, 500, 50, 200))
  objectList.append(Object(5800, 450, 1000, 50))
  objectList.append(Object(7000, 450, 1000, 50))
  objectList.append(Object(7800, 600, 200, 50))
  objectList.append(Object(7400, 800, 200, 50))
  objectList.append(Object(7400, 1100, 100, 50))
  objectList.append(Object(7900, 1200, 100, 50))
  objectList.append(Object(7950, 1500, 50, 50))
  objectList.append(Object(7400, 1700, 200, 50))
  objectList.append(Object(7400, 1750, 150, 100))
  objectList.append(Object(8800, 200, 50, 3000))
  objectList.append(Object(8200, 2000, 450, 50))
  objectList.append(Object(8350, 1800, 450, 50))
  objectList.append(Object(8200, 1300, 450, 50))
  objectList.append(Object(8400, 1350, 250, 200))
  objectList.append(Object(8200, 900, 225, 50))
  objectList.append(Object(8575, 900, 225, 50))
  objectList.append(Object(8575, 900, 50, 250))
  objectList.append(Object(8375, 1050, 50, 100))
  objectList.append(Object(8425, 1100, 200, 50))
  objectList.append(Object(8350, 700, 450, 50))
  objectList.append(Object(8200, 500, 450, 50))
  objectList.append(Object(8350, 300, 450, 50))
  return player, objectList, winpad

def loadNonTrivial2():
  pass

def tas(): # right/left arrow to change frame press/hold w to write input s to save q to quit
  global time
  
  inputArr = [0 for i in range(0, 10000)]
  stateArr = [Player(0, 0) for i in range(0, 10000)]
  ghostStateArr = []
  time = 0
  
  player, objectList, winpad = loadNonTrivial1()
  controller = Human()
  
  pygame.init()
  screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
  clock = pygame.time.Clock()
  font = pygame.font.SysFont("Arial", 40)
  
  active = True
  
  ZOOM = 0.5
  tasGhost = [Player(0, 0), InputString("tas.txt", True)]
  ghostSurface = pygame.Surface((Player.WIDTH*ZOOM, Player.HEIGHT*ZOOM), pygame.SRCALPHA)
  ghostSurface.fill((0, 255, 255, 85))
  
  # computing ghost state
  
  ghostWon = False
  time = 0
  ghostStateArr.append(tasGhost[0].clone())
  
  while not (ghostWon or time > 9990):
    ghostAction = tasGhost[1].getAction()
    ghostWon = tasGhost[0].doTick(ghostAction, objectList, winpad)
    time += 1
    ghostStateArr.append(tasGhost[0].clone())
  
  time = 0
  while active:
    clock.tick(60)

    write = False
    continueFlag = False
    
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        active = False
      if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_w:
          write = True
        if event.key == pygame.K_RIGHT:
          won = player.doTick(inputArr[time], objectList, winpad)
          time += 1
          stateArr[time] = player.clone()
          continueFlag = True
          if won:
            active = False
            ghostString = ""
            for inp in inputArr:
              ghostString += str(inp)
            with open("tas.txt", "w") as file:
              file.write(ghostString)
        if event.key == pygame.K_LEFT:
          time -= 1
          player = stateArr[time].clone()
          continueFlag = True
        if event.key == pygame.K_s:
          ghostString = ""
          for inp in inputArr:
            ghostString += str(inp)
          with open("tas.txt", "w") as file:
            file.write(ghostString)
        if event.key == pygame.K_q:
          active = False
    
    if continueFlag:
      continue
    
    screen.fill(pygame.Color("white"))
        
    width, height = screen.get_size()
    camX = player.x - (width/2)/ZOOM + (Player.WIDTH/2)
    camY = player.y + (3*height/4)/ZOOM - (Player.HEIGHT/2)
    
    action = inputArr[time]
    if write:
      action = controller.getAction()
      inputArr[time] = action
    
    if time < len(ghostStateArr):
      screen.blit(ghostSurface, ((ghostStateArr[time].x-camX)*ZOOM, (camY-ghostStateArr[time].y-Player.HEIGHT)*ZOOM))

    playerRect = pygame.Rect((player.x-camX)*ZOOM, (camY-player.y-Player.HEIGHT)*ZOOM, Player.WIDTH*ZOOM, Player.HEIGHT*ZOOM)
    pygame.draw.rect(screen, pygame.Color("black"), playerRect)
        
    winpadRect = pygame.Rect((winpad.x-camX)*ZOOM, (camY-winpad.y-winpad.height)*ZOOM, winpad.width*ZOOM, winpad.height*ZOOM)
    pygame.draw.rect(screen, pygame.Color("green"), winpadRect)
        
    for obj in objectList:
      objRect = pygame.Rect((obj.x-camX)*ZOOM, (camY-obj.y-obj.height)*ZOOM, obj.width*ZOOM, obj.height*ZOOM)
      pygame.draw.rect(screen, pygame.Color("blue"), objRect)
                
    text_surface = font.render(f"({int(player.x)}, {int(player.y)})", True, pygame.Color("red"))
    text_rect = text_surface.get_rect(topleft=(0, 0))
    screen.blit(text_surface, text_rect)
    
    text_surface = font.render(f"Frame: {time}", True, pygame.Color("red"))
    text_rect = text_surface.get_rect(topleft=(0, 50))
    screen.blit(text_surface, text_rect)
    
    actionString = "Action: "
    if action == 0:
      actionString += ""
    elif action == 1:
      actionString += "Jump"
    elif action == 2:
      actionString += "Left"
    elif action == 3:
      actionString += "Jump Left"
    elif action == 4:
      actionString += "Right"
    elif action == 5:
      actionString += "Jump Right"
    
    text_surface = font.render(actionString, True, pygame.Color("red"))
    text_rect = text_surface.get_rect(topleft=(0, 100))
    screen.blit(text_surface, text_rect)
    
    pygame.display.flip()

def play(level):
  global time

  player, objectList, winpad = level()
  controller = Human()
  #controller = InputString("44444444444444444444444444444444444444444444444444444444444444444444444444444444555555555555555555555555555555554444444444444444444444444444444455555555555555555555555555555555444444444444444411111111111111110000000000000000555555555555555544444444444444444444444444444444444444444444444455555555555555554444444444444444555555555555555555555555555555554444444444444444444444444444444455555555555555554444444444444444444444444444444455555555555555555555555555555555444444444444444444444444444444445555555555555555000000000000000033333333333333331111111111111111222222222222222255555555555555555555555555555555333333333333333344444444444444441111111111111111444444444444444433333333333333332222222222222222333333333333333355555555555555554444444444444444444444444444444444444444444444444444444444444444222222222222222233333333333333335555555555555555444444444444444444444444444444440000000000000000333333333333333333333333333333334444444444444444444444444444444422222222222222222222222222222222444444444444444444444444444444442222222222222222222222222222222200000000000000004444444444444444444444444444444444444444444444444444444444444444444444444444444444444444444444444444444444444444")
  
  ghostList = []#[Player(0, 0), InputString("pb.txt", True)]]
  with open("backupInfo.txt", 'r') as file:
    for line in file:
      ghostList.append([Player(0, 0), InputString(line.rstrip('\n'))])
    
  pygame.init()
  screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
  clock = pygame.time.Clock()
  font = pygame.font.SysFont("Arial", 40)
    
  active = True
  state = 0
  time = -60
  subFrame = 0.0
  ghostString = ""
    
  ZOOM = 0.5
  ghostSurface = pygame.Surface((Player.WIDTH*ZOOM, Player.HEIGHT*ZOOM), pygame.SRCALPHA)
  ghostSurface.fill((0, 255, 255, 85))
  
  while(active):
        clock.tick(60)
        reset = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                active = False
            if event.type == pygame.KEYDOWN:
              if event.key == pygame.K_r:
                reset = True
              if event.key == pygame.K_q:
                active = False
        
        if(reset):
          player = Player(0, 0)
          for ghost in ghostList:
            ghost[0] = Player(0, 0)
          state = 0
          time = -60
          subFrame = 0.0
          ghostString = ""
          continue
        
        screen.fill(pygame.Color("white"))
        
        width, height = screen.get_size()
        camX = player.x - (width/2)/ZOOM + (Player.WIDTH/2)
        camY = player.y + (3*height/4)/ZOOM - (Player.HEIGHT/2)
        
        if state == 0:
            time += 1
            text_surface = font.render(str(time), True, pygame.Color("black"))
            text_rect = text_surface.get_rect(center=(width // 2, height // 2))
            screen.blit(text_surface, text_rect)
            if time == 0:
                state = 1
        elif state == 1:
            action = controller.getAction()
            for ghost in ghostList:
              ghostAction = ghost[1].getAction()
              finished = ghost[0].doTick(ghostAction, objectList, winpad)
              screen.blit(ghostSurface, ((ghost[0].x-camX)*ZOOM, (camY-ghost[0].y-Player.HEIGHT)*ZOOM))
              if finished:
                ghost[0].x = -999999
              
            time += 1
            ghostString += str(action)
            won = player.doTick(action, objectList, winpad)
            
            playerRect = pygame.Rect((player.x-camX)*ZOOM, (camY-player.y-Player.HEIGHT)*ZOOM, Player.WIDTH*ZOOM, Player.HEIGHT*ZOOM)
            pygame.draw.rect(screen, pygame.Color("black"), playerRect)
        
            winpadRect = pygame.Rect((winpad.x-camX)*ZOOM, (camY-winpad.y-winpad.height)*ZOOM, winpad.width*ZOOM, winpad.height*ZOOM)
            pygame.draw.rect(screen, pygame.Color("green"), winpadRect)
        
            for obj in objectList:
                objRect = pygame.Rect((obj.x-camX)*ZOOM, (camY-obj.y-obj.height)*ZOOM, obj.width*ZOOM, obj.height*ZOOM)
                pygame.draw.rect(screen, pygame.Color("blue"), objRect)
                
            text_surface = font.render(f"({int(player.x)}, {int(player.y)})", True, pygame.Color("black"))
            text_rect = text_surface.get_rect(topleft=(0, 0))
            screen.blit(text_surface, text_rect)
            
            if won:
                overDistance = player.x+Player.WIDTH-winpad.x
                subFrame = 1000 - int((overDistance / player.velX)*1000)
                state = 2
                with open("ghost.txt", 'w') as file:
                  file.write(ghostString)
        else:
            if subFrame == 1000:
              text_surface = font.render(f"Finished in {time} ({time}.) frames", True, pygame.Color("black"))
            else:
              text_surface = font.render(f"Finished in {time} ({time-1}.{subFrame}) frames", True, pygame.Color("black"))
            text_rect = text_surface.get_rect(center=(width // 2, height // 2))
            screen.blit(text_surface, text_rect)
        
        pygame.display.flip()
    
  pygame.quit()