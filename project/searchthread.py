import fnmatch
import os
import threading


class SearchThread(threading.Thread):
    '''Threaded implementation of a project search for given extensions.'''
    def __init__(self, folders, extensions, callback=None):
        self.folders = folders
        self.extensions = extensions
        self.callback = callback
        self.result = False

        threading.Thread.__init__(self)

    def run(self):
        self.result = self.get_php_files()
        if self.callback:
            self.callback(self.result)

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
