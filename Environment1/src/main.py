import pygame
import time as t # bum used time as a var
import json
import socket
import math
from sortedcontainers import SortedList
from gameNew import *
from old import *
from collections import deque

nodeCount = 0
# basic solve (no heuristic)
# start at base node, expand out, list out new nodes, repeat

# basic solve (heuristic)
# start at base node, expand out, list out new nodes, calculate distance to winpad, prioritize based on distance

# basic solve (heuristic + pruning)
# start at base node, expand out, list out new nodes, check for repeated times and prune the repeated node

# modified currently ex1 and ex2 won't work as intended
class Node:
    __slots__ = ("player", "string", "childNodes", "distance", "isWin")

    def __init__(self, player, string, isWin, winpad):
        global nodeCount
        nodeCount += 1

        self.player = player
        self.string = string
        self.childNodes = [None] * 6
        self.distance = self.getDistance(winpad)
        self.isWin = isWin

    def __eq__(self, other):
        return self.distance == other.distance

    def __ne__(self, other):
        return self.distance != other.distance

    def __lt__(self, other):
        return self.distance < other.distance

    def __le__(self, other):
        return self.distance <= other.distance

    def __gt__(self, other):
        return self.distance > other.distance

    def __ge__(self, other):
        return self.distance >= other.distance

    def getChildren(self, objectList, winpad, frames=1):
        for i in range(6):
            childPlayer = self.player.clone() # 2rd prio for optimization
            isWin = False
            for j in range(frames):
                isWin = childPlayer.doTick(i, objectList, winpad)
                if isWin:
                    break

            self.childNodes[i] = Node(childPlayer, self.string+(str(i)*frames), isWin, winpad)
        return self.childNodes

    def getKey(self):
        return (self.player.x, self.player.y, self.player.velX, self.player.velY)

    def getDistance(self, winpad):
        return math.sqrt((winpad.y-self.player.y)**2 + (winpad.x-self.player.x)**2) + float(len(self.string)*10)

    def getTime(self):
        return len(self.string)

# basic search
def exedeus1solve(level, depthCap=10):
    global nodeCount

    startTime = t.perf_counter()
    player, objectList, winpad = level()
    baseNode = Node(player, "", False)
    layer = deque([baseNode])
    solvedFlag = False
    solution = ""
    updateTimer = t.perf_counter()
    finalDepth = depthCap

    for depth in range(depthCap):
        nextLayer = deque([])
        if solvedFlag:
            break
        duration = t.perf_counter() - startTime
        print(f"Depth: {depth}, Total Nodes: {nodeCount}, Duration: {duration:.3f}")
        for node in layer:
            if t.perf_counter() - updateTimer > 30:
                print(f"Total Nodes: {nodeCount}")
                updateTimer = t.perf_counter()
            if solvedFlag:
                break
            childNodes = node.getChildren(objectList, winpad) # slowdown
            for cNode in childNodes:
                if cNode.isWin:
                    finalDepth = depth+1
                    solution = cNode.string
                    solvedFlag = True
                    break
            nextLayer.extend(childNodes)
        layer = nextLayer

    endTime = t.perf_counter()
    duration = endTime - startTime

    if solvedFlag:
        print("Found Optimal Solution: \n" + solution)
    else:
        print("Depth cap reached")
    print(f"Depth: {finalDepth}, Total Nodes: {nodeCount}")
    print(f"Time Taken: {duration:.3f}")
    
    return solution

# basic search with pruning
def exedeus2solve(level, depthCap=13):
    global nodeCount

    startTime = t.perf_counter()
    player, objectList, winpad = level()
    baseNode = Node(player, "", False)
    layer = deque([baseNode])
    solvedFlag = False
    solution = ""
    updateTimer = t.perf_counter()
    finalDepth = depthCap

    visitedNodes = set()
    visitedNodes = {baseNode.getKey()}

    for depth in range(depthCap):
        nextLayer = deque([])
        if solvedFlag:
            break
        duration = t.perf_counter() - startTime
        print(f"Depth: {depth}, Total Nodes: {nodeCount}, Duration: {duration:.3f}")
        for node in layer:
            if t.perf_counter() - updateTimer > 30:
                print(f"Total Nodes: {nodeCount}")
                updateTimer = t.perf_counter()
            if solvedFlag:
                break
            childNodes = node.getChildren(objectList, winpad)
            for cNode in childNodes:
                key = cNode.getKey()
                if key in visitedNodes:
                    continue
                visitedNodes.add(key)
                nextLayer.append(cNode)
                if cNode.isWin:
                    finalDepth = depth+1
                    solution = cNode.string
                    solvedFlag = True
                    break
        layer = nextLayer

    endTime = t.perf_counter()
    duration = endTime - startTime

    if solvedFlag:
        print("Found Optimal Solution: \n" + solution)
    else:
        print("Depth cap reached")
    print(f"Depth: {finalDepth}, Total Nodes: {nodeCount}")
    print(f"Time Taken: {duration:.3f}")
    
    return solution

