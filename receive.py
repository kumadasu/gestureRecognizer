import serial
import numpy as np
import matplotlib.pyplot as plt

with serial.Serial('/dev/ttyUSB0', 115200, timeout=3) as ser:
    hpb = [[0, 0, 0]]

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

        hpb = np.vstack([hpb, [h, p, b]])
        if num % 100 == 0 :
            plt.cla
            plt.plot(hpb)
            plt.pause(0.0000001)
