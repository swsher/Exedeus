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
  FRIC_MULT = 0.80
    
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
        
    self.velX *= Player.FRIC_MULT
    self.velY -= Player.FALL_ACCEL
    self.x += self.velX
    self.y += self.velY
        
    uncheckedCollisions = True
    while uncheckedCollisions:
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
    return player, objectList, winpad

def loadTrivial2():
    player = Player(0, 0)
    winpad = Object(2000, 0, 200, 1000)
    objectList = []
    objectList.append(Object(-10000, -1000, 20000, 1000))
    objectList.append(Object(300, 0, 500, 150))
    objectList.append(Object(1300, 0, 500, 150))
    return player, objectList, winpad

def loadSemiTrivial1():
  player = Player(0, 0)
  winpad = Object(1500, 500, 200, 1000)
  objectList = []
  objectList.append(Object(-10000, -1000, 20000, 1000))
  objectList.append(Object(700, 0, 200, 500))
  objectList.append(Object(600, 150, 100, 100))
  objectList.append(Object(900, 300, 1000, 200))
  return player, objectList, winpad

def loadSemiTrivial2():
  player = Player(0, 0)
  winpad = Object(1500, 700, 200, 1000)
  objectList = []
  objectList.append(Object(-10000, -1000, 20000, 1000))
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

def play():
  global time

  player, objectList, winpad = loadNonTrivial1()
  controller = Human()
  
  ghostList = [[Player(0, 0), InputString("pb.txt", True)]]
  #for i in range(386):
    #filename = "lis" + str(i)
    #ghostList.append([Player(0, 0), InputString(filename, True)])
    
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

def bruteForce(loadFunc, maxDepth=100):
  global time
  
  currentString = "0"*maxDepth
  currentIter = 0
  
  bestString = None
  bestDecTime = 99999999.0
  
  active = True
  startTime = t.time()
  
  while active:
    currentIter += 1
    if currentIter % 100000 == 0:
      elapsedTime = t.time() - startTime
      ips = currentIter / elapsedTime
      print(f"\nCurrent Iteration: {currentIter} IPS: {ips}")
    
    player, objectList, winpad = loadFunc()
    controller = InputString(currentString)
    time = 0
    won = False
    
    while not ((time > maxDepth) or won):
      action = controller.getAction()
      won = player.doTick(action, objectList, winpad)
      time += 1
    
    if won:
      overDistance = player.x+Player.WIDTH-winpad.x
      subFrame = (1000 - int((overDistance / player.velX)*1000))/1000
      decimalTime = (time - 1) + subFrame
      
      if decimalTime < bestDecTime:
        bestDecTime = decimalTime
        trimmedString = currentString[:time]
        maxDepth = time
        print(f"\n\n\nInputString: {trimmedString}\nTime: {decimalTime} frames\nIteration: {currentIter}")
        bestDecTime = decimalTime
        bestString = trimmedString
    
    else:
      decimalTime = 1.0 * (100000 - player.x)
      if decimalTime < bestDecTime:
        bestDecTime = decimalTime
        trimmedString = currentString[:time]
        maxDepth = time
        print(f"\n\n\nInputString: {trimmedString}\nDistance: {player.x} units\nIteration: {currentIter}")
        bestDecTime = decimalTime
        bestString = trimmedString
    
    incrIndex = 0
    while incrIndex < maxDepth:
      active = False
      if currentString[incrIndex] == "5":
        currentString = currentString[:incrIndex] + "0" + currentString[incrIndex+1:]
        incrIndex += 1
      else:
        currentString = currentString[:incrIndex] + str(int(currentString[incrIndex])+1) + currentString[incrIndex+1:]
        active = True
        break
  
  return bestString