def removeAboveTime(nodeList, maxTime):
    for i in range(len(nodeList)-1, -1, -1):
        if nodeList[i].getTime() >= maxTime:
            nodeList.pop(i)

# heuristic based search with very naive implementation
def exedeus3solve(level, timeLimit=1800):
    global nodeCount

    startTime = t.perf_counter()
    nodeList = SortedList()
    maxTime = 60000
    
    player, objectList, winpad = level()
    baseNode = Node(player, "", False, winpad)
    nodeList.add(baseNode)
    solvedFlag = True
    solution = ""

    updateTimer = t.perf_counter()

    visitedNodes = dict()
    visitedNodes[baseNode.getKey()] = 0

    bestNode = nodeList.pop(0)
    while bestNode is not None:

        if t.perf_counter() - startTime > timeLimit:
            solution = bestNode.string
            solvedFlag = False
            break

        otherTime = visitedNodes.get(bestNode.getKey())
        if otherTime is not None and bestNode.getTime() > otherTime:
            bestNode = nodeList.pop(0)
            continue

        if t.perf_counter() - updateTimer > 30:
            print(f"Total Nodes: {nodeCount} List Length: {len(nodeList)} Current Distance: {bestNode.getDistance(winpad)} Current Position/Time: ({bestNode.player.x}, {bestNode.player.y}, {len(bestNode.string)})")
            updateTimer = t.perf_counter()
        
        childNodes = bestNode.getChildren(objectList, winpad)
        for cNode in childNodes:
            if maxTime <= len(cNode.string):
                continue
            otherTime = visitedNodes.get(cNode.getKey())
            if otherTime is not None and cNode.getTime() >= otherTime:
                continue

            visitedNodes[cNode.getKey()] = cNode.getTime()
            if cNode.isWin:
                solution = cNode.string
                maxTime = len(solution)
                removeAboveTime(nodeList, maxTime)
                duration = t.perf_counter() - startTime
                print(f"Found New Solution(Length: {len(solution)}): " + solution)
                print(f"Duration: {duration:.3f}")
                break
            nodeList.add(cNode)

        if len(nodeList) == 0:
            break
        bestNode = nodeList.pop(0)
    
    endTime = t.perf_counter()
    duration = endTime - startTime

    if solvedFlag:
        print("Found Optimal Solution: \n" + solution)
    else:
        print("Cap Reached, Best Solution: \n" + solution)
    print(f"Total Nodes: {nodeCount}")
    print(f"Time Taken: {duration:.3f}")
    
    return solution

# now frames are split
def exedeus4solve(level, timeLimit=28800, frames=16):
    global nodeCount

    startTime = t.perf_counter()
    nodeList = SortedList()
    maxTime = 60000
    
    player, objectList, winpad = level()
    baseNode = Node(player, "", False, winpad)
    nodeList.add(baseNode)
    solvedFlag = True
    solution = ""

    updateTimer = t.perf_counter()

    visitedNodes = dict()
    visitedNodes[baseNode.getKey()] = 0

    bestNode = nodeList.pop(0)
    while bestNode is not None:

        if t.perf_counter() - startTime > timeLimit:
            if solution == "":
                solution = bestNode.string
            solvedFlag = False
            break

        otherTime = visitedNodes.get(bestNode.getKey())
        if otherTime is not None and bestNode.getTime() > otherTime:
            bestNode = nodeList.pop(0)
            continue

        if t.perf_counter() - updateTimer > 30:
            print(f"Total Nodes: {nodeCount} List Length: {len(nodeList)} Current Distance: {bestNode.getDistance(winpad)} Current Position/Time: ({bestNode.player.x}, {bestNode.player.y}, {len(bestNode.string)})")
            updateTimer = t.perf_counter()
        
        childNodes = bestNode.getChildren(objectList, winpad, frames)
        for cNode in childNodes:
            if maxTime <= len(cNode.string):
                continue
            otherTime = visitedNodes.get(cNode.getKey())
            if otherTime is not None and cNode.getTime() >= otherTime:
                continue

            visitedNodes[cNode.getKey()] = cNode.getTime()
            if cNode.isWin:
                solution = cNode.string
                maxTime = len(solution)
                removeAboveTime(nodeList, maxTime)
                duration = t.perf_counter() - startTime
                print(f"Found New Solution(Length: {len(solution)}): " + solution)
                print(f"Duration: {duration:.3f}")
                break
            nodeList.add(cNode)

        if len(nodeList) == 0:
            if solution == "":
                solution = bestNode.string
                solvedFlag = False
            break
        bestNode = nodeList.pop(0)
    
    endTime = t.perf_counter()
    duration = endTime - startTime

    if solvedFlag:
        print(f"Found Optimal Solution Within Constraint({frames} frame inputs): \n" + solution)
    else:
        print("Cap Reached, Best Solution: \n" + solution)
    print(f"Total Nodes: {nodeCount}")
    print(f"Time Taken: {duration:.3f}")
    
    return solution

def main():
    #play(loadNonTrivial1)
    exedeus4solve(loadNonTrivial1, frames=8)

if __name__ == "__main__":
    main()