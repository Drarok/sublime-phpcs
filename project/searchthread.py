import fnmatch
import os
import threading

import time


class SearchThread(threading.Thread):
    '''Threaded implementation of a project search for given extensions.'''
    def __init__(self, folders, extensions):
        self.folders = folders
        self.extensions = extensions
        self.result = False

        threading.Thread.__init__(self)

    def run(self):
        time.sleep(2)
        self.result = self.get_php_files()

    def get_php_files(self):
        matches = []
        for folder in self.folders:
            for root, folders, filenames in os.walk(folder):
                for extension in self.extensions:
                    extension = '*.' + extension
                    for filename in fnmatch.filter(filenames, extension):
                        matches.append(os.path.join(root, filename))
        matches.sort()
        return matches
