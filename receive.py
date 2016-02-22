import serial
import numpy as np
import matplotlib.pyplot as plt
import math
import mathutils


def projection_to_plane(quat):
    vec_n = mathutils.Vector((1, 0, 0))
    vec_rotate = vec_n.copy()
    vec_rotate.rotate(quat)
    return [-vec_rotate.y, -vec_rotate.z]


fig, ax = plt.subplots()
plt.axis('off')
x_data = []
y_data = []

points, = ax.plot(x_data, y_data, marker='None', linestyle='solid', linewidth=20, color='black')
size = 1.2
ax.set_xlim(-size, size)
ax.set_ylim(-size, size)

with serial.Serial('/dev/ttyUSB0', 115200, timeout=3) as ser:
    for i in range(0, 20):
        x_data = []
        y_data = []
        for num in range(1,400):
            line = ser.readline()

            # Send character to start DMP streaming when timeout occurs.
            if not line:
                print('send starting character')
                ser.write(b' ')
                continue

            # Only print line if it is not formatted.
            test = line.strip(b'\r\n').split(b'\t')
            if not len(test) == 5:
                print(line)
                continue

            # Treat strings as float if it is formatted.
            (header, w, x, y, z) = [t(s) for t, s in zip((str, float, float, float, float), line.strip(b'\r\n').split(b'\t'))]

            # Construct quaternion
            quat = mathutils.Quaternion((w, x, y, z))
            quat.normalize()

            # Calculate coordinate
            x_coord, y_coord = projection_to_plane(quat)

            # Draw points
            x_data.append(x_coord)
            y_data.append(y_coord)
            points.set_data(x_data, y_data)
            if num % 20 == 0:
                plt.pause(0.0000001)
        print("Image:"+"{0:02d}".format(i))
        plt.savefig("test" + "{0:02d}".format(i) + ".png", format='png')
