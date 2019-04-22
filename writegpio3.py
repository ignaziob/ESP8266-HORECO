import RPi.GPIO as GPIO
import time
import sys
import json

debug = 1

def gpio_activate_relays(i,j): 
#HW configuration
  GPIO.setmode(GPIO.BCM) #GPIO numbers
  RELAY1_GPIO = 18 # my relay board connects IN1 to GPIO18
  RELAY2_GPIO = 23 # my relays board connects IN2 to GPIO23
  RELAY3_GPIO = 17 # my relays board connects IN3 to GPIO23
  RELAY4_GPIO = 27 # my relays board connects IN4 to GPIO23

  GPIO.setup(RELAY1_GPIO, GPIO.OUT) #assign mode
  GPIO.setup(RELAY2_GPIO, GPIO.OUT) #assign mode
  GPIO.setup(RELAY3_GPIO, GPIO.OUT) #assign mode
  GPIO.setup(RELAY4_GPIO, GPIO.OUT) #assign mode

#parameters validation
  if i<1 or i>4 :
    if debug == 1 : print("DEBUG: error first parameter not in range (0,1)")
    sys.exit( -2) # exit -2 error parameter #1

  if (j[:3] != "OFF") and j[0:2] != "ON" :
    if debug == 1 : print ("DEBUG: error 2nd parameter shall contain ON/OFF")
    sys.exit(-3) #exit -3 error paramete #2
 
  if (j[:2] == "ON") :
    set_status = GPIO.LOW
  else :
    set_status = GPIO.HIGH

  if i == 1 : 
    GPIO.output(RELAY1_GPIO, set_status) #on/off       
  if i == 2 :
    GPIO.output(RELAY2_GPIO, set_status) #on/off
  if i == 3 : 
    GPIO.output(RELAY3_GPIO, set_status) #on/off       
  if i == 4 : 
    GPIO.output(RELAY4_GPIO, set_status) #on/off       
#end def gpio_activate_relays(i,j)


#main program start
#read from json the file with remote actuator status

# if 2 paramenters then using from command line
if (len(sys.argv)) == 3 : 
  relayID=int(sys.argv[1])
  relayStatus=(sys.argv[2]).upper() # convert on/off to CAPITAL  
  if relayID<1 or relayID>4 :
    if debug == 1 : print ("DEBUG: error 1st parameter not in range [1-4]")
    sys.exit(-12) #exit -12 error paramete #1
    
  if (relayStatus[:3] != "OFF") and relayStatus	[0:2] != "ON" :
    if debug == 1 : print ("DEBUG: error 2nd parameter shall contain ON/OFF")
    sys.exit(-13) #exit -13 error paramete #2
  print ("ID=",relayID,"Status=",relayStatus[:3])
  gpio_activate_relays(relayID,relayStatus)
  exit (0)

# using the relaystatus.txt as input
# previously created with curl
with open('relaystatus.txt') as json_data:
  d = json.load(json_data)

if debug == 1 : 
  print (" DEBUG: ID2 ",d["2"])
  print (" DEBUG: ID1 ",d["1"])
  print (" DEBUG: ID3 ",d["3"])
  print (" DEBUG: ID4 ",d["4"])

gpio_activate_relays(1,d["1"])
gpio_activate_relays(2,d["2"])
gpio_activate_relays(3,d["3"])
gpio_activate_relays(4,d["4"])

if debug == 1 :
 print( " DEBUG: end program",sys.argv[0])

sys.exit(0)

