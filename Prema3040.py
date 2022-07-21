import GPIBPrologix
import csv  
import time
import datetime

GPIB = GPIBPrologix.ResourceManager("/dev/ttyACM0")

#Init Prema3040
inst1 = GPIB.open_resource(7)

inst1.query("R3")     #Resistance mode 3, PT100 1mA
inst1.query("F2")     #Auto filter
inst1.query("T7")     #Set integration time 4S
inst1.query("CN0")    #Only data on query

inst1.query("O4")     #4 Wire
inst1.query("U1")     #Basic unit ON

inst1.query("AZA1")   #Auto zero on
inst1.query("AZT0300")#Auto zero every 300seconds

inst1.query("MAR")    #Front, Channel A, RTD
time.sleep(20)
while(1):
    try:
        counter = 0
        a = inst1.query("RD?") #Query a measurement
        prevA = a 
        while(a == prevA and counter < 50):
                a = inst1.query("RD?")
                time.sleep(0.1)
                counter = counter + 1
        print(round((float(a[:10])-100)/0.385,4))
    except:
        print("error")
        time.sleep(1)
