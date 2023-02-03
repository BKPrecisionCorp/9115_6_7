# This is example code for the BK Precision 9117
# A programming manual for the BK Precision 9117 can be found at:
# https://bkpmedia.s3.amazonaws.com/downloads/programming_manuals/en-us/9115_series_programming_manual.pdf
# Note the 9117 can not utilize the list mode functions

import pyvisa as visa
import time     # This is used for the sleep function (Delay)



print("This Script is made for the BK9117 DC Power Supply")
manager = visa.ResourceManager()
li = manager.list_resources()
for index in range(len(li)):
    print(str(index)+" - "+li[index])
choice = input("Which Device?: ")
PSU=manager.open_resource(li[int(choice)]) #creates an alias (variable) for the VISA resource name of a device
# we do this so we don't have to call that constantly. This is unique to a unit and changes depending on USB port used and serial number of a unit. 
# This will automatically detect connected devices and allows you to select the one you want to run the script on.


#####_____ DEFINING FUNCTIONS _____#####
def setup():
	PSU.write("SYST:REM")
	PSU.write("*CLS")
	PSU.write("SYST:INT USB")
	PSU.write("VOLT:LEV 0")
	PSU.write("CURR:LEV 10")                                                     # If current limit is very low, rise time will be very slow!
	PSU.write("OUTP ON")                                                       # Turn On for Testing!

def ListStep(start, end, delay):                                                # Start point (V), End Point (V), and length of Time (Unit Below)
    range = end - start                                                         # Check if rising or falling
    unit = delay / 1000                                                         # Division detirmines units of time, currently mS
    pollFlag = 0                                                                # Flag for polling
    
    PSU.write("RISE:LEV 0")
    PSU.write("FALL:LEV 0")                                                     # Reset rise and fall
    PSU.write("VOLT:LEV " + str(round(start, 3)))                               # Set Voltage to start value

    if(range < 0):
        PSU.write("FALL:LEV " + str(round(unit, 3)))                            # If reducing value, set fall rate
        PSU.write("VOLT:LEV " + str(round(end, 3)))                             # Set Voltage to end value
        pollFlag = 1                                                            # enable polling
    elif (range > 0):
        PSU.write("RISE:LEV " + str(round(unit, 3)))                            # If raising value, set rise rate
        PSU.write("VOLT:LEV " + str(round(end, 3)))                             # Set Voltage to end value
        pollFlag = 1                                                            # enable polling

    if(pollFlag == 1):                                                         
        while(pollFlag == 1):                                                   # If polling enabled, sleep and poll for voltage value
            time.sleep(0.001)
            PSU.write("MEAS:VOLT?")
            output = (PSU.read())
            if(float(output) > end - 1 and float(output) < end + 1):            # If measured voltage within +-1V of final value, disable polling
                pollFlag = 0
    else:
        time.sleep(unit)                                                        # If polling never enabled, delay for time length


def close():
	PSU.write("*CLS")
	PSU.write("OUTP OFF")
	PSU.write("SYST:LOC")


#####_____ COMMANDS _____#####

setup()
time.sleep(1)

ListStep(6, 6, 100)
ListStep(6, 60, 20)
ListStep(60, 60, 20)
ListStep(60, 6, 100)
ListStep(6, 6, 100)

close()
