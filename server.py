import socket
import threading

import pickle
import time

import select, queue

class Server:
    def __init__(self, serverIP, serverPort):
        self.ReBelServerVersion = "v0.2.10"

        self.serverIP = serverIP
        self.serverPort = serverPort

        self.connections = 0
        self.maxConnections = 6

        self.dataSize = 128

        self.clients = {}
        #self.allReadyToRing = False

        self.messageEnd = bytes("/", "utf-8")

        self.frameRate = 100

        self.incomingMessagesThread = threading.Thread(target=self.incomingMessages, args=(), daemon=True)
        self.outgoingMessagesThread = threading.Thread(target=self.outgoingMessages, args=(), daemon=True)
        self.backgroundTasksThread = threading.Thread(target=self.backgroundTasks, args=(), daemon=True)

        self.numberOfBells = 8
        self.bellStrokeList = ['B'] * self.numberOfBells

    def bellRinging(self, s, stroke, bell):
        try:
            self.bellStrokeList[int(bell)-1]  = 'B' if self.bellStrokeList[int(bell)-1] == 'H' else 'H'
            self.clientOutgoingMessageQueue.put(['all', bytes("R:"+self.bellStrokeList[int(bell)-1]+bell ,"utf-8")])
            print("[RINGING] Bell {} rung by {}".format(self.bellStrokeList[int(bell)-1]+bell, self.clients[s]['name']))
        except:
            print("[ERROR] Connection to {} ({}:{}) lost".format(self.clients[s]['name'], self.clients[s]['addr'][0], self.clients[s]['addr'][1]))

    def setClientName(self, s, message):
        self.clients[s]['name'] = (message.split(":"))[1]
        print("[CONNECT] New connection from {} ({}:{})".format(self.clients[s]['name'], self.clients[s]['addr'][0], self.clients[s]['addr'][1]))
        print("[DATA] Number of Connections:", self.connections)
        self.clientOutgoingMessageQueue.put([s, bytes("setClientName:Success:{}".format(self.clients[s]['name']) ,"utf-8")])

    def clientDisconnect(self, s, message):
        print("[CLIENT] Client {} disconnecting with message: {}".format(self.clients[s]['name'], (message.split(":"))[1]))

    def ping(self, s):
        self.clientOutgoingMessageQueue.put([s, bytes("0" ,"utf-8")])
        print("[SERVER] Being pinged by {} ({}:{})".format(self.clients[s]['name'], self.clients[s]['addr'][0], self.clients[s]['addr'][1]))

    def startRinging(self, s, message):
        print("[COMMAND] StartRinging command recieved")
        self.clients[s]['ready'] = True
        self.clientOutgoingMessageQueue.put([s, bytes('serverMessage:"{}" command recieved'.format((message.split(":"))[1]), "utf-8")])

        self.clientOutgoingMessageQueue.put(['all', bytes('ringingCommand:Begin', "utf-8")])

        notReadyCounter = 0

        for client in self.clients.values():
            if client['ready'] == False:
                notReadyCounter += 1
        if notReadyCounter == 0:
            print("[RINGING] All connected users ringing")
        else:
            print("[RINGING] {}/{} connected users ringing".format(len(self.clients) - notReadyCounter, len(self.clients)))

    def recieveCommand(self, s, message):

        if message == "clientCommand:startRinging":
            self.startRinging(s, message)
        elif (message.split(":"))[0] == "setClientName":
            self.setClientName(s, message)
        elif (message.split(":"))[0] == "clientDisconnect":
            self.clientDisconnect(s, message)
        elif (message.split(":"))[0] == "ping":
            self.ping(s)
        elif (message.split(":"))[0] == "numberOfBells":
            if (message.split(":"))[1] == "get":
                self.clientOutgoingMessageQueue.put([s, bytes("setNumberOfBells:{}".format(self.numberOfBells) ,"utf-8")])
            elif (message.split(":"))[1] == "set":
                pass
        elif (message.split(":"))[0] == "R":
            self.bellRinging(s, (message.split(":"))[1][0], (message.split(":"))[1][1:])
        elif (message.split(":"))[0] == "":
            print("[WARNING] Blank client command, possible deconnection by {} ({}:{})".format(self.clientName, self.addr[0], self.addr[1]))
            self.clientOutgoingMessageQueue.put([s, bytes("serverMessage:[WARNING] Blank client command, are you still there?" ,"utf-8")])
        else:
            print('[ERROR] Unrecognised command from client "{}"'.format((message.split(":"))[0]))
            self.clientOutgoingMessageQueue.put([s, bytes('serverMessage:[ERROR] Unrecognised command from client "{}"'.format((message.split(":"))[0]), "utf-8")])

    def incomingMessages(self):
        while True:
            start = time.time()
            try:
                s, message = self.clientIncomingMessageQueue.get_nowait()
            except:
                pass
            else:
                self.recieveCommand(s, message)
            time.sleep(max(1./self.frameRate - (time.time() - start), 0))

    def outgoingMessages(self):
        while True:
            start = time.time()
            try:
                s, message = self.clientOutgoingMessageQueue.get_nowait()
            except:
                pass
            else:
                if s == 'all':
                    for client in self.clients.values():
                        client['connection'].send(message+self.messageEnd)
                else:
                    s.send(message+self.messageEnd)
            time.sleep(max(1./self.frameRate - (time.time() - start), 0))

    def backgroundTasks(self):
        print("[START] Server starting")

        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.setblocking(0)

        try:
            self.server.bind((self.serverIP, self.serverPort))
        except socket.error as e:
            print(str(e))

        self.server.listen(self.maxConnections)

        self.inputs = [self.server]
        self.outputs = []

        self.clientIncomingMessageQueue = queue.Queue()
        self.incomingMessagesThread.start()
        self.clientOutgoingMessageQueue = queue.Queue()
        self.outgoingMessagesThread.start()

        print("[INFO] Waiting for a connection")
        print("[INFO] Server IP: {}, server port: {}".format(self.serverIP, self.serverPort))

        while self.inputs:

            start = time.time()

            self.readable, self.writable, self.exceptional = select.select(self.inputs, self.outputs, self.inputs)

            for s in self.readable:
                if s is self.server:
                    connection, addr = s.accept()
                    connection.setblocking(0)
                    self.clients[connection] = {'socket':s, 'connection':connection, 'addr':addr, 'name':None, 'userLevel':'user',
                                                'ready':False}

                    self.clientOutgoingMessageQueue.put([connection, bytes("connectionStatus:Success:Connected to ReBel server:{}".format(self.ReBelServerVersion), "utf-8")])
                    print("[SERVER] Incoming connection from {}:{}".format(addr[0], addr[1]))
                    self.connections += 1

                    self.inputs.append(connection)
                else:

                    data = s.recv(self.dataSize)
                    if data:
                        data = data.decode("utf-8")
                        for message in data.split("/")[:-1]:
                            self.clientIncomingMessageQueue.put([s, message])

                        if s not in self.outputs:
                            self.outputs.append(s)
                    else:
                        if s in self.outputs:
                            self.outputs.remove(s)
                            self.inputs.remove(s)
                            name_tmp = self.clients[s]['name']
                            self.clients.pop(s)
                            s.close()
                            self.connections -= 1
                            print("[CLIENT] Client {} disconnected".format(name_tmp))

            time.sleep(max(1./self.frameRate - (time.time() - start), 0))
 
        for client in self.clients.values():
            client['socket'].close()

    def getServerCommand(self):
        while True:
            start = time.time()

            serverCommand = input()

            if (serverCommand.split(" "))[0] == "quit":
                self.server.close()
                quit()
            elif (serverCommand.split(" "))[0] == "ls":
                print("{} Connections:".format(self.connections))
                for client in self.clients.values():
                    print("{}: {}:{} ({})".format(client['name'], client['addr'][0], client['addr'][1], client['userLevel']))
            elif (serverCommand.split(" "))[0] == "numberofbells":
                print("Number of bells: {}".format(self.numberOfBells))
            elif (serverCommand.split(" "))[0] == "setnumberofbells":
                self.numberOfBells = int((serverCommand.split(" "))[1])
                self.clientOutgoingMessageQueue.put(['all', bytes("setNumberOfBells:{}".format(self.numberOfBells) ,"utf-8")])
                self.bellStrokeList = ['B'] * self.numberOfBells
                print("Set number of bells to {}".format(self.numberOfBells))

            time.sleep(max(1./self.frameRate - (time.time() - start), 0))

    def start(self):
        self.backgroundTasksThread.start()
        self.getServerCommand()


if __name__ == "__main__":
    serverIP = input("Server IP (leave blank for default): ")
    if not serverIP:
        serverIP = "0.0.0.0"
    serverPort = input("Server port (leave blank for default of 35555): ")
    if not serverPort:
        serverPort = 35555
    else:
        serverPort = int(serverPort)
    server = Server(serverIP, serverPort)
    server.start()
