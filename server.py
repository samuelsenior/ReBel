import socket
from _thread import *
import pickle
import time

import select, queue

class Server:
    def __init__(self, serverIP, serverPort):
        self.ReBelServerVersion = "v0.2.1"

        self.serverIP = serverIP
        self.serverPort = serverPort

        self.connections = 0
        self.maxConnections = 6

        self.dataSize = 128

        self.clients = {}
        self.allReadyToRing = False

        self.messageEnd = bytes("/", "utf-8")

        self.frameRate = 30

    def bellRinging(self, s, bell):
        try:
            self.clientOutgoingMessageQueue.put(['all', bytes(bell ,"utf-8")])
            print("[RINGING] Bell {} rung by {}".format(bell, self.clients[s]['name']))
        except:
            print("[ERROR] Connection to {} ({}:{}) lost".format(self.clients[s]['name'], self.clients[s]['addr'][0], self.clients[s]['addr'][1]))

    def setClientName(self, s, message):
        self.clients[s]['name'] = (message.split(":"))[1]
        print("[CONNECT] New connection from {} ({}:{})".format(self.clients[s]['name'], self.clients[s]['addr'][0], self.clients[s]['addr'][1]))
        print("[DATA] Number of Connections:", self.connections)
        self.clientOutgoingMessageQueue.put([s, bytes("setClientName:Success:{}".format(self.clients[s]['name']) ,"utf-8")])

    def clientDisconnect(self, s, message):
        print("[CLIENT] Client {} disconnecting with message: {}".format(self.clients[s]['name'], (message.split(":"))[1]))

    def startRinging(self, s, message):
        print("[COMMAND] StartRinging command recieved")
        self.startRinging_bool = True
        self.clients[s]['ready'] = True
        self.clientOutgoingMessageQueue.put([s, bytes('serverMessage:[SERVER] "{}" command recieved'.format((message.split(":"))[1]), "utf-8")])

        notReadyCounter = 0
        readyCounter = 0

        for client in self.clients.values():
            if client['ready'] == False:
                notReadyCounter += 1
        if notReadyCounter == 0:
            self.clientOutgoingMessageQueue.put(['all', bytes('ringingCommand:Begin', "utf-8")])
            self.allReadyToRing = True
            #self.dataSize = 3
            print("[RINGING] All users ready to ring, starting...")
        else:
            print("[RINGING] {}/{} users ready to ring".format(len(self.clients) - notReadyCounter, len(self.clients)))

    def recieveCommand(self, s, message):

        if message == "clientCommand:startRinging":
            self.startRinging(s, message)
        elif (message.split(":"))[0] == "setClientName":
            self.setClientName(s, message)
        elif (message.split(":"))[0] == "clientDisconnect":
            self.clientDisconnect(s, message)
        elif self.allReadyToRing == True:
            self.bellRinging(s, message)
        elif (message.split(":"))[0] == "":
            print("[WARNING] Blank client command, possible deconnection by {} ({}:{})".format(self.clientName, self.addr[0], self.addr[1]))
            self.clientOutgoingMessageQueue.put([s, bytes("serverMessage:[WARNING] Blank client command, are you still there?" ,"utf-8")])
        else:
            print('[ERROR] Unrecognised command from client "{}"'.format((message.split(":"))[0]))
            self.clientOutgoingMessageQueue.put([s, bytes('serverMessage:[ERROR] Unrecognised command from client "{}"'.format((message.split(":"))[0]), "utf-8")])

    def incommingMessages(self):
        while True:
            start = time.time()
            try:
                s, message = self.clientIncommingMessageQueue.get_nowait()
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

        self.clientIncommingMessageQueue = queue.Queue()
        start_new_thread(self.incommingMessages, ())
        self.clientOutgoingMessageQueue = queue.Queue()
        start_new_thread(self.outgoingMessages, ())

        print("[INFO] Waiting for a connection")
        print("[INFO] Server IP: {}, server port: {}".format(self.serverIP, self.serverPort))

        while self.inputs:

            self.readable, self.writable, self.exceptional = select.select(self.inputs, self.outputs, self.inputs)

            for s in self.readable:
                if s is self.server:
                    connection, addr = s.accept()
                    connection.setblocking(0)
                    self.clients[connection] = {'socket':s, 'connection':connection, 'addr':addr, 'name':None, 'userLevel':'user',
                                                'ready':False}

                    self.clientOutgoingMessageQueue.put([connection, bytes("connectionStatus:Success:Connected to ReBel server: {}".format(self.ReBelServerVersion), "utf-8")])
                    print("[SERVER] Incoming connection from {}:{}".format(addr[0], addr[1]))
                    self.connections += 1

                    self.inputs.append(connection)
                else:

                    data = s.recv(self.dataSize)
                    if data:
                        data = data.decode("utf-8")
                        for message in data.split("/")[:-1]:
                            self.clientIncommingMessageQueue.put([s, message])

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
 
        for client in self.clients.values():
            client['socket'].close()

    def getServerCommand(self):
        while True:
            start = time.time()

            serverCommand = input()

            if serverCommand == "quit":
                self.server.close()
                quit()
            elif serverCommand == "ls":
                print("{} Connections:".format(self.connections))
                for client in self.clients.values():
                    print("{}: {}:{} ({})".format(client['name'], client['addr'][0], client['addr'][1], client['userLevel']))

            time.sleep(max(1./self.frameRate - (time.time() - start), 0))

    def start(self):
        start_new_thread(self.backgroundTasks, ())
        self.getServerCommand()


if __name__ == "__main__":
    serverIP = input("Server IP: ")
    serverPort = int(input("Server port: "))
    server = Server(serverIP, serverPort)
    server.start()