def bruteForceLIS(loadFunc, maxDepth=200, maxInputs=100, saveAll=False):
  global time
  
  numWins = 0
  
  inputs = [0]
  changePoints = []
  currentIter = 0
  
  bestString = None
  bestDecTime = 99999999.0
  
  active = True
  startTime = t.time()
  
  while active:
    currentIter += 1
    if currentIter % 200 == 0:
      elapsedTime = t.time() - startTime
      ips = currentIter / elapsedTime
      print(f"\nCurrent Iteration: {currentIter} IPS: {ips}")
      print(inputs)
    
    player, objectList, winpad = loadFunc()
    currentString = ""
    
    strIndex = 0
    changePointIndex = 0
    changePoint = 0
    for inp in inputs:
      if changePointIndex == len(changePoints):
        changePoint = maxDepth
      else:
        changePoint = changePoints[changePointIndex]
        changePointIndex += 1
      while strIndex < changePoint:
        currentString += str(inp)
        strIndex += 1
    
    controller = InputString(currentString)
    time = 0
    won = False
    
    while not ((time > maxDepth) or won):
      action = controller.getAction()
      won = player.doTick(action, objectList, winpad)
      time += 1
    
    if won:
      overDistance = player.x+Player.WIDTH-winpad.x
      subFrame = (1000 - int((overDistance / player.velX)*1000))/1000
      decimalTime = (time - 1) + subFrame
      
      trimmedString = currentString[:time]
      
      if saveAll:
        filename = "lis" + str(numWins)
        with open(filename, "w") as file:
          file.write(trimmedString)
      
      if decimalTime < bestDecTime:
        bestDecTime = decimalTime
        print(f"\n\n\nInputString: {trimmedString}\nTime: {decimalTime} frames\nIteration: {currentIter}")
        bestString = trimmedString
      
      numWins += 1
    
    else:
      decimalTime = 1.0 * (100000 - player.x)
      if decimalTime < bestDecTime:
        bestDecTime = decimalTime
        trimmedString = currentString[:time]
        maxDepth = time
        print(f"\n\n\nInputString: {trimmedString}\nDistance: {player.x} units\nIteration: {currentIter}")
        bestDecTime = decimalTime
        bestString = trimmedString
    
    updateInput = True
    changePointIndex = len(changePoints) - 1
    changePointBuffer = 0
    while changePointIndex >= 0:
      if changePoints[changePointIndex] == maxDepth-changePointBuffer:
        changePointIndex -= 1
        changePointBuffer += 1
      else:
        changePoints[changePointIndex] += 1
        base = changePoints[changePointIndex] + 1
        changePointIndex += 1
        while changePointIndex < len(changePoints):
          changePoints[changePointIndex] = base
          changePointIndex += 1
          base += 1
        updateInput = False
        break
      
    addInput = False
    if updateInput:
      addInput = True
      incrIndex = len(inputs)-1
      while incrIndex >= 0:
        if inputs[incrIndex] == 5:
          if not incrIndex == 0 and inputs[incrIndex-1] == 0 and (not incrIndex == 1):
            inputs[incrIndex] = 1
          else:
            inputs[incrIndex] = 0
          incrIndex -= 1
        else:
          inputs[incrIndex] += 1
          if not incrIndex == 0 and inputs[incrIndex-1] == inputs[incrIndex]:
            continue
          addInput = False
          break
      for i in range(len(changePoints)):
        changePoints[i] = i+1
    
    if addInput:
      numInputs = len(inputs)
      print(f"\nAll {numInputs} input strings finished")
      if len(inputs) == maxInputs:
        active = False
      else:
        inputs.append(0)
        for i in range(len(inputs)):
          if i % 2 == 0:
            inputs[i] = 0
          else:
            inputs[i] = 1
        changePoints.append(0)
        for i in range(len(changePoints)):
          changePoints[i] = i+1
  
  print(numWins)
  return bestString

def greedySolve(loadFunc, maxDepth=1000):
  global time
  
  bestDecTime = 9999999999.0
  currentDecTime = bestDecTime-1
  startTime = t.time()
  
  baseString = "0"*maxDepth
  currentString = baseString
  currentBestString = baseString
  currentIter = 0
  
  while bestDecTime > currentDecTime:
    baseString = currentBestString
    bestDecTime = currentDecTime
    alteration = [0, 0] # value, index
    while True:
      currentIter += 1
      if currentIter % 100000 == 0:
        elapsedTime = t.time() - startTime
        ips = currentIter / elapsedTime
        print(f"\nCurrent Iteration: {currentIter} IPS: {ips}")
    
      player, objectList, winpad = loadFunc()
      
      if str(alteration[0]) == baseString[alteration[1]]:
        if alteration[0] == 5:
          alteration[0] = 0
          alteration[1] += 1
          if alteration[1] >= maxDepth:
            break
        else:
          alteration[0] += 1
        continue
      
      currentString = baseString
      currentString = currentString[:alteration[1]] + str(alteration[0]) + currentString[alteration[1]+1:]
      
      controller = InputString(currentString)
      time = 0
      won = False
    
      while not ((time > maxDepth) or won):
        action = controller.getAction()
        won = player.doTick(action, objectList, winpad)
        time += 1
    
      if won:
        overDistance = player.x+Player.WIDTH-winpad.x
        subFrame = (1000 - int((overDistance / player.velX)*1000))/1000
        decimalTime = (time - 1) + subFrame
      
        if decimalTime < currentDecTime:
          currentDecTime = decimalTime
          trimmedString = currentString[:time]
          maxDepth = time
          print(f"\n\n\nInputString: {trimmedString}\nTime: {decimalTime} frames\nIteration: {currentIter}")
          currentBestString = trimmedString
    
      else:
        decimalTime = 1.0 * (100000 - player.x)
        if decimalTime < currentDecTime:
          currentDecTime = decimalTime
          player.x = int(1000*player.x)/1000.0
          print(f"\n\n\nInputString: {currentString}\nDistance: {player.x} units\nIteration: {currentIter}")
          currentBestString = currentString
        
      if alteration[0] == 5:
        alteration[0] = 0
        alteration[1] += 1
        if alteration[1] >= maxDepth:
          break
      else:
        alteration[0] += 1
  
  return baseString

