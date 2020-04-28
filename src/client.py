import socket
import pickle
import time

import threading
import select, queue

from log import Log

class Network(Log):
    def __init__(self, logFile, frameRate=30):

        self.logFile = logFile

        Log.__init__(self, logFile=logFile)

        self.frameRate = frameRate

        self._lock = threading.Lock()
        self.clientThread = threading.Thread(target=self.start, args=(), daemon=True)
        self.incomingMessagesThread = threading.Thread(target=self.incomingMessages, args=(), daemon=True)
        self.outgoingMessagesThread = threading.Thread(target=self.outgoingMessages, args=(), daemon=True)

        self.disconnecting = False

        self.dataSize = 128
        self.ringing = False
        self.bellsRung = []

        self.messageEnd = bytes("/", "utf-8")

        self.connected = False
        self.gotNumberOfBells = False
        self.numberOfBells = []

    def send(self, message):
        try:
            self.outgoingMessageQueue.put(bytes(message ,"utf-8"))
            #self.log("[CLIENT] {}".format(message))
        except:
            self.log("[ERROR] Could not send message to server: {}".format(message))

    def setName(self):
        self.send("setClientName:" + self.userName)

    def receiveCommand(self, message):
        if message.split(":")[0] == "connectionStatus":
            if message.split(":")[1] == "Success":
                self.serverVersion = message.split(":")[3]
                self.log("[SERVER] {} {} on {}:{}".format(message.split(":")[2], self.serverVersion, self.addr[0], self.addr[1]))
                self.setName()
            else:
                self.log("[SERVER] Could not connect to server, error: {}".format(message.split(":")[1]))
                self.server.close()
                raise
        elif message.split(":")[0] == "serverMessage":
            self.log("[SERVER] {}".format(message.split(":")[1]))
        elif (message.split(":"))[0] == "setClientName":
            if (message.split(":"))[1] == "Success":
                self.clientName = (message.split(":"))[2]
                self.log("[SERVER] Name set to {}".format(self.clientName))
            else:
                self.log("[SERVER] Could not set name, error: {}".format((message.split(":"))[1]))
                self.clientName = "Default"
                self.log("[SERVER] Using name 'None'")  
        elif (message.split(":"))[0] == "setNumberOfBells":
            self.numberOfBells.append(int(message.split(":")[1]))
            self.gotNumberOfBells = True
            self.log("[SERVER] Number of ringing bells is {}".format(message.split(":")[1]))
        elif message.split(":")[0] == "ringingCommand":
            if message.split(":")[1] == "Begin":
                self.log("[RINGING] Ringing beginning")
                self.ringing = True 
            else:
                self.log("[ERROR] Unrecognised ringing command: {}".format((message.split(":"))[1]))
        elif (message.split(":"))[0] == "R":
            self.bellsRung.append(((message.split(":"))[1][0], (message.split(":"))[1][1:]))
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
            time.sleep(max(1./self.frameRate - (time.time() - start), 0))

    def outgoingMessages(self):
        while True:
            start = time.time()
            try:
                message = self.outgoingMessageQueue.get_nowait()
            except:
                pass
            else:
                self.server.send(message+self.messageEnd)
            time.sleep(max(1./self.frameRate - (time.time() - start), 0))

    def start(self):

        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        inputs = [self.server]
        outputs = []

        self.incomingMessageQueue = queue.Queue()
        self.incomingMessagesThread.start()
        self.outgoingMessageQueue = queue.Queue()
        self.outgoingMessagesThread.start()

        self.log("[INFO] Connecting to server...")
        self.log("[INFO] Server IP: {}, server port: {}".format(self.serverIP, self.serverPort))
        self._lock.acquire()
        try:
            self.server.connect(self.addr)
        except socket.error as e:
            self.log("Client.start.connect(): {}".format(str(e)))
            inputs = None
            self.connected = False
        else:
            self.server.setblocking(0)
            self.connected = True
        self._lock.release()

        self.running = True
        while self.running:
            start = time.time()
            try:
                self.readable, self.writable, self.exceptional = select.select(inputs, outputs, inputs)
            except:
                pass
            else:
                for s in self.readable:
                    data = s.recv(self.dataSize)
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
            time.sleep(max(1./self.frameRate - (time.time() - start), 0))
 
        self.server.close()
        self.connected = False
        self.disconnecting = False

    def connect(self, userName, serverIP, serverPort):
        while self.disconnecting:
            time.sleep(0.1)

        self.__init__(logFile=self.logFile)

        self.userName = userName
        self.serverIP = serverIP
        self.serverPort = serverPort
        self.addr = (self.serverIP, self.serverPort)

        self.clientThread.start()
        time.sleep(0.5)
        self._lock.acquire()
        if self.connected == False:
            self.clientThread.stop()
        self._lock.release()
        return self.connected

    def disconnect(self):
        self.disconnecting = True
        self.running = False

    def getNumberOfBells(self):
        if self.gotNumberOfBells == True:
            return self.numberOfBells.pop(0)
        else:
            raise

    def getBellRung(self):
        if len(self.bellsRung) > 0:
            return self.bellsRung.pop(0)
        else:
            raise

