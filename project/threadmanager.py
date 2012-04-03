import project
from Queue import Queue
import sublime
import threading
import time


class ThreadManager:
    _instance = None
    threads = None

    @classmethod
    def instance(cls):
        if cls._instance is None:
            cls._instance = ThreadManager()
        return cls._instance

    def __init__(self, window, extensions):
        self.threads = Queue()
        self.window = window
        self.extensions = extensions
        self.stages = [self.find_files, self.check_files]
        self.run_next_stage()

    def run_next_stage(self):
        if self.stages:
            stage = self.stages.pop(0)
            stage()

    def find_files(self):
        threads = []
        thread = project.SearchThread(self.window.folders(), self.extensions)
        threads.append(thread)
        thread.start()
        self.handle_threads(threads)

    def check_files(self):
        threads = []
        thread = threading.Thread(target=self.do_nothing)
        thread.result = True
        threads.append(thread)
        thread.start()
        self.handle_threads(threads)

    def do_nothing(self):
        time.sleep(2)

    def handle_threads(self, threads, i=0, delta=1):
        next_threads = []
        for thread in threads:
            if thread.is_alive():
                next_threads.append(thread)
                continue
            if thread.result == False:
                continue
            print 'Thread finished: %s with result \'%s\'' % (
                str(thread), str(thread.result))
        threads = next_threads

        if len(threads):
            # Cheap animation.
            before = i % 8
            after = 7 - before
            if not after:
                delta = -1
            if not before:
                delta = 1
            i += delta
            view = sublime.active_window().active_view()
            view.set_status('phpcs', 'PHPCS [%s=%s] (%d)' % (' ' * before, ' ' * after, len(threads)))

            sublime.set_timeout(lambda: self.handle_threads(threads, i, delta), 100)
        else:
            sublime.active_window().active_view().erase_status('phpcs')
            self.run_next_stage()
