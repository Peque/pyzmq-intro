import zmq
import time


ctx = zmq.Context()
sck = ctx.socket(zmq.REQ)

sck.connect('tcp://127.0.0.1:9876')

for i in range(10):
    sck.send_string('Hello!')
    print(sck.recv_string())
    time.sleep(1)
