import GPIBPrologix
import csv  
import time
import datetime
from math import sin

GPIB = GPIBPrologix.ResourceManager("/dev/ttyACM0")

#Init Prema3040
inst1 = GPIB.open_resource(7)
inst2 = GPIB.open_resource(3)
inst3 = GPIB.open_resource(16)

inst3.query("MODE VDc")
inst3.query("RANGE 10")
inst3.query("DIGits 7")
inst3.query("DRift OFf")

inst1.query("R3")     #Resistance mode 3, PT100 1mA
inst1.query("F2")     #Auto filter
inst1.query("T7")     #Set integration time 4S
inst1.query("CN0")    #Only data on query
inst1.query("O4")     #4 Wire
inst1.query("U1")     #Basic unit ON
inst1.query("AZA1")   #Auto zero on
inst1.query("AZT0300")#Auto zero every 300seconds
inst1.query("MAR")    #Front, Channel A, RTD

inst2.query("SE")
inst2.query("LLA 15")
inst2.query("LHA 35")
inst2.query("R3")

time.sleep(20)
while(1):
    try:
        for x in range(200):
            inst2.query("D" + str(round(5*sin(0.03141592*x)+23),2))
            for i in range(10):
                inst3.query("TRIgger")
                counter = 0
                a = inst3.read()
                prevA = a
                while(a == prevA and counter < 30):
                        a = inst3.read()
                        time.sleep(0.1)
                        counter = counter + 1
                inst3.query("DISplay []")
                S7061 = a[0:10]
                print("S7061 reading 10V:",a,S7061)

                counter = 0
                a = inst1.query("RD?") #Query a measurement
                prevA = a 
                while(a == prevA and counter < 50):
                    a = inst1.query("RD?")
                    time.sleep(0.1)
                    counter = counter + 1
                P3040 = round((float(a[:10])-100)/0.385,4)
                print(P3040)
    except:
        print("error")
        time.sleep(1)
