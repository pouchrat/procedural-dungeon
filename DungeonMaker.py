import random as rand
import RoomMaker as RM

class DungeonMaker:
    def __init__(self, dungeonSize = 10, roomSize = 10,
                 tunnelCount = 15, maxTunnelLen = 10,
                 wall = "#",
                 debug = False):

        # DEBUG
        self.debug = debug

        # DUNGEON ARRAY INIT
        self.dungeonSize = dungeonSize
        self.roomSize = roomSize
        self.dungeonArray = []

        # TUNNEL
        self.tunnelCount = tunnelCount
        self.maxTunnelLen = maxTunnelLen
        self.cur = [0,0]
        self.facingArray = [[1,0], # Right
                           [-1,0], # Left
                           [0,1],  # Down
                           [0,-1]] # Up
        self.facing = rand.choice(self.facingArray)
        
        # CREATE ROOM MAKER
        self.rm = RM.RoomMaker([self.roomSize,self.roomSize],debug = debug)

        # SET WALL CHAR
        self.wall = wall
        
        self.rm.createFilledRoom()
        self.filledRoom = self.rm.room


    def play(self):
        self.chooseCurPos()
        self.createArray()
        
        while self.tunnelCount > 0:
            self.digTunnel()
            self.tunnelCount -= 1
        
    
    def createArray(self):
        self.dungeonArray = []
        for row in range(self.dungeonSize):
            self.dungeonArray.append([])
            for col in range(self.dungeonSize):
                self.dungeonArray[row].append(self.filledRoom)

    def displayDungeon(self):
        dungeonDisplay = ""
        for m in range(0,self.dungeonSize):
            for k in range(0,self.roomSize):
                for j in range(0,self.dungeonSize):
                    for i in range(0,self.roomSize):
                        dungeonDisplay += str(self.dungeonArray[j][m].roomArray[k][i])
                if k < self.roomSize - 1:
                    dungeonDisplay += "\n"
            if m < self.dungeonSize - 1:
                dungeonDisplay += "\n"
            
        return dungeonDisplay


    # TUNNEL
    def chooseCurPos(self):
        row = rand.randrange(0,self.dungeonSize)
        col = rand.randrange(0,self.dungeonSize)
        self.cur = [row,col]

    def chooseFacing(self):
        if self.facing[0] == 0:
            self.facing = rand.choice([self.facingArray[0],self.facingArray[1]])
        else:
            self.facing = rand.choice([self.facingArray[2],self.facingArray[3]])

    def chooseTunnelLen(self):
        return rand.randrange(1,self.maxTunnelLen+1)

    def detectNearby(self):
        nearby = [0,0,0,0]

        if self.cur[0] - 1 >= 0:
            if self.dungeonArray[self.cur[0] - 1][self.cur[1]] != self.filledRoom:
                nearby[3] = 1
        if self.cur[0] + 1 < self.dungeonSize:
            if self.dungeonArray[self.cur[0] + 1][self.cur[1]] != self.filledRoom:
                nearby[1] = 1
        if self.cur[1] - 1 >= 0:
            if self.dungeonArray[self.cur[0]][self.cur[1] - 1] != self.filledRoom:
                nearby[0] = 1
        if self.cur[1] + 1 < self.dungeonSize:
            if self.dungeonArray[self.cur[0]][self.cur[1] + 1] != self.filledRoom:
                nearby[2] = 1

        return nearby
    
    def addDoorsNearby(self):
        nearby = self.detectNearby()
        if nearby[0] == 1:
            self.dungeonArray[self.cur[0]][self.cur[1] - 1].addDoors([0,0,1,0])
        if nearby[1] == 1:
            self.dungeonArray[self.cur[0] + 1][self.cur[1]].addDoors([0,0,0,1])
        if nearby[2] == 1:
            self.dungeonArray[self.cur[0]][self.cur[1] + 1].addDoors([1,0,0,0])
        if nearby[3] == 1:
            self.dungeonArray[self.cur[0] - 1][self.cur[1]].addDoors([0,1,0,0])
    
    def digTunnel(self):
        self.chooseFacing()
        tunnelLen = self.chooseTunnelLen()

        self.rm.doorCoord = [0,0,0,0]

        if self.facing[0] != 0:
            faceInd = 0
            curInd = 1
            coordInd = 0
        if self.facing[1] != 0:
            faceInd = 1
            curInd = 0
            coordInd = 1
        
        for i in range(0, tunnelLen):
            self.rm.doorCoord[coordInd] = 1
            self.rm.doorCoord[coordInd + 2] = 1

            self.rm.createRoom()
            self.rm.populateRoom()
            newRoom = self.rm.room

            if (self.cur[curInd] + self.facing[faceInd] < self.dungeonSize and
                self.cur[curInd] + self.facing[faceInd] >= 0):

                self.cur[curInd] = self.cur[curInd] + self.facing[faceInd]
                self.dungeonArray[self.cur[0]][self.cur[1]] = newRoom
                    
            elif (self.cur[curInd] + self.facing[faceInd] >= self.dungeonSize):

                self.cur[curInd] = 0
                self.dungeonArray[self.cur[0]][self.cur[1]] = newRoom
                
            else:
                
                self.cur[curInd] = self.dungeonSize - 1
                self.dungeonArray[self.cur[0]][self.cur[1]] = newRoom
            
            self.addDoorsNearby()
            self.dungeonArray[self.cur[0]][self.cur[1]].addDoors(self.detectNearby())

                

       