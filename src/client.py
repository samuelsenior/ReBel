import socket
import pickle
import time

import threading
from multiprocessing import Process, Queue
from multiprocessing import Manager
import multiprocessing

import select

from log import Log

class NetworkSubprocess(Log):
    def __init__(self, logFile, incomingMessageQueue, outgoingMessageQueue, bellsRung, variables):
        self.logFile = logFile
        Log.__init__(self, logFile=logFile)

        self.incomingMessageQueue = incomingMessageQueue
        self.outgoingMessageQueue = outgoingMessageQueue

        self.bellsRung = bellsRung

        self.variables = variables

        self.incomingMessagesThread = threading.Thread(target=self.incomingMessages, args=(), daemon=True)
        self.outgoingMessagesThread = threading.Thread(target=self.outgoingMessages, args=(), daemon=True)

    def send(self, message):
        try:
            self.outgoingMessageQueue.put(bytes(message, "utf-8"))
        except:
            self.log("[ERROR] Could not send message to server: {}".format(message))

    def setName(self):
        self.send("setClientName:" + self.variables['userName'])

    def receiveCommand(self, message):

        if message.split(":")[0] == "connectionStatus":
            if message.split(":")[1] == "Success":
                self.variables['serverVersion'] = message.split(":")[3]
                self.log("[SERVER] {} {} on {}:{}".format(message.split(":")[2], self.variables['serverVersion'], self.variables['addr'][0], self.variables['addr'][1]))
                self.setName()
            else:
                self.log("[SERVER] Could not connect to server, error: {}".format(message.split(":")[1]))
                self.server.close()
                raise
        elif message.split(":")[0] == "serverMessage":
            self.log("[SERVER] {}".format(message.split(":")[1]))
        elif (message.split(":"))[0] == "setClientName":
            if (message.split(":"))[1] == "Success":
                self.variables['clientName'] = (message.split(":"))[2]
                self.log("[SERVER] Name set to {}".format(self.variables['clientName']))
            else:
                self.log("[SERVER] Could not set name, error: {}".format((message.split(":"))[1]))
                self.variables['clientName'] = "Default"
                self.log("[SERVER] Using name 'None'")  
        elif (message.split(":"))[0] == "setNumberOfBells":
            self.variables['numberOfBells'] = int(message.split(":")[1])
            self.variables['gotNumberOfBells'] = True
            self.log("[SERVER] Number of ringing bells is {}".format(message.split(":")[1]))
        elif message.split(":")[0] == "ringingCommand":
            if message.split(":")[1] == "Begin":
                self.log("[RINGING] Ringing beginning")
                self.variables['ringing'] = True 
            else:
                self.log("[ERROR] Unrecognised ringing command: {}".format((message.split(":"))[1]))
        elif (message.split(":"))[0] == "R":
            self.bellsRung.put(((message.split(":"))[1][0], (message.split(":"))[1][1:]))
        elif (message.split(":"))[0] == "":
            self.log("[WARNING] Empty server message, possible deconnection")
        else:
            self.log('[ERROR] Unrecognised command from server "{}"'.format((message.split(":"))[0]))

    def incomingMessages(self):
        while True:
            start = time.time()
            try:
                message = self.incomingMessageQueue.get_nowait()
            except:
                pass
            else:
                self.receiveCommand(message)
            time.sleep(max(1./self.variables['frameRate'] - (time.time() - start), 0))

    def outgoingMessages(self):
        while True:
            start = time.time()
            try:
                message = self.outgoingMessageQueue.get_nowait()
            except:
                pass
            else:
                self.server.send(message+self.variables['messageEnd'])
            time.sleep(max(1./self.variables['frameRate'] - (time.time() - start), 0))

    def start(self):
        self._lock = threading.Lock()
        Log.__init__(self, logFile=self.logFile)

        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        inputs = [self.server]
        outputs = []

        self.incomingMessagesThread.start()
        self.outgoingMessagesThread.start()

        self.log("[INFO] Connecting to server...")
        self.log("[INFO] Server IP: {}, server port: {}".format(self.variables['serverIP'], self.variables['serverPort']))
        self._lock.acquire()
        try:
            self.server.connect(self.variables['addr'])
        except socket.error as e:
            self.log("[ERROR] Client.start.connect(): {}".format(str(e)))
            inputs = None
            self.variables['connected'] = False
            self.variables['running'] = False
        else:
            self.server.setblocking(0)
            self.variables['connected'] = True
            self.variables['running'] = True
        self._lock.release()

        while self.variables['running']:
            start = time.time()
            try:
                self.readable, self.writable, self.exceptional = select.select(inputs, outputs, inputs)
            except:
                pass
            else:
                for s in self.readable:
                    data = s.recv(self.variables['dataSize'])
                    if data:
                        data = data.decode("utf-8")
                        for message in data.split("/")[:-1]:
                            self.incomingMessageQueue.put(message)
                        if s not in outputs:
                            outputs.append(s)
                    else:
                        if s in outputs:
                            outputs.remove(s)
                            inputs.remove(s)
                            s.close()
            time.sleep(max(1./self.variables['frameRate'] - (time.time() - start), 0))
 
        self.server.close()
        self.variables['connected'] = False
        self.variables['disconnecting'] = False

class Network(Log):
    def __init__(self, logFile, frameRate=30):

        multiprocessing.freeze_support()

        self.logFile = logFile
        Log.__init__(self, logFile=logFile)
        self.incomingMessageQueue = Queue()
        self.outgoingMessageQueue = Queue()

        self.bellsRung = Queue()

        manager = Manager()
        self.variables = manager.dict({'frameRate':frameRate, 'disconnecting':False, 'dataSize':128, 'ringing':False,
                                       'messageEnd':bytes("/", "utf-8"), 'connected':None, 'gotNumberOfBells':False, 'numberOfBells':0,
                                       'userName':"", 'serverIP':"", 'serverPort':-1, 'addr':None, 'serverVersion':'-1.-1.-1',
                                       'clientName':"", 'running':False, 'messagingThreadsClosed':False})

    def send(self, message):
        try:
            self.outgoingMessageQueue.put(bytes(message, "utf-8"))
        except:
            self.log("[ERROR] Could not send message to server: {}".format(message))

    def startNetworkSubProcess(logFile, incomingMessageQueue, outgoingMessageQueue, bellsRung, variables):
        networkSubprocess = NetworkSubprocess(logFile, incomingMessageQueue, outgoingMessageQueue, bellsRung, variables)
        networkSubprocess.start()

    def connect(self, userName, serverIP, serverPort):

        while self.variables['disconnecting']:
            time.sleep(0.1)

        self.__init__(logFile=self.logFile)

        self.variables['userName'] = userName
        self.variables['serverIP'] = serverIP
        self.variables['serverPort'] = serverPort
        self.variables['addr'] = (self.variables['serverIP'], self.variables['serverPort'])

        self.clientThread = Process(target=Network.startNetworkSubProcess, args=(self.logFile, self.incomingMessageQueue, self.outgoingMessageQueue, self.bellsRung, self.variables))
        self.clientThread.start()
        time.sleep(0.5)

        if self.variables['connected'] == False:
            self.clientThread.join()

        return self.variables['connected']

    def disconnect(self):
        self.variables['disconnecting'] = True
        self.variables['running'] = False

    def shutdown(self):

        self.disconnect()

        try:
            self.incomingMessagesThread.join()
        except:
            pass

        try:
            self.outgoingMessagesThread.join()
        except:
            pass

        self.clientThread.join()

    def getNumberOfBells(self, empty=False):
        if empty:
            self.variables['gotNumberOfBells'] = False
        else:
            if self.variables['gotNumberOfBells'] == True:
                return self.variables['numberOfBells']
            else:
                raise

    def getBellRung(self):
        try:
            return self.bellsRung.get_nowait()
        except:
            raise

    def getVar(self, key):
        return self.variables[key]

    def setVar(self, key, value):
        self.variables[key] = value

    def threadsRunning(self):
        return self.clientThread.is_alive()
