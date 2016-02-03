import serial

with serial.Serial('/dev/ttyUSB0', 115200, timeout=3) as ser:
    while 1:
        line = ser.readline()
        if not line:
            print('send starting character')
            ser.write(b' ')
            continue
        # print(line)
        print(line.strip(b'\r\n').split(b'\t'))
