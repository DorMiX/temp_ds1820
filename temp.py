import os
import glob
import time
from datetime import datetime
from datetime import timedelta

# These tow lines mount the device:
os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')
 
base_dir = '/sys/bus/w1/devices/'
# Get all the filenames begin with 10 in the path base_dir.
device_folder = glob.glob(base_dir + '00*')
print(device_folder)
device_file = device_folder + '/w1_slave'
def read_rom():
    name_file=device_folder+'/name'
    f = open(name_file,'r')
    return f.readline()
 
def read_temp_raw():
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    return lines
 
def read_temp():
    lines = read_temp_raw()
    # Analyze if the last 3 characters are 'YES'.
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw()
    # Find the index of 't=' in a string.
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        # Read the temperature .
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0
        return temp_c


#print(' rom: '+ read_rom())
df = "/home/pi/Documents/meresi_adatok.csv"
dt = timedelta(seconds=300)
with open(df, "a") as macsv:
    if os.stat(df).st_size == 0:
        macsv.write("Time,Celsius\n")
        

while True:
    t1 = datetime.now()
    now = datetime.now()
    #print(str(now) + ' C=%3.3f  F=%3.3f'% read_temp())
    with open(df, "a") as macsv:
        macsv.write(str(now.strftime("%Y-%m-%d %H:%M:%S"))+',%2.2f\n'% read_temp())
        macsv.flush()
    t2 = datetime.now()
    real_dt = (dt - (t2-t1)).total_seconds()
    time.sleep(real_dt)
