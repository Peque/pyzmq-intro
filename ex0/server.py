import zmq
import sys


ctx = zmq.Context()
sck = ctx.socket(zmq.REP)

sck.bind('tcp://127.0.0.1:9876')

while True:
    sck.recv_string()
    sck.send_string('World!')
