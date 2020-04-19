import sys

class Error:
    def __init__(self):
        pass

    def error(self, message, returnCode):
        sys.stderr.write("[ERROR] {}".format(message))
        sys.exit(returnCode)