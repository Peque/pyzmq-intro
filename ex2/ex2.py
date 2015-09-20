import zmq
import time
import threading


class Subscriber(threading.Thread):

    def __init__(self, context, uris, topics, alias=None):
        threading.Thread.__init__(self)
        self.alias = alias
        self.topics = topics
        self.socket = context.socket(zmq.SUB)
        for uri in uris:
            self.socket.connect(uri)
        for topic in topics:
            self.socket.setsockopt(zmq.SUBSCRIBE, topic.encode('ascii'))

    def run(self):
        while True:
            print('%s received: %s' % (self.alias, self.socket.recv_string()))
        self.socket.close()


class Publisher(threading.Thread):

    def __init__(self, context, uri, topics, alias=None):
        threading.Thread.__init__(self)
        self.alias = alias
        self.topics = topics
        self.socket = context.socket(zmq.PUB)
        self.socket.bind(uri)

    def run(self):
        for i in range(10000):
            for topic in self.topics:
                self.socket.send_string('%s %s (%s)' % (topic, self.alias, i))
            time.sleep(1)
        self.socket.close()


ctx = zmq.Context()
uri0 = 'tcp://127.0.0.1:9999'
uri1 = 'tcp://127.0.0.1:9998'

pub0 = Publisher(ctx, uri0, ['A', 'B', 'X'], 'PUB0')
pub0.start()

time.sleep(10)

sub0 = Subscriber(ctx, [uri0], ['A', 'B'], 'SUB0')
sub0.start()

time.sleep(10)

sub1 = Subscriber(ctx, [uri0, uri1], ['A', 'C'], 'SUB1')
sub1.start()

time.sleep(10)

pub1 = Publisher(ctx, uri1, ['A', 'C'], 'PUB1')
pub1.start()
