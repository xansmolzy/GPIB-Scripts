import GPIBPrologix
import csv  
import time
import datetime
import smbus
import bme280

GPIB = GPIBPrologix.ResourceManager("/dev/ttyACM0")
with open(r'Logfile-LTZ-S7061-HP34401A-HP3488A.csv', 'a') as f:
    writer = csv.writer(f)
    writer.writerow(["DateTime","10V Voltage S7061","10VR Voltage S7061", "7V Voltage S7061","7VR Voltage S7061","10V Voltage HP34401A","10VR Voltage HP34401A", "7V Voltage HP34401A","7VR Voltage HP34401A" ,"BME Temperature","BME Pressure", "BME Humidity"])

#Init Solartron 7061
inst1 = GPIB.open_resource(16)
inst1.query("MODE VDc")
inst1.query("RANGE 10")
inst1.query("DIGits 7")
inst1.query("DRift OFf")
#Init HP 34401A
inst2 = GPIB.open_resource(16)
#Init HP 3488A
inst3 = GPIB.open_resource(9)
inst3.query("CRESET 2, 3")

bus = smbus.SMBus(1)
calibration_params = bme280.load_calibration_params(bus, 0x76)

for lp in range(20000):
        data = bme280.sample(bus, 0x76, calibration_params)
        print(data)

        inst3.query("CRESET 2, 3")
        inst3.query("CLOSE 303")
        time.sleep(3)

        #Get S7061
        inst1.query("TRIgger")
        counter = 0
        a = inst1.read()
        prevA = a
        while(a == prevA and counter < 30):
                a = inst1.read()
                time.sleep(0.1)
                counter = counter + 1
        inst1.query("DISplay []")
        S7061_10V = a[0:10]
        print("S7061 reading 10V:",a,S7061_10V)

        inst3.query("CRESET 2, 3")
        inst3.query("CLOSE 313")
        time.sleep(3)

        #Get S7061
        inst1.query("TRIgger")
        counter = 0
        a = inst1.read()
        prevA = a
        while(a == prevA and counter < 30):
                a = inst1.read()
                time.sleep(0.1)
                counter = counter + 1
        inst1.query("DISplay []")
        S7061_10V_Rev = a[0:10]
        print("S7061 reading 10V reversed:",a,S7061_10V_Rev)

        inst3.query("CRESET 2, 3")
        inst3.query("CLOSE 203")
        time.sleep(3)

        #Get HP34401A
        inst2.query(inst2.query("MEAS:VOLT:DC? 10,MAX"))
        counter = 0
        a = inst2.read()
        prevA = a
        while(a == prevA and counter < 30):
                a = inst2.read()
                time.sleep(0.1)
                counter = counter + 1
        inst2.query("DISPlay:TEXT \"\"")
        HP34401_10V = a[0:10]
        print("HP34401 reading 10V:",a,HP34401_10V)

        inst3.query("CRESET 2, 3")
        inst3.query("CLOSE 213")
        time.sleep(3)

        #Get HP34401A
        inst2.query(inst2.query("MEAS:VOLT:DC? 10,MAX"))
        counter = 0
        a = inst2.read()
        prevA = a
        while(a == prevA and counter < 30):
                a = inst2.read()
                time.sleep(0.1)
                counter = counter + 1
        inst2.query("DISPlay:TEXT \"\"")
        HP34401_10V_Rev = a[0:10]
        print("HP34401 reading 10V:",a,HP34401_10V_Rev)

        inst3.query("CRESET 2, 3")
        inst3.query("CLOSE 323")
        time.sleep(3)

        #Get S7061
        inst1.query("TRIgger")
        counter = 0
        a = inst1.read()
        prevA = a
        while(a == prevA and counter < 30):
                a = inst1.read()
                time.sleep(0.1)
                counter = counter + 1
        inst1.query("DISplay []")
        S7061_7V = a[0:10]
        print("S7061 reading 10V:",a,S7061_7V)

        inst3.query("CRESET 2, 3")
        inst3.query("CLOSE 333")
        time.sleep(3)

        #Get S7061
        inst1.query("TRIgger")
        counter = 0
        a = inst1.read()
        prevA = a
        while(a == prevA and counter < 30):
                a = inst1.read()
                time.sleep(0.1)
                counter = counter + 1
        inst1.query("DISplay []")
        S7061_7V_Rev = a[0:10]
        print("S7061 reading 10V reversed:",a,S7061_7V_Rev)

        inst3.query("CRESET 2, 3")
        inst3.query("CLOSE 223")
        time.sleep(3)

        #Get HP34401A
        inst2.query(inst2.query("MEAS:VOLT:DC? 10,MAX"))
        counter = 0
        a = inst2.read()
        prevA = a
        while(a == prevA and counter < 30):
                a = inst2.read()
                time.sleep(0.1)
                counter = counter + 1
        inst2.query("DISPlay:TEXT \"\"")
        HP34401_7V = a[0:10]
        print("HP34401 reading 10V:",a,HP34401_7V)

        inst3.query("CRESET 2, 3")
        inst3.query("CLOSE 233")
        time.sleep(3)

        #Get HP34401A
        inst2.query(inst2.query("MEAS:VOLT:DC? 10,MAX"))
        counter = 0
        a = inst2.read()
        prevA = a
        while(a == prevA and counter < 30):
                a = inst2.read()
                time.sleep(0.1)
                counter = counter + 1
        inst2.query("DISPlay:TEXT \"\"")
        HP34401_7V_Rev = a[0:10]
        print("HP34401 reading 10V:",a,HP34401_7V_Rev)

        d = datetime.datetime.now()
        x = d - datetime.timedelta(microseconds=d.microsecond)
        fields=[x.strftime(),float(S7061_10V),float(S7061_10V_Rev),float(S7061_7V),float(S7061_7V_Rev),float(HP34401_10V),float(HP34401_10V_Rev),float(HP34401_7V),float(HP34401_7V_Rev),data.humidity,data.temperature,data.pressure]
        print(fields)
        with open(r'Logfile-LTZ-S7061-HP34401A-HP3488A.csv', 'a') as f:
                writer = csv.writer(f)
                writer.writerow(fields)
GPIB.close()