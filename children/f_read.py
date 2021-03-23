import serial
import time

path = "/dev/ttyUSB0"

s = serial.Serial(path,9600)
s.reset_input_buffer()
s.reset_output_buffer()
s.write("manual_connect\r\n".encode("ascii"))
s.flush()
s.reset_input_buffer()
s.reset_output_buffer()
s.write("dados\r\n".encode("ascii"))
s.flush()
time.sleep(1)
y = s.read_until(b'\n').decode("ascii").strip("\n").strip("\r")
s.reset_input_buffer()
s.reset_output_buffer
y = y.split(" ")
print(f"RESPONSE: {y}")
s.close()