class Vertex:
  
  def __init__(self, index, x, y, dist):
    self.index = index
    self.x = x
    self.y = y
    self.dist = dist
    self.edges = []
    
  def __str__(self):
    return f"({self.x}, {self.y})"
    
  def __repr__(self):
    return f"({self.x}, {self.y})"
  
  def unpack(self):
    arrayForm = [self.index, self.x, self.y, self.dist, [edge.unpack() for edge in self.edges]]
    return arrayForm
  
  def repack(self, arrayForm, graph):
    self.index = arrayForm[0]
    self.x = arrayForm[1]
    self.y = arrayForm[2]
    self.dist = arrayForm[3]
    self.edges = [Edge(None, None, None) for arr in arrayForm[4]]
    for i, edge in enumerate(self.edges):
        edge.repack(arrayForm[4][i], graph)

class Edge:
  
  def __init__(self, sNode, eNode, time):
    self.sNode = sNode
    self.eNode = eNode
    self.time = time
  
  def __str__(self):
    return f"({self.sNode.x}, {self.sNode.y}) -> ({self.eNode.x}, {self.eNode.y}) in {self.time} frames"
  
  def __repr__(self):
    return f"({self.sNode.x}, {self.sNode.y}) -> ({self.eNode.x}, {self.eNode.y}) in {self.time} frames"
  
  def unpack(self):
    arrayForm = [self.sNode.index, self.eNode.index, self.time]
    return arrayForm
  
  def repack(self, arrayForm, graph):
    self.sNode = graph[arrayForm[0]]
    self.eNode = graph[arrayForm[1]]
    self.time = arrayForm[2]
  
