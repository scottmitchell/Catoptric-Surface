import serial.tools.list_ports

def getAvailableSerialPorts():
    allPorts = serial.tools.list_ports.comports()
    arduinoPorts = []
    for p in allPorts:
        if p.pid == 67:
            arduinoPorts.append(p)
    return arduinoPorts


serialPortOrder = { "8543931323035121E170" : 1,
					"8543931323035130C092" : 2,
					"85439313230351610262" : 3,
					"75435353934351D052C0" : 4,
					"85436323631351509171" : 5,
					"75435353934351F0C020" : 6,
					#"8543931333035160E081" : 7,
					"85439313230351818090" : 8,
					"755333434363519171F0" : 9,
					"8543931333035160F102" : 10,
					"8543931323035161B021" : 11,
					"85439313330351D03160" : 12,
					"85439303133351716221" : 13,
					"85436323631351300201" : 14,
					"75435353934351E07072" : 15,
					"8543931323035170D0C2" : 16 
				}


if __name__ == '__main__':
    serports = getAvailableSerialPorts()
    for s in serports:
        print(s.serial_number)

    allPorts = serial.tools.list_ports.comports()

    arduinoPorts = [p for p in allPorts if p.pid == 67]

    try:
        arduinoPorts.sort(key= lambda x: serialPortOrder[x.serial_number])
    except:
        print("One or more arduino serial number unrecognized")

    for a in arduinoPorts:
        try:
            print ("Arduino #%s : Row #%d" % (a.serial_number, serialPortOrder[a.serial_number]))
        except:
            print ("Arduino #%s : Unrecognized Serial Number" % a.serial_number)

    while True:
        x = input()
        print (x)