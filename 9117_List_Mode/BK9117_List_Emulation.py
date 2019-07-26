# This is example code for the BK Precision 9117
# A programming manual for the BK Precision 9117 can be found at:
# https://bkpmedia.s3.amazonaws.com/downloads/programming_manuals/en-us/9115_series_programming_manual.pdf
# Note the 9117 can not utilize the list mode functions

import visa
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


def setup():
	PSU.write("*CLS")
	PSU.write("SYST:INT USB")
	PSU.write("SYST:REM")
	PSU.write("SYST:INT USB")
	PSU.write("VOLT:LEV 0")
	PSU.write("CURR:LEV 1")         # If current limit is very low, rise time will be very slow!
	PSU.write("OUTP ON")


def close():
	PSU.write("*CLS")
	PSU.write("OUTP OFF")
	PSU.write("SYST:LOC")



setup()
time.sleep(1)


#####_____ Brute Force List Mode _____#####


def commandList(start, end, time):	# Enter beginning voltage (V), ending voltage (V), and time (unit depends on below).
	Value = start					# start value to be changed
	range = end - start				# range of numbers traversed
	dv = range / time				# value change per unit of time
	cnt = 0							# counts to time value
	commands = []					# empty list to handle commands
	while cnt - 1 < time:
		commands.append("VOLT:LEV " + str(round(Value, 3)))		# appends voltage commands with current value
		Value = Value + dv										# adjust value
		cnt += 1
	return commands


def sendCommand(list):
	cnt = 0
	while cnt < len(list):
		print("Sending Command: ", end = '')
		print(list[cnt])
		PSU.write(list[cnt])
		time.sleep(0.001)									# This value detirmines time unit
		cnt += 1
	print("")
	print("List Complete")



#Output = commandList(6, 6, 100) + commandList(6, 60, 20) + commandList(60, 60, 20) + commandList(60, 6, 100) + commandList(6, 6, 100)
#Output = commandList(6, 6, 1) + commandList(60, 60, 20)+ commandList(6, 6, 1)
#time.sleep(1)
#sendCommand(Output)



#####_____ More Efficient List Mode Emulation _____#####

def commandRamp(start, end, delay):
    range = end - start
    PSU.write("VOLT:LEV " + str(round(start, 3)))
    if(range < 0):
        PSU.write("FALL:LEV " + str(round(delay/1000, 3)))
        PSU.write("VOLT:LEV " + str(round(end, 3)))

        print("VOLT:LEV " + str(round(start, 3)))
        print("VOLT:LEV " + str(round(end, 3)))
    elif (range > 0):
        PSU.write("RISE:LEV " + str(round(delay/1000, 3)))
        PSU.write("VOLT:LEV " + str(round(end, 3)))

        print("VOLT:LEV " + str(round(start, 3)))
        print("VOLT:LEV " + str(round(end, 3)))
    time.sleep(delay/100)

#commandRamp(6, 6, 100)
#commandRamp(6, 60, 20)
#commandRamp(60, 60, 20)
#commandRamp(60, 6, 100)
#commandRamp(6, 6, 100)


#####_____ Most Efficient List Mode Emulation _____#####

def commandRampAuto(start, end, delay):                                     # Start point (V), End Point, and length of Time
    range = end - start
    unit = delay / 1000
    sleepFlag = 0
    
    PSU.write("RISE:LEV 0")
    PSU.write("FALL:LEV 0")
    PSU.write("VOLT:LEV " + str(round(start, 3)))
    if(range < 0):
        print("FALL:LEV " + str(round(unit, 3)))
        PSU.write("FALL:LEV " + str(round(unit, 3)))
        PSU.write("VOLT:LEV " + str(round(end, 3)))
        sleepFlag = 1
    elif (range > 0):
        print("RISE:LEV " + str(round(unit, 3)))
        PSU.write("RISE:LEV " + str(round(unit, 3)))
        PSU.write("VOLT:LEV " + str(round(end, 3)))
        sleepFlag = 1
    if(sleepFlag == 1):
        while(sleepFlag == 1):
            time.sleep(0.001)
            PSU.write("MEAS:VOLT?")
            output = (PSU.read())
            print(output)
            if(float(output) > end - 1 and float(output) < end + 1):
                sleepFlag = 0
    else:
        time.sleep(unit)

commandRampAuto(6, 6, 100)
commandRampAuto(6, 60, 20)
commandRampAuto(60, 60, 20)
commandRampAuto(60, 6, 100)
commandRampAuto(6, 6, 100)
close()