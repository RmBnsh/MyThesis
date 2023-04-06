import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

plt.style.use('classic')
#print(plt.style.available)

narg = len(sys.argv)
if narg>=2:
    filename=sys.argv[1]
else:
    filename = input('Enter filename to plot: ')

dataframe = pd.read_csv(filename)
time=np.array(dataframe.iloc[:,0])
vehicle_speed=np.array(dataframe.iloc[:,1])

#---Plot
fig = plt.figure()
ax = plt.axes()

plt.xlabel(dataframe.columns[0].replace("_"," ").replace("["," ["))
plt.ylabel(dataframe.columns[1].replace("_"," ").replace("["," ["))

ax.plot(time,vehicle_speed)

plotfilename = filename.split('.')[-2]+".png"
fig.savefig(plotfilename)

speed=vehicle_speed/3.6
dt=time-np.roll(time,1)
dt[0]=dt[1]
acceleration=(np.roll(speed,-1)-np.roll(speed,1))/(dt+np.roll(dt,-1))   #Using central differentiation
power=()

#---Kinematic analysis
print("Average speed [km/h]",np.average(vehicle_speed))
print("Max speed [km/h]",np.max(vehicle_speed))
print("Distance [m]",np.sum(speed*dt))
print("Max acceleration [m/s2]",np.max(acceleration))
print("Max deceleration [m/s2]",np.min(acceleration))

#---Energy analysis
if narg<3:
    exit()

import json

f=open(sys.argv[2])
param=json.load(f)
f.close()

Cd=param['Aerodynamic_coefficient[-]']
Af=param['Frontal_area[m2]']
Cr=param['Rolling_resistance_coefficient[-]']
mv=param['Weight[kg]']

g=9.81  #m/s2   gravitational acceleration
T=298 #K    Ambient temperature
P=101325    #Pa Ambient pressure
Ma=0.029    #kg/mol Air molecular mass
Ru=8.314    #J/molK Universal gas constant

rho=P*Ma/(Ru*T)

Fr=Cr*mv*g
Fa=Cd*Af*1/2*rho*speed**2
Ftot=mv*acceleration
Fg=0    #gradient

Ftr=Ftot+Fr+Fa+Fg
Wtr=Ftr*speed   #W  traction power

print(np.min(Wtr),np.max(Wtr))
