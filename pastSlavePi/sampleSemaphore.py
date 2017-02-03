from twisted.internet.defer import DeferredSemaphore, gatherResults, DeferredList
from twisted.internet.task import deferLater, LoopingCall
from twisted.internet import reactor, defer
import glob, time

def async(n):
    print 'Starting job', n
    # d = deferLater(reactor, n, lambda: None)
    d = defer.Deferred()
    def cbFinished(ignored):
        print 'Finishing job', n
    d.addCallback(cbFinished)
    return d

def upload_pull(i):
    allVideos = glob.glob('*.py')
    dl = defer.Deferred()
    # d = deferLater(reactor, 1, lambda: None)
    for item in range(len(allVideos)):
        print "sending file: ", allVideos[item]
        time.sleep(1)

    print "finished"
    def cbFinished(ignored):
        print 'Finishing job', i

    dl.addCallback(cbFinished)
    return dl

def main():
    sem = DeferredSemaphore(1)

    #Need to figure out how to add enough callbacks to last for the entire session
    # jobs = []
    # for i in range(5):
    #     jobs.append(sem.run(upload_pull, i))

    d = DeferredList()
    for i in range(5):
        d.append(sem.run(upload_pull, i))

    d = DeferredList(dl) 
    # d = gatherResults(jobs)
    d.addCallback(lambda ignored: reactor.stop())
    reactor.run()

# def main():
#     sem = DeferredSemaphore(3)

#     jobs = []
#     for i in range(10):
#         jobs.append(sem.run(async, i))

#     d = gatherResults(jobs)
#     d.addCallback(lambda ignored: reactor.stop())
#     reactor.run()

# def runFiles():
#     keepRunning = True
#     semi = DeferredSemaphore(1)

#     while keepRunning = True:
#         jobs = []
#         job.append(semi.run(collectFiles))
#         jobs = DeferredList(jobs)
#         def cbFinished(ignored):
#             print 'Finishing job'
#         def checkProcess(ignored):
#             if var=False:
#                 keepRunning = False
#                 reactor.stop()

#         jobs.addCallback(cbFinished)
#     return jobs

#Manage whole process
def runFiles():
    semi = DeferredSemaphore(1)

    jobs = []
    for runs in range(5):
        jobs.append(semi.run(collectFiles))

    # jobs = DeferredList(jobs)
    def cbFinished(ignored):
        print 'Finishing job'
    # jobs.addCallback(cbFinished)
    print "Finished"
    return jobs

#Glob + upload > every 45 mins run this process?
def collectFiles():
    semaphore = DeferredSemaphore(1)
    files = glob.glob('*.py')
    dl = list()

    for item in range(len(files)):
        #Queues list of things to be sent (one item at a time-for loop)
        dl.append(semaphore.run(sendFiles, files[item]))

    # get a DefferedList
    dl = DeferredList(dl)
    def cbFinished(ignored):
        print 'Finishing job'
    dl.addCallback(cbFinished)
    return dl

#Upload SCP files
def sendFiles(img):
    print "sending img: ", img
    time.sleep(0.5)
    return "finished"



def thing_that_does_http():
    # create semaphore to manage the deferreds
    semaphore = DeferredSemaphore(1)

    # create a list with all urls to check
    files = glob.glob('*.py')
    dl = list()

    # append deferreds to list
    for item in range(len(files)):
        # returns deferred
        dl.append(semaphore.run(sendFiles, files[item]))

    # get a DefferedList
    dl = DeferredList(dl)
    def cbFinished(ignored):
        print 'Finishing job'
    dl.addCallback(cbFinished)

    # add some callbacks for error handling
    # dl.addErrback(self._handleError)
    return dl

# def main():
#     loop_http = LoopingCall(thing_that_does_http)
#     # # run once per minute, starting now.
#     loop_http.start(10)
#     reactor.run()

if __name__ == '__main__':
    # main()
    # upload_pull(3)

    # thing_that_does_http()
    runFiles()

    # reactor.listenTCP(8123, TCPEventReceiverFactory())
    # loop_http = LoopingCall(thing_that_does_http)
    # # # run once per minute, starting now.
    # loop_http.start(10)
    # reactor.run()