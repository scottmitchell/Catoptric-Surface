import tkinter as Tk
from CatoptricRow import CatoptricRow
import csv


numColumns = 0
numRows = 4
serialCOMs = [] #("COM5", "COM5")

class CatoptricSurface():
	def __init__(self, numColumns, numRows, COMs):
		self.numColumns = numColumns
		self.numRows = numRows
		self.columnInterfaces = []
		self.setupColumnInterfaces(COMs)

	def setupColumnInterfaces(self, COMs):
		for i in range(self.numColumns):
			self.columnInterfaces.append(CatoptricRow(i, serialCOMs[i], numRows))


class CatoptricGUI():
	def __init__(self, master):
		self.e = Tk.Entry(master)
		self.e.pack()
		self.e.focus_set()
		self.loadButton = Tk.Button(master, text="Load", width=10)
		self.loadButton.pack()
		self.runButton = Tk.Button(master, text="Run", width=10)
		self.runButton.pack()

	def loadCSV(self):
		print(self.e.get()) 


class CatoptricController():
	def __init__(self):
		self.root = Tk.Tk()
		self.model = CatoptricSurface(numColumns, numRows, serialCOMs)
		self.view = CatoptricGUI(self.root)

		self.csvData = []

		self.view.loadButton.bind("<Button>", self.getCSV)
		self.view.runButton.bind("<Button>", self.runCSV)

	def run(self):
		self.root.title("Catoptric Surface Controller")
		self.root.deiconify()
		self.root.mainloop()

	def getCSV(self, event):
		# Deleta old CSV data
		self.csvData  = []

		# Get CSV path from entry field
		csvPath = self.view.e.get()

		# Read in CSV contents
		with open(csvPath, newline='') as csvfile:
			reader = csv.reader(csvfile, delimiter=',')
			for row in reader:
				x = []
				for i in range(0, len(row)):
					x.append(row[i])
				self.csvData.append(x)

	def runCSV(self, event):
		for line in self.csvData:
			if (int(line[0]) < self.model.numColumns and int(line[1]) < self.model.numRows):
				self.model.columnInterfaces[int(line[0])].stepMotor(line[1], line[2], line[3], line[4])




if __name__ == '__main__':
	c = CatoptricController()
	c.run()