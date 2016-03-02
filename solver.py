import serial
import matplotlib.pyplot as plt
from use_archive import classify_with_archive

imgname = 'test.png'
digits_archive_file = '/home/kumadasu/Downloads/20160221-235633-61bc_epoch_30.0.tar.gz'


def projection_to_plane(quat):
    w = quat[0]
    x = quat[1]
    y = quat[2]
    z = quat[3]
    return [2*(x*y-w*z), 2*(x*z+w*y)]


fig, ax = plt.subplots()
plt.axis('off')
x_data = []
y_data = []

points, = ax.plot(x_data, y_data, marker='None', linestyle='solid', linewidth=10, color='black')
size = 1.2
ax.set_xlim(-size, size)
ax.set_ylim(-size, size)

with serial.Serial('/dev/ttyUSB0', 115200, timeout=3) as ser:
    for i in range(1):
        x_data = []
        y_data = []
        for num in range(1,800):
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
            quat = [w, x, y, z]
            norm = w*w+x*x+y*y+z*z
            quat[:] = [val/norm for val in quat]

            # Calculate coordinate
            x_coord, y_coord = projection_to_plane(quat)

            # Draw points
            x_data.append(x_coord)
            y_data.append(y_coord)
            points.set_data(x_data, y_data)
            if num % 20 == 0:
                plt.pause(0.0000001)
        plt.savefig(imgname, format='png')

classify_with_archive(digits_archive_file, [imgname], use_gpu=False)
