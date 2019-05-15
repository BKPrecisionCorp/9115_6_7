import time
import visa
rm=visa.ResourceManager('@py') #Remove the '@py' if using Ni-Visa (Windows generally)
li=rm.list_resources()
for index in range(len(li)):
    print(str(index)+" - "+li[index])
choice = input("Which device?: ")
vi=rm.open_resource(li[int(choice)])

print(vi.query("*idn?"))
time.sleep(1)
vi.write("*cls") #clear errors...

vi.write("syst:rem")
#Write a sequence of states - 10 sequences available with 1024 points max each
vi.write("seq:edit 1") #using slot 1

#Create the sequence.

#set active steps (binary to decimal) here we have 5 steps (0-4) so binary (00 0001 1111) = 31 in decimal
vi.write("seq:step:active 31")
#steps each takes step#,val
vi.write("seq:volt 1,13.6")
vi.write("seq:curr 1,max")
vi.write("seq:width 1,0.1")
vi.write("seq:slope 1,0.1") #ramp to this point time in seconds

vi.write("seq:volt 2,10")
vi.write("seq:curr 2,max")
vi.write("seq:width 2,0.1")
vi.write("seq:slope 2,0.05")

vi.write("seq:volt 3,12")
vi.write("seq:curr 3,max")
vi.write("seq:width 3,0.2")
vi.write("seq:slope 3,0.05")

vi.write("seq:volt 4,9")
vi.write("seq:curr 4,max")
vi.write("seq:width 4,0.1")
vi.write("seq:slope 4,0.01")

vi.write("seq:volt 5,13.6")
vi.write("seq:curr 5,max")
vi.write("seq:width 5,0.1")
vi.write("seq:slope 5,0.05")

#Save the sequence to memory
vi.write("seq:save")

#A second sequence for slot 2
vi.write("seq:edit 2") 
#set active steps (binary to decimal) here we have 3 steps (0-2) so binary (00 0000 0111) = 7 in decimal
vi.write("seq:step:active 7")
#steps each takes step#,val
vi.write("seq:volt 1,5")
vi.write("seq:curr 1,max")
vi.write("seq:width 1,0.1")
vi.write("seq:slope 1,0.1") #ramp to this point time in seconds

vi.write("seq:volt 2,8")
vi.write("seq:curr 2,max")
vi.write("seq:width 2,0.1")
vi.write("seq:slope 2,0.05")

vi.write("seq:volt 3,13.6")
vi.write("seq:curr 3,max")
vi.write("seq:width 3,0.2")
vi.write("seq:slope 3,0.05")

vi.write("seq:save")

time.sleep(1)

#Create a list that calls the sequence
vi.write("list:state off") # to edit, the list mode must be off
vi.write("list:edit 1")
vi.write("list:repeat 1")
#set the sequences to use here it is just the first
#The set is a binary representation again 00 0000 0011 so step 1 is the only active one
vi.write("list:link:sequence 3")
vi.write("list:power max")
vi.write("list:save")
time.sleep(1)

#recall and set List 1 to active
vi.write("list:recall 1")
vi.write("list:state on") #the trigger will now be active - list starts with a trigger event

time.sleep(2)
#setup trigger for computer control (BUS)
vi.write("trigger:source bus")
#turn on the output and initiate the sequence
vi.write("volt 12")
vi.write("curr 31")
vi.write("outp on")
time.sleep(2)
vi.write("*trg")
time.sleep(2)
vi.write("outp off")
vi.write("list:state off")

vi.close()