def graphConversion(loadFunc, bounds, increment=100, dist=20): # bounds (x1, x2, y1, y2) ensure that (0, 0) on bounds
  global time
  player, objectList, winpad = loadFunc()
  graph = []
  
  # 3 7 11
  # 2 6 10
  # 1 5 9
  # 0 4 8
  indIncr = -(-(bounds[3]-bounds[2])//increment)
  maxInd = -(-indIncr*((bounds[1]-bounds[0])//increment))

  for x in range(bounds[0], bounds[1], increment):
    for y in range(bounds[2], bounds[3], increment):
      # bl b br r tr t tl l
      index = len(graph)
      graph.append(Vertex(index, x, y, dist))
  
  for vertex in graph:
    for obj in objectList:
      xCollide = (vertex.x < (obj.x + obj.width)) and (obj.x < (vertex.x + Player.WIDTH))
      yCollide = (vertex.y < (obj.y + obj.height)) and (obj.y < (vertex.y + Player.HEIGHT))
      if xCollide and yCollide:
        vertex.dist = -67 # w sentinel value
        
    xCollide = (vertex.x < (winpad.x + winpad.width)) and (winpad.x < (vertex.x + Player.WIDTH))
    yCollide = (vertex.y < (winpad.y + winpad.height)) and (winpad.y < (vertex.y + Player.HEIGHT))
    if xCollide and yCollide:
      vertex.dist = -67
        
  graph.append(Vertex(len(graph), -1, -1, -1)) # victory node
  
  for vertInd, vertex in enumerate(graph):
    if vertex.dist == -1 or vertex.dist == -67:
      continue
    neighbors = []
    for thing in graph:
      if (thing.dist != -67) and (abs(thing.x - vertex.x) < 260) and (abs(thing.y - vertex.y) < 650):
        neighbors.append(thing)
    vertex.edges = [None for neighbor in neighbors]
    vertex.edges.append(None)

    inputs = [0, 1]
    changePoints = [1]
  
    active = True

    while active:
      player.x = vertex.x
      player.y = vertex.y
      player.velX = 0
      player.velY = 0
      currentString = ""
    
      strIndex = 0
      changePointIndex = 0
      changePoint = 0
      for inp in inputs:
        if changePointIndex == len(changePoints):
          changePoint = 20
        else:
          changePoint = changePoints[changePointIndex]
          changePointIndex += 1
        while strIndex < changePoint:
          currentString += str(inp)
          strIndex += 1
    
      controller = InputString(currentString)
      time = 0
      won = False
      hitVertex = False
      
      while not ((time > 20) or won):
        action = controller.getAction()
        won = player.doTick(action, objectList, winpad)
        time += 1
        for i, neighbor in enumerate(neighbors):
          if (player.x >= (neighbor.x - neighbor.dist)) and (player.x <= (neighbor.x + neighbor.dist)):
            if (player.y >= (neighbor.y - neighbor.dist)) and (player.y <= (neighbor.y + neighbor.dist)):
              if not vertex.edges[i] or vertex.edges[i].time > time:
                vertex.edges[i] = Edge(vertex, neighbor, time)
    
      if won:
        if not vertex.edges[-1] or vertex.edges[-1].time > time:
          vertex.edges[-1] = Edge(vertex, graph[-1], time)
      
      # currently at
      updateInput = True
      changePointIndex = len(changePoints) - 1
      changePointBuffer = 0
      while changePointIndex >= 0:
        if changePoints[changePointIndex] == 20-changePointBuffer:
          changePointIndex -= 1
          changePointBuffer += 1
        else:
          changePoints[changePointIndex] += 1
          base = changePoints[changePointIndex] + 1
          changePointIndex += 1
          while changePointIndex < len(changePoints):
            changePoints[changePointIndex] = base
            changePointIndex += 1
            base += 1
          updateInput = False
          break
      
      if updateInput:
        active = False
        incrIndex = len(inputs)-1
        while incrIndex >= 0:
          if inputs[incrIndex] == 5:
            if not incrIndex == 0 and inputs[incrIndex-1] == 0 and (not incrIndex == 1):
              inputs[incrIndex] = 1
            else:
              inputs[incrIndex] = 0
            incrIndex -= 1
          else:
            inputs[incrIndex] += 1
            if not incrIndex == 0 and inputs[incrIndex-1] == inputs[incrIndex]:
              continue
            active = True
            break
        for i in range(len(changePoints)):
          changePoints[i] = i+1
    if vertInd % 50 == 0:
      totalVertices = len(graph) - 1
      print(f"vertex {vertInd}/{totalVertices} done")
    vertex.edges = [edge for edge in vertex.edges if edge] # tuff
    
  return graph

def findMinimum(queue, dist):
  minValue = 99999999999
  minVertex = None
  for vertex in queue:
    if dist[vertex.index] < minValue:
      minVertex = vertex
      minValue = dist[vertex.index]
  return minVertex
    

def dijkstra(graph, source=0):
  dist = [99999999 for vertex in graph]
  prev = [None for vertex in graph]
  queue = [vertex for vertex in graph if vertex.dist != -67]
  dist[source] = 0
  
  while queue:
    current = findMinimum(queue, dist)
    queue.remove(current)

    for edge in current.edges:
      alternate = dist[current.index] + edge.time
      if alternate < dist[edge.eNode.index]:
        dist[edge.eNode.index] = alternate
        prev[edge.eNode.index] = current
  
  return dist, prev

def generateFromPrev(loadFunc, prev):
  global time
  player, objectList, winpad = loadFunc()
  
  lastX = 0
  lastY = 0
  lastVelX = 0
  lastVelY = 0
  baseString = ""
  addOnString = ""
  
  pathway = [Vertex(-1, -1, -1, -1)]
  current = prev[-1]
  while prev[current.index]:
    pathway.insert(0, current)
    current = prev[current.index]
      
  for vertex in pathway:
    if vertex.index == 0:
      continue
    
    addOnString = ""
    bestTime = 999
    
    inputs = [0, 1]
    changePoints = [1]
  
    active = True
    succeeded = False

    while active:
      player.x = lastX
      player.y = lastY
      player.velX = lastVelX
      player.velY = lastVelY
      currentString = ""
    
      strIndex = 0
      changePointIndex = 0
      changePoint = 0
      for inp in inputs:
        if changePointIndex == len(changePoints):
          changePoint = 50
        else:
          changePoint = changePoints[changePointIndex]
          changePointIndex += 1
        while strIndex < changePoint:
          currentString += str(inp)
          strIndex += 1
    
      controller = InputString(currentString)
      time = 0
      won = False

      while not ((time > 50) or won):
        action = controller.getAction()
        won = player.doTick(action, objectList, winpad)
        time += 1
        if won:
          break
        if not vertex.dist == -1 and (player.x >= (vertex.x - vertex.dist)) and (player.x <= (vertex.x + vertex.dist)):
          if (player.y >= (vertex.y - vertex.dist)) and (player.y <= (vertex.y + vertex.dist)):
            if time < bestTime:
              succeeded = True
              addOnString = currentString[:time]
              bestTime = time
              potLastX = player.x
              potLastY = player.y
              potLastVelX = player.velX
              potLastVelY = player.velY
            break
    
      if won:
        if time < bestTime:
          succeeded = True
          addOnString = currentString[:time]
          bestTime = time
          # to prevent errors on runs where 2lis can reach winpad in sub 20 frames
          potLastX = player.x
          potLastY = player.y
          potLastVelX = player.velX
          potLastVelY = player.velY
      
      updateInput = True
      changePointIndex = len(changePoints) - 1
      changePointBuffer = 0
      while changePointIndex >= 0:
        if changePoints[changePointIndex] == 20-changePointBuffer:
          changePointIndex -= 1
          changePointBuffer += 1
        else:
          changePoints[changePointIndex] += 1
          base = changePoints[changePointIndex] + 1
          changePointIndex += 1
          while changePointIndex < len(changePoints):
            changePoints[changePointIndex] = base
            changePointIndex += 1
            base += 1
          updateInput = False
          break
      
      if updateInput:
        active = False
        incrIndex = len(inputs)-1
        while incrIndex >= 0:
          if inputs[incrIndex] == 5:
            if not incrIndex == 0 and inputs[incrIndex-1] == 0 and (not incrIndex == 1):
              inputs[incrIndex] = 1
            else:
              inputs[incrIndex] = 0
            incrIndex -= 1
          else:
            inputs[incrIndex] += 1
            if not incrIndex == 0 and inputs[incrIndex-1] == inputs[incrIndex]:
              continue
            active = True
            break
        for i in range(len(changePoints)):
          changePoints[i] = i+1
    
    baseString += addOnString
    lastX = potLastX
    lastY = potLastY
    lastVelX = potLastVelX
    lastVelY = potLastVelY
    
    if not succeeded:
      return baseString, vertex
    
  return baseString, None

def djikstraSolve(loadFunc, bounds, increment=100, dist=20, graph=None):
  if graph is None:
      graph = graphConversion(loadFunc, bounds, increment, dist)
  jsonCopyGraph = [vertex.unpack() for vertex in graph]
  with open('saved_graph.json', 'w') as file:
    json.dump(jsonCopyGraph, file)
      
  bestString = ""
  bestX = -100
  while True:
    dist, prev = dijkstra(graph)
    if dist[-1] >= 100000:
      print("dijkstra solve failed")
      break
    repeated = False
    lastFailedVertex = None
    currentString = None
    failedVertex = None
    while not repeated:
        currentString, failedVertex = generateFromPrev(loadNonTrivial1, prev)
        if failedVertex is None:
          bestString = currentString
          break
        else:
          if failedVertex == lastFailedVertex:
              repeated = True
          lastFailedVertex = failedVertex
          print(failedVertex.x)
          print(currentString)
          prev[failedVertex.index] = prev[prev[failedVertex.index].index]

    for i in range(0, len(prev[failedVertex.index].edges)):
      if prev[failedVertex.index].edges[i].eNode == failedVertex:
        del prev[failedVertex.index].edges[i]
        break
  
  return bestString
  
def main():
  play()
  #jsonGraph = []
  #with open("/kaggle/input/datasets/ultraeon/saved-graph/saved_graph.json", "r") as file:
      #jsonGraph = json.load(file)
      
  #repackedGraph = [Vertex(None, None, None, None) for arr in jsonGraph]
  #for i, vertex in enumerate(repackedGraph):
      #vertex.repack(jsonGraph[i], repackedGraph)
      
  #bestString = djikstraSolve(loadNonTrivial1, (0, 9901, 0, 2301), increment=40, dist=25, graph=repackedGraph)
  #print("\nBest String: " + bestString)

if __name__ == "__main__":
    main()