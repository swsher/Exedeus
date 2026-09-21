#import pygame
import time as t # bum used time as a var
import json
import socket

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