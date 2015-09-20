import zmq
import time
import threading


class Worker(threading.Thread):

    def __init__(self, context, uri, alias=None):
        threading.Thread.__init__(self)
        self.alias = alias
        self.socket = context.socket(zmq.PULL)
        self.socket.connect(uri)

    def run(self):
        while True:
            msg = self.socket.recv_string()
            time.sleep(1.5)
            print('%s processed by %s!' % (msg.split()[-1], self.alias))
        self.socket.close()


class Ventilator(threading.Thread):

    def __init__(self, context, uri):
        threading.Thread.__init__(self)
        self.socket = context.socket(zmq.PUSH)
        self.socket.bind(uri)

    def run(self):
        for i in range(100):
            print('Pushing %i' % i)
            self.socket.send_string('%i' % i)
            time.sleep(0.5)
        self.socket.close()


ctx = zmq.Context()
uri = 'tcp://127.0.0.1:5555'

actors = []
actors.append(Ventilator(ctx, uri))
actors.append(Worker(ctx, uri, 'WK0'))
actors.append(Worker(ctx, uri, 'WK1'))

for actor in actors:
    actor.start()

time.sleep(15)
actors.append(Worker(ctx, uri, 'WK2').start())
actors.append(Worker(ctx, uri, 'WK3').start())
actors.append(Worker(ctx, uri, 'WK4').start())

for actor in actors:
    actor.join()
