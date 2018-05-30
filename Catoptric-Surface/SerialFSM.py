import serial
import time
import csv

# Define states
GET_MAGIC_NUM = 0
GET_KEY = 1
GET_NUM_CHAR_HIGH = 2
GET_NUM_CHAR_LOW = 3
GET_CHAR = 4
GET_ACK_KEY = 5
GET_ACK_X = 6
GET_ACK_Y = 7
GET_ACK_M = 8
GET_NACK_KEY = 9

class SerialFSM(object):
    def __init__(self, name):
        self.name = name
        super(SerialFSM, self).__init__()
        self.currentCommandsToArduino = 0
        self.nackCount = 0
        self.ackCount = 0

        self.currentState = 0
        #self.setupStates()
        self.stateDefs = {0 : self.getMagicNum,
                        1 : self.getKey,
                        2 : self.getNumCharHigh,
                        3 : self.getNumCharLow,
                        4 : self.getChar,
                        5 : self.getAckKey,
                        6 : self.getAckX,
                        7 : self.getAckY,
                        8 : self.getAckM,
                        9 : self.getNackKey}
        
        self.resetVariables()


    def resetVariables(self):
        self.ackX = 0
        self.ackY = 0
        self.ackM = 0
        self.countHigh = 0
        self.countLow = 0
        self.count = 0
        self.message = []
        self.messageReady = False


    def Execute(self, c):
        self.currentState = self.stateDefs[self.currentState](c)


##########
# STATES #
##########

    def getMagicNum(self, c):
        self.resetVariables()
        if (c == b'!'):
            return GET_KEY
        else:
            return GET_MAGIC_NUM
        
    def getKey(self, c):
        if (c == b'a'):
            self.currentCommandsToArduino -= 1
            return GET_ACK_KEY
        elif (c == b'b'):
            return GET_NACK_KEY
        elif (c == b'c'):
            return GET_NUM_CHAR_HIGH
        else:
            return GET_MAGIC_NUM

    def getAckKey(self, c):
        self.ackCount += 1
        if (c == b'A'):
            return GET_ACK_X
        else:
            return GET_MAGIC_NUM
        
    def getAckX(self, c):
        c = ord( c )
        if (c <= 32):
            self.ackX = c
            return GET_ACK_Y
        else:
            return GET_MAGIC_NUM

    def getAckY(self, c):
        c = ord( c )
        if (c <= 32):
            self.ackY = c
            return GET_ACK_M
        else:
            return GET_MAGIC_NUM

    def getAckM(self, c):
        c = ord( c )
        if (c <= 2):
            self.ackM = c
            #print("Mirror (%d, %d), Motor %d moved to new state" % (self.ackX, self.ackY, self.ackM))
            
            return GET_MAGIC_NUM
        else:
            return GET_MAGIC_NUM

    def getNumCharHigh(self, c):
        self.countHigh = ord( c )
        return GET_NUM_CHAR_LOW

    def getNumCharLow(self, c):
        self.countLow = ord( c )
        self.count = (self.countHigh << 8) + self.countLow
        self.message = []
        return GET_CHAR

    def getChar(self, c):
        if (self.count <= 1):
            self.message.append(chr(ord(c)))
            self.messageReady = True
            return GET_MAGIC_NUM
        
        else:
            self.message.append(chr(ord(c)))
            self.count -= 1
            return GET_CHAR

    def getNackKey(self, c):
        self.nackCount += 1
        if (c == b'B'):
            #Process Nack
            return GET_MAGIC_NUM
        else:
            return GET_MAGIC_NUM

