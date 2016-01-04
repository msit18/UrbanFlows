from random import randrange

from twisted.internet.defer import DeferredQueue
from twisted.internet.task import deferLater, cooperate
from twisted.internet import reactor


def async(n):
    print 'Starting job', n
    d = deferLater(reactor, n, lambda: None)
    def cbFinished(ignored):
        print 'Finishing job', n
    d.addCallback(cbFinished)
    return d

def worker(jobs):
    while True:
        yield jobs.get().addCallback(async)

def main(stuff):
    jobs = DeferredQueue()

    print len(stuff)
    for i in range(len(stuff)):
        jobs.put(stuff[i])
        print i

    for i in range(6):
        cooperate(worker(jobs))

    reactor.run()


if __name__ == '__main__':
    AList = ['first item', 'second item', "third item", "fourth"]
    main(AList)