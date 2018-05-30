from SerialFSM import SerialFSM
import time
import csv
import serial
from queue import Queue

maxCommandsOut = 2

class CatoptricRow(object):
	def __init__(self, rowNumber, numMirrors, serialPort):
		self.rowNumber = rowNumber
		self.numMirrors = numMirrors
		self.commandQueue = Queue()
		

		# Init Motor States
		self.motorStates = []
		for i in range(numMirrors):
			states = [0, 0]
			self.motorStates.append(states)

		# Setup Serial
		self._setup(serialPort)


	def _setup(self, serialPort):
		self.serial = serial.Serial(serialPort, 9600)
		self.serial.reset_input_buffer()
		self.serial.reset_output_buffer()
		time.sleep(2)
		self.fsm = SerialFSM(self.rowNumber)
	
	def resetSerialBuffer(self):
		self.serial.reset_input_buffer()
		self.serial.reset_output_buffer()

	
	def update(self):
		self.checkIncoming()
		if (self.getCurrentCommandsOut() < maxCommandsOut and self.commandQueue.qsize() > 0):
			message = self.commandQueue.get()
			self.sendMessageToArduino(message)


	def checkIncoming(self):
		if (self.serial.in_waiting >= 1):
			c = self.serial.read()
			self.fsm.Execute(c)
		if self.fsm.messageReady:
			message = self.fsm.message
			self.fsm.message = []
			print(message)


	def stepMotor(self, y, m, d, c):
		c = int(c)*(513.0/360.0)
		countLow = int(c) & 255
		countHigh = (int(c) >> 8) & 255
	    
		message = [33, 65, self.rowNumber, y, m, d, countHigh, countLow]
		self.commandQueue.put(message)


	def sendMessageToArduino(self, message):
		for i in range(0, len(message)):
			bCurrent = bytes( [int(message[i])] )
			self.serial.write(bCurrent)
		self.fsm.currentCommandsToArduino += 1
	    

	def getCurrentCommandsOut(self):
		return self.fsm.currentCommandsToArduino

	def getCurrentNackCount(self):
		return self.fsm.nackCount

	def getCurrentAckCount(self):
		return self.fsm.ackCount
	

	def reorientMirrorAxis(self, command):
		mirror = int(command[1])
		motor = int(command[2])
		newState = int(command[3])
		currentState = self.motorStates[mirror][motor]
		
		delta = newState - currentState
		direction = 0
		if (delta < 0):
			direction = 1

		self.stepMotor(mirror, motor, direction, abs(delta))
		self.motorStates[mirror][motor] = newState

	def reset(self):
		for i in range(self.numMirrors):
			self.stepMotor(i+1, 1, 0, 200)
			self.stepMotor(i+1, 0, 0, 200)
			self.motorStates[i][0] = 0
			self.motorStates[i][1] = 0


