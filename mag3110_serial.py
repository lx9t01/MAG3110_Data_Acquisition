#############################################
##     Record Serial Data from USB port    ##
##          by Haixiang Xu                 ##
##          Note: requires serial lib      ##
#############################################


import serial
import matplotlib.pyplot as plt



connected = False
locations = ['/dev/tty.usbmodem1421','/dev/tty.usbmodem1411','/dev/ttyUSB0','/dev/ttyUSB1','/dev/ttyUSB2','/dev/ttyUSB3','dev/tty.usbserial','/dev/cu.usbmodem1421']

for device in locations:
    try:
        print "Trying...",device
        ser = serial.Serial(device, 9600)
        break
    except:
        print "Failed to connect on",device

while not connected:
    serin = ser.read()
    connected = True;

outfile = open("result.txt", 'w');

############### record plot ###############
time = []
data = [[],[],[],[]]
lines = ['r-','g-','b-','k-']
s = ""
idx = 1

plt.ioff()
fig = plt.figure(num=1)
lnx, = plt.plot(time, data[0], 'r-')
lny, = plt.plot(time, data[1], 'g-')
lnz, = plt.plot(time, data[2], 'b-')
lnt, = plt.plot(time, data[3], 'k-')
fig.show()

while 1:
    if ser.inWaiting():
        x=ser.read()
        outfile.write(x)
        s = s + x
        if x=="\n":
            print s
            try:
                [t, nx, ny, nz, nt] = s.split(' ')
                # print(t+" "+nx+" "+ny+" "+nz+" "+nt)
                time.append(int(t))
                data[0].append(float(nx))
                data[1].append(float(ny))
                data[2].append(float(nz))
                data[3].append(float(nt))
                
            except ValueError:
                pass
            s = ""
            idx += 1
        outfile.flush()

        if idx % 20 == 0:
            lnx.set_xdata(time)
            lnx.set_ydata(data[0])
            lny.set_xdata(time)
            lny.set_ydata(data[1])
            lnz.set_xdata(time)
            lnz.set_ydata(data[2])
            lnt.set_xdata(time)
            lnt.set_ydata(data[3])
            plt.axis([time[0], time[0] + 6000, -300, 300])
            plt.draw()
            plt.pause(0.005)

        if idx % 60 == 0:
            fig = plt.clf()
            time = []
            data = [[],[],[],[]]
            lnx, = plt.plot(time, data[0], 'r-')
            lny, = plt.plot(time, data[1], 'g-')
            lnz, = plt.plot(time, data[2], 'b-')
            lnt, = plt.plot(time, data[3], 'k-')
            idx = 1

## close the serial connection and text file
outfile.close()
ser.close()