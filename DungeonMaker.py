import random as rand
import math
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


    def play(self):
        self.chooseCurPos()
        self.createArray()
        
        while self.tunnelCount > 0:
            self.digTunnel()
            self.tunnelCount -= 1
            
        print(self.displayDungeon())
        
    
    def createArray(self):
        self.dungeonArray = []
        self.rm.createWallRoom()
        wallRoom = self.rm.roomArray
        for row in range(self.dungeonSize):
            self.dungeonArray.append([])
            for col in range(self.dungeonSize):
                self.dungeonArray[row].append(wallRoom)

    def displayDungeon(self):
        dungeonDisplay = ""
        for m in range(0,self.dungeonSize):
            for k in range(0,self.roomSize):
                for j in range(0,self.dungeonSize):
                    for i in range(0,self.roomSize):
                        dungeonDisplay += str(self.dungeonArray[j][m][k][i])
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
    
    def digTunnel(self): # WIP
        self.chooseFacing()
        tunnelLen = self.chooseTunnelLen()

        if self.facing[0] != 0:

            for i in range(0,tunnelLen):
                self.rm.play()
                newRoom = self.rm.roomArray
            
                if (self.cur[1] + self.facing[0] < self.dungeonSize and
                    self.cur[1] + self.facing[0] >= 0):

                    self.cur[1] = self.cur[1] + self.facing[0]
                    self.dungeonArray[self.cur[0]][self.cur[1]] = newRoom
                    
                elif (self.cur[1] + self.facing[0] >= self.dungeonSize):

                    self.cur[1] = 0
                    self.dungeonArray[self.cur[0]][self.cur[1]] = newRoom
                    
                else:
                    
                    self.cur[1] = self.dungeonSize - 1
                    self.dungeonArray[self.cur[0]][self.cur[1]] = newRoom
                    
        if self.facing[1] != 0:

            for i in range(0,tunnelLen):
                self.rm.play()
                newRoom = self.rm.roomArray
            
                if (self.cur[0] + self.facing[1] < self.dungeonSize and
                    self.cur[0] + self.facing[1] >= 0):

                    self.cur[0] = self.cur[0] + self.facing[1]
                    self.dungeonArray[self.cur[0]][self.cur[1]] = newRoom

                elif (self.cur[0] + self.facing[1] >= self.dungeonSize):

                    self.cur[0] = 0
                    self.dungeonArray[self.cur[0]][self.cur[1]] = newRoom
                    
                else:
                    
                    self.cur[0] = self.dungeonSize - 1
                    self.dungeonArray[self.cur[0]][self.cur[1]] = newRoom

    