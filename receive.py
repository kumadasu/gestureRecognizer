import serial
import numpy as np
import matplotlib.pyplot as plt
import math


def projection_to_plane(hpb):
    h = hpb[0]/360*2*math.pi
    p = hpb[1]/360*2*math.pi
    return [math.tan(h), math.tan(-p)/math.cos(h)]

fig, ax = plt.subplots()

x = []
y = []

points, = ax.plot(x, y, marker='o', linestyle='--')
size = 5
ax.set_xlim(-size, size)
ax.set_ylim(-size, size)

with serial.Serial('/dev/ttyUSB0', 115200, timeout=3) as ser:
    for num in range(1,5000):
        line = ser.readline()

        # Send character to start DMP streaming when timeout occurs.
        if not line:
            print('send starting character')
            ser.write(b' ')
            continue

        # Only print line if it is not formatted.
        test = line.strip(b'\r\n').split(b'\t')
        if not len(test) == 4:
            print(line)
            continue

        # Treat strings as float if it is formatted.
        (header, h, p, b) = [t(s) for t, s in zip((str, float, float, float), line.strip(b'\r\n').split(b'\t'))]
        print(header, h, p, b)

        hpb = [h, p, b]
        x_coord, y_coord = projection_to_plane(hpb)
        x.append(x_coord)
        y.append(y_coord)
        points.set_data(x, y)
        if num % 20 == 0 :
            plt.pause(0.0000001)
