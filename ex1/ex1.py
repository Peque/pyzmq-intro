import zmq
import time
import threading


N_MESSAGES = 1000
N_REQUESTERS = 3


class Requester(threading.Thread):

    def __init__(self, context, uri, alias=None):
        threading.Thread.__init__(self)
        self.alias = alias
        self.socket = context.socket(zmq.REQ)
        self.socket.connect(uri)

    def run(self):
        for i in range(N_MESSAGES):
            self.socket.send_string('%s (%s)' % (self.alias, i))
            self.socket.recv_string()
        self.socket.close()


class Replier(threading.Thread):

    def __init__(self, context, uri, alias=None):
        threading.Thread.__init__(self)
        self.alias = alias
        self.socket = context.socket(zmq.REP)
        self.socket.bind(uri)

    def run(self):
        for i in range(N_MESSAGES * N_REQUESTERS):
            self.socket.recv_string()
            self.socket.send_string('ACK')
        self.socket.close()


ctx = zmq.Context()
uri = 'inproc://127.0.0.1:9999'

actors = []
for i in range(N_REQUESTERS):
    actors.append(Requester(ctx, uri, 'REQ%s' % i))
actors.append(Replier(ctx, uri, 'REP0'))

t0 = time.time()
for actor in actors:
    actor.start()
for actor in actors:
    actor.join()
t1 = time.time()

print(t1 - t0)
