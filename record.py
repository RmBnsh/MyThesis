import obd #import required libraries
import time
import serial
import csv

obd.logger.setLevel(obd.logging.DEBUG)  #//enable console printing of all debug messages

connection = obd.Async(fast=False) #auto-connects to USB or RF port


rpm_value = 0
speed_value = 0
coolant_value = 0
maf_value = 0
air_status_value = 0
intake_pressure_value = 0
throttle_position_value = 0 

#RPM
def new_rpm(r):
	global rpm_value
	rpm_value = r.value.magnitude
	print("\t")
	
#SPEED
def new_speed(s):
	global speed_value
	speed_value = s.value.magnitude
	print("\t")
	
#COOLANT TEMPERATURE
def new_coolant_temperature(t):
	global coolant_value 
	coolant_value = t.value.magnitude
	print("\t")
	
#MAF AIR FLOW RATE
def new_maf(mf):
	global  maf_value
	maf_value = mf.value.magnitude
	print("\t")
	
#AIR STATUS
def new_air_status(st):
	global air_status_value 
	air_status_value = st.value.magnitude
	print("\t")
	

#INTAKE PRESSURE
def new_intake_pressure(ip):
	global intake_pressure_value 
	intake_pressure_value = ip.value.magnitude
	print("\t")
	
	
#THROTTLE POSITION
def new_throttle_position(tp):
	global throttle_position_value 
	throttle_position_value = tp.value.magnitude 
	print("\t")
	
connection.watch(obd.commands.RPM, callback=new_rpm)
connection.watch(obd.commands.SPEED, callback=new_speed)
connection.watch(obd.commands.COOLANT_TEMP, callback=new_coolant_temperature)
connection.watch(obd.commands.MAF, callback=new_maf)
connection.watch(obd.commands.AIR_STATUS, callback=new_air_status)
connection.watch(obd.commands.INTAKE_PRESSURE, callback=new_intake_pressure)
connection.watch(obd.commands.THROTTLE_POS, callback=new_throttle_position)

connection.start() #the callback now will be anabled for new values
starttime=time.time()
ctime=time.ctime(starttime)

mylist = ["TIME[s],", "SPEED[km/h],", "RPM[rpm],", "COOLANT[degC],", "MAF[g/s],", "AIR STATUS,", "INTAKE PRESSURE,", "THROTTLE POSITION[%]"]
with open ('DATA_'+str(ctime).replace(' ','_')+'.csv', 'w') as f:
    for items in mylist:
        f.write('%s' %items)
    try:
        while True:
            timecount = time.time()-starttime
            print("File Write:",speed_value,rpm_value,coolant_value,maf_value,air_status_value,intake_pressure_value,throttle_position_value)
            f.write(f"\n{timecount},{speed_value},{rpm_value},{coolant_value},{maf_value},{air_status_value},{intake_pressure_value},{throttle_position_value}")
            time.sleep(1.0)
    except KeyboardInterrupt:
        pass
connection.stop()
