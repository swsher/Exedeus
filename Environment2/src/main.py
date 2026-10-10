from game import *
import time as t
from sortedcontainers import SortedList
import psutil

class Node:
    __slots__ = ("player", "string", "childNodes", "distance", "isWin")

    def __init__(self, player, string, isWin, winpad):
        global nodeCount
        nodeCount += 1

        self.player = player
        self.string = string
        self.childNodes = [None] * 32
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
        for i in range(32):
            childPlayer = self.player.clone()
            isWin = False
            for j in range(frames):
                isWin = childPlayer.doTick(i, objectList, winpad)
                if isWin:
                    break

            self.childNodes[i] = Node(childPlayer, self.string+(f"{i:03d}"*frames), isWin, winpad)
        return self.childNodes

    def getKey(self):
        return (self.player.x, self.player.y, self.player.z, self.player.velX, self.player.velY, self.player.velZ, self.player.direction, self.player.coyoteTime)

    # ub if cellSize isn't an int > 0
    def getCellKey(self, cellSize=5):
        fCellSize = float(cellSize)
        return (int(self.player.x/fCellSize)*cellSize, int(self.player.y/fCellSize)*cellSize, int(self.player.z/fCellSize)*cellSize, int(self.player.velX/fCellSize)*cellSize, int(self.player.velY/fCellSize)*cellSize, int(self.player.velZ/fCellSize)*cellSize, int(self.player.direction/fCellSize)*cellSize, int(self.player.coyoteTime/fCellSize)*cellSize)

    def getDistance(self, winpad):
        return math.sqrt((winpad.y-self.player.y)**2 + (winpad.x-self.player.x)**2 + (winpad.z-self.player.z)**2) + (float(len(self.string)*10)/3)

    def getTime(self):
        return len(self.string)

def removeAboveTime(nodeList, maxTime):
    for i in range(len(nodeList)-1, -1, -1):
        if nodeList[i].getTime() >= maxTime:
            nodeList.pop(i)
            
# now cells group similar frames
def exedeus5solve(level, timeLimit=300, frames=16, cellSize=10):
    global nodeCount
    nodeCount = 0

    startTime = t.perf_counter()
    nodeList = SortedList()
    maxTime = 60000
    endCondition = "ERROR_SHOULD_NOT_BE_THIS_END_CONDITION"
    
    player, objectList, winpad = level()
    baseNode = Node(player, "", False, winpad)
    nodeList.add(baseNode)
    solvedFlag = True
    bestDistance = 9999999999
    solution = ""

    updateTimer = t.perf_counter()

    visitedNodes = dict()
    visitedNodes[baseNode.getCellKey(cellSize)] = 0

    bestNode = nodeList.pop(0)
    while bestNode is not None:
         
        percentMemory = psutil.virtual_memory().percent
        if percentMemory > 99:
            print("Memory Cap Reached")
            ramGB = psutil.virtual_memory().total / (1024 ** 3)
            endCondition = f"RAM_EXCEEDED({ramGB}_GB)"
            solvedFlag = False
            break

        distance = bestNode.getDistance(winpad)
        if distance < bestDistance:
            print(distance)
            solution = bestNode.string
            bestDistance = distance

        if t.perf_counter() - startTime > timeLimit:
            print("Time limit reached")
            endCondition = f"TIME_LIMIT_EXCEEDED({timeLimit}_SECONDS)"
            solvedFlag = False
            break

        otherTime = visitedNodes.get(bestNode.getCellKey(cellSize))
        if otherTime is not None and bestNode.getTime() > otherTime:
            if len(nodeList) == 0:
                print("Full solution space searched")
                endCondition = f"SEARCH_COMPLETED({nodeCount}_NODES)"
                break

            bestNode = nodeList.pop(0)
            continue

        if t.perf_counter() - updateTimer > 30:
            #print(f"Total Nodes: {nodeCount} List Length: {len(nodeList)} Current Distance: {bestNode.getDistance(winpad)} Current Position/Time: ({bestNode.player.x}, {bestNode.player.y}, {len(bestNode.string)})")
            updateTimer = t.perf_counter()
        
        childNodes = bestNode.getChildren(objectList, winpad, frames)
        for cNode in childNodes:
            if maxTime <= len(cNode.string):
                continue
            otherTime = visitedNodes.get(cNode.getCellKey(cellSize))
            if otherTime is not None and cNode.getTime() >= otherTime:
                continue

            visitedNodes[cNode.getCellKey(cellSize)] = cNode.getTime()
            if cNode.isWin:
                solution = cNode.string
                maxTime = len(solution)
                removeAboveTime(nodeList, maxTime)
                duration = t.perf_counter() - startTime
                #print(f"Found New Solution(Length: {len(solution)}): " + solution)
                bestDistance = -69
                #print(f"Duration: {duration:.3f}")
                break
            nodeList.add(cNode)

        if len(nodeList) == 0:
            print("Full solution space searched")
            endCondition = f"SEARCH_COMPLETED({nodeCount}_NODES)"
            break

        bestNode = nodeList.pop(0)
    
    endTime = t.perf_counter()
    duration = endTime - startTime

    #if solvedFlag:
        #print(f"Found Optimal Solution Within Constraint({frames} frame inputs): \n" + solution)
    #else:
        #print("Cap Reached, Best Solution: \n" + solution)
    #print(f"Total Nodes: {nodeCount}")
    #print(f"Time Taken: {duration:.3f}")
    
    return solution, endCondition

def main():
    play()
    #print(exedeus5solve(loadBasicJumps))

if __name__ == "__main__":
    main()
