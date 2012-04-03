'''
Very simple testbed.
'''

from threading import Thread
from project import SearchThread
from Queue import Queue


class TestBed:
    def __init__(self):
        self.workQueue = Queue()
        self.outputQueue = Queue()

        self.startOutput()
        self.find_all_files()

    def startOutput(self):
        t = Thread(target=self._output, name='outputThread')
        t.daemon = True
        t.start()

    def _output(self):
        while True:
            s = self.outputQueue.get()
            print s
            self.outputQueue.task_done()

    def output(self, s):
        self.outputQueue.put(s)

    def find_all_files(self):
        '''Find all applicable files.'''
        path = './testFiles'
        searchThread = SearchThread([path], ['php', 'php4', 'php5'], self.process_files)
        searchThread.start()

    def process_files(self, files):
        '''Process all the found files.'''
        print 'Got %d files to process.' % len(files)

        queue = Queue()
        [queue.put(filePath) for filePath in files]
        self.queue = queue

        workers = 4
        for i in range(0, workers):
            self.output('Starting worker %d' % i)
            t = Thread(target=self.worker, args=[i])
            t.daemon = True
            t.start()
        self.queue.join()
        print 'Threads done'

    def worker(self, id):
        '''Do the work.'''
        while True:
            filePath = self.queue.get()
            self.lintCheck(filePath, id)
            self.queue.task_done()

    def lintCheck(self, filePath, id):
        self.output('[Worker %d] Lint-checking %s' % (id, filePath))

TestBed()
