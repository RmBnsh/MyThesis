import termux
import csv
import time
from math import radians,cos,sin,asin,sqrt

def haversine(lat1, lon1, lat2, lon2):
    #https://en.wikipedia.org/wiki/Haversine_formula

    R =  6372.8e3 #[m]   3959.87433 is in miles.  For Earth radius in kilometers use 6372.8 km

    dLat = radians(lat2 - lat1)
    dLon = radians(lon2 - lon1)
    lat1 = radians(lat1)
    lat2 = radians(lat2)

    a = sin(dLat/2)**2 + cos(lat1)*cos(lat2)*sin(dLon/2)**2
    c = 2*asin(sqrt(a))

    return R * c    #Same units as R

# Open CSV file
csvfile = open('test.csv', 'w', newline='')
# Create CSV writer
writer = csv.writer(csvfile, delimiter="\t", dialect="excel")

writer.writerow(["Time[s]","Latitude[deg]","Longidute[deg]","Altitude[m]","Accuracy[m]","Bearing[deg]","Speed_meas[m/s]","Speed_comp[m/s]"])
ptime=[]
latitude=[]
longitude=[]
accuracy=[]
#for i in range(100):
while True:
    try:
        #sensors=termux.Sensors.allSensorsData()
        #data=termux.Sensors.sensorsData("")
        result,location,something=termux.API.location()
        t = time.localtime()
        current_time = time.strftime("%H:%M:%S", t)
        rtime=time.time()
        #print(location)
        if location:
            ptime.append(rtime)
            latitude.append(location["latitude"])
            longitude.append(location["longitude"])
            accuracy.append(location["accuracy"])
            if len(ptime)>2:    #   At least three data points
                ds=haversine(latitude[-1],longitude[-1],latitude[-2],longitude[-2])
                dt=ptime[-1]-ptime[-2]
                if ds<accuracy[-1]+accuracy[-2]:
                    #try with bigger time step
                    ds=haversine(latitude[-1],longitude[-1],latitude[-3],longitude[-3])
                    dt=ptime[-1]-ptime[-3]
                    if ds<accuracy[-1]+accuracy[-3]:    
                        #if accuracy is small again, assume position has not changed.
                        ds=0
                speed_comp=ds/dt
            else:
                speed_comp=-9.9 #not enough data
            writer.writerow([rtime,location["latitude"],location["longitude"],location["altitude"],location["accuracy"],location["bearing"],location["speed"],speed_comp])
            print(f'{current_time}\t{location["speed"]*3.6:<7.1f}\t{speed_comp*3.6:<7.1f}')
        else:
            time.sleep(1)
            print(current_time, "NoSignal")
    except KeyboardInterrupt:
        break

csvfile.close()
