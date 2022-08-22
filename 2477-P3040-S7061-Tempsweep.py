import GPIBPrologix
import csv  
import time
import datetime
import bme280
import smbus2
from math import sin

GPIB = GPIBPrologix.ResourceManager("/dev/ttyACM0")
with open(r'Logfile-NOMCSweep-01A.csv', 'a') as f:
    writer = csv.writer(f)
    writer.writerow(["DateTime","Resistance","Box Temperature", "Set Temperature","BME Temperature","BME Pressure", "BME Humidity"])
bus = smbus2.SMBus(1)
calibration_params = bme280.load_calibration_params(bus, 0x76)

inst1 = GPIB.open_resource(7)
inst2 = GPIB.open_resource(3)
inst3 = GPIB.open_resource(16)

inst3.query("MODE TRUEOHM")
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

inst2.query("S2")
inst2.query("LLA 15")
inst2.query("LHA 35")
inst2.query("R3")
while(1):
    for x in range(200):
        try:
            inst2.query("D"+str(round(5*sin(0.03141592*x)+23,2)))
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
                print("S7061 reading: ",S7061)

                counter = 0
                a = inst1.query("RD?") #Query a measurement
                P3040 = round((float(a[:10])-100)/0.385,4)
                print(P3040)

                d = datetime.datetime.now()
                dx = d - datetime.timedelta(microseconds=d.microsecond)
                data = bme280.sample(bus, 0x76, calibration_params)
                fields=[dx.strftime("%d-%m-%y %H:%M:%S"),float(S7061),float(P3040),float(round(5*sin(0.03141592*x)+23,2)),data.humidity,data.temperature,data.pressure]
                print(fields)
                with open(r'Logfile-NOMCSweep-01A.csv', 'a') as f:
                        writer = csv.writer(f)
                        writer.writerow(fields)
        except:
            print("error")
            time.sleep(1)
