import socket
import pickle
import time

import threading
import select, queue

class Network:
    def __init__(self, frameRate=30):
        self.frameRate = frameRate

        self._lock = threading.Lock()
        self.clientThread = threading.Thread(target=self.start, args=(), daemon=True)
        self.incommingMessagesThread = threading.Thread(target=self.incommingMessages, args=(), daemon=True)
        self.outgoingMessagesThread = threading.Thread(target=self.outgoingMessages, args=(), daemon=True)

        self.dataSize = 128
        self.ringing = False
        self.bellsRung = []

        self.messageEnd = bytes("/", "utf-8")

        self.connected = False

    def send(self, message):
        try:
            self.outgoingMessageQueue.put(bytes(message ,"utf-8"))
            print("[CLIENT] {}".format(message))
        except:
            print("[ERROR] Could not send message to server: {}".format(message))

    def setName(self):
        self.send("setClientName:" + self.userName)

    def recieveCommand(self, message):
        if message.split(":")[0] == "connectionStatus":
            if message.split(":")[1] == "Success":
                self.serverVersion = message.split(":")[3]
                print("[SERVER] {} {} on {}:{}".format(message.split(":")[2], self.serverVersion, self.addr[0], self.addr[1]))

                self.setName()
            else:
                print("[SERVER] Could not connect to server, error: {}".format(message.split(":")[1]))
                self.server.close()
                raise
        elif message.split(":")[0] == "serverMessage":
            print("[SERVER] {}".format(message.split(":")[1]))
        elif (message.split(":"))[0] == "setClientName":
            if (message.split(":"))[1] == "Success":
                self.clientName = (message.split(":"))[2]
                print("[SERVER] Name set to {}".format(self.clientName))
            else:
                print("[SERVER] Could not set name, error: {}".format((message.split(":"))[1]))
                self.clientName = "Default"
                print("[SERVER] Using name 'None'")  
        elif message.split(":")[0] == "ringingCommand":
            if message.split(":")[1] == "Begin":
                print("[RINGING] Ringing beginning")
                self.ringing = True 
            else:
                print("[ERROR] Unrecognised ringing command: {}".format((message.split(":"))[1]))
        elif (message.split(":"))[0] == "":
            print("[WARNING] Empty server message, possible deconnection")
        else:
            print('[ERROR] Unrecognised command from server "{}"'.format((message.split(":"))[0]))

    def processRecvdMessage(self, message):
        if self.ringing == True:
            if message[0] != "-":
                self.bellsRung.append(message)
            else:
                pass
        elif self.ringing == False:
            self.recieveCommand(message)

    def incommingMessages(self):
        while True:
            start = time.time()
            try:
                message = self.incommingMessageQueue.get_nowait()
            except:
                pass
            else:
                self.processRecvdMessage(message)
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

        self.incommingMessageQueue = queue.Queue()
        self.incommingMessagesThread.start()
        self.outgoingMessageQueue = queue.Queue()
        self.outgoingMessagesThread.start()

        print("[INFO] Connecting to server...")
        print("[INFO] Server IP: {}, server port: {}".format(self.serverIP, self.serverPort))
        self._lock.acquire()
        try:
            self.server.connect(self.addr)
        except socket.error as e:
            print("Client.start.connect(): {}".format(str(e)))
            inputs = None
            self.connected = False
        else:
            self.server.setblocking(0)
            self.connected = True
        self._lock.release()

        while inputs:
            start = time.time()
            self.readable, self.writable, self.exceptional = select.select(inputs, outputs, inputs)
            for s in self.readable:
                data = s.recv(self.dataSize)
                if data:
                    data = data.decode("utf-8")
                    for message in data.split("/")[:-1]:
                        self.incommingMessageQueue.put(message)
                    if s not in outputs:
                        outputs.append(s)
                else:
                    if s in outputs:
                        outputs.remove(s)
                        inputs.remove(s)
                        s.close()
            time.sleep(max(1./self.frameRate - (time.time() - start), 0))
 
        self.server.close()

    def connect(self, userName, serverIP, serverPort):
        self.userName = userName
        self.serverIP = serverIP
        self.serverPort = serverPort
        self.addr = (self.serverIP, self.serverPort)

        self.clientThread.start()
        time.sleep(0.5)
        self._lock.acquire()
        #self._lock.release()
        if self.connected == False:
            self.clientThread.stop()
        print("connected:", self.connected)
        self._lock.release()
        return self.connected

    def disconnect(self):
        self.client.close()

    def getBellRung(self):
        if len(self.bellsRung) > 0:
            return self.bellsRung.pop(0)

