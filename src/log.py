import sys

class Log:
    def __init__(self, logFile):
        self.logFile = logFile

    def clearLog(self):
        with open(self.logFile, 'w') as log:
            pass

    def log(self, message, printMessage=True):
        with open(self.logFile, 'a') as log:
            log.write(message+"\n")
            log.flush()
        if printMessage:
            sys.stdout.write(message+"\n")
            sys.stdout.flush()
