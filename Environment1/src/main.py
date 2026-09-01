import pygame
import time as t # bum used time as a var
import json
import socket
from game import *
from old import *
from collections import deque

nodeCount = 0
# basic solve (no heuristic)
# start at base node, expand out, list out new nodes, repeat

# basic solve (heuristic)
# start at base node, expand out, list out new nodes, calculate distance to winpad, prioritize based on distance

# basic solve (heuristic + pruning)
# start at base node, expand out, list out new nodes, check for repeated times and prune the repeated node

class Node:
    __slots__ = ("player", "string", "childNodes", "isWin")

    def __init__(self, player, string, isWin):
        global nodeCount
        nodeCount += 1

        self.player = player
        self.string = string
        self.childNodes = [None] * 6
        self.isWin = isWin

    def getChildren(self, objectList, winpad):
        for i in range(6):
            childPlayer = self.player.clone() # 2rd prio for optimization
            isWin = childPlayer.doTick(i, objectList, winpad)
            self.childNodes[i] = Node(childPlayer, self.string+str(i), isWin)
        return self.childNodes

    def getKey(self):
        return (self.player.x, self.player.y, self.player.velX, self.player.velY)

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

def main():
    exedeus2solve(loadTrivial2)

if __name__ == "__main__":
    main()