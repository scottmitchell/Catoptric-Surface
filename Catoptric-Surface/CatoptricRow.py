from SerialFSM import SerialFSM
import time
import csv
import serial

class CatoptricRow(object):
	def __init__(self, rowNumber, numMirrors, serialPort):
		self.rowNumber = rowNumber
		self.numMirrors = numMirrors
		
		self._setup(serialPort)


	def _setup(self, serialPort):
		self.serial = serial.Serial(serialPort, 9600)
		time.sleep(2)
		self.fsm = SerialFSM(self.rowNumber)


	def checkIncoming(self):
		if (self.serial.in_waiting >= 1):
			c = self.serial.read()
			self.fsm.Execute(c)
		if self.fsm.messageReady:
			message = self.fsm.message
			self.fsm.message = []
			self.processMessage(message)
			return message
		else:
			return None


	def updatePositionByCSV(self, csvPath):
		#Read csv data
		with open(csvPath, newline='') as csvfile:
			reader = csv.reader(csvfile, delimiter=',')

			for row in reader:
				x = []
				for i in range(0, len(row)):
					x.append(row[i])
				if (int(x[0]) == int(self.rowNumber)):
					self.stepMotor(x[1], x[2], x[3], x[4])


	def stepMotor(self, y, m, d, c):
		c = int(c)*(513.0/360.0)
		countLow = int(c) & 255
		countHigh = (int(c) >> 8) & 255
	    
		message = [33, 65, self.rowNumber, y, m, d, countHigh, countLow]
		self.sendMessageToArduino(message)


	def sendMessageToArduino(self, message):
		for i in range(0, len(message)):
			bCurrent = bytes( [int(message[i])] )
			self.serial.write(bCurrent)
		self.fsm.currentCommandsToArduino += 1
	    

	def getCurrentCommandsOut(self):
		return self.fsm.currentCommandsToArduino


