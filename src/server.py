#!/usr/bin/env sh
''''which python3 >/dev/null 2>&1 && exec python3 "$0" "$@"                 # '''
''''test $(python --version 2>&1 | cut -c 8) -eq 3 && exec python "$0" "$@" # '''
''''exec echo "Python 3 not found."                                         # '''

import os
import sys

import socket
import threading

from requests import get

import pickle
import time

import select, queue

from log import Log

class Server(Log):
    def __init__(self, serverLocalIP, serverPort):
        if getattr(sys, 'frozen', False):
            # In a bundle
            self.exeDir = os.path.dirname(sys.executable)
        else:
            # In normal python
            self.exeDir = ""
        Log.__init__(self, logFile=os.path.join(self.exeDir, "..", "log", "serverLog.txt"))
        self.clearLog()

        self.reBelServerVersion = "v1.2.0"
        self.log("[INFO] Running ReBel server {}".format(self.reBelServerVersion))

        self.serverLocalIP = serverLocalIP
        self.serverPublicIP = None
        self.serverPort = serverPort

        self.connections = 0
        self.maxConnections = 12

        self.dataSize = 128*2

        self.clients = {}

        self.messageEnd = bytes("/", "utf-8")

        self.frameRate = 1000

        self.incomingMessagesThread = threading.Thread(target=self.incomingMessages, args=(), daemon=True)
        self.outgoingMessagesThread = threading.Thread(target=self.outgoingMessages, args=(), daemon=True)
        self.backgroundTasksThread = threading.Thread(target=self.backgroundTasks, args=(), daemon=True)

        self.numberOfBells = 8
        self.bellStrokeList = ['H'] * self.numberOfBells

    def bellRinging(self, s, stroke, bell):
        try:
            self.clientOutgoingMessageQueue.put(['all', bytes("R:"+self.bellStrokeList[int(bell)-1]+bell ,"utf-8")])
            self.log("[RINGING] Bell {} rung by {}".format(self.bellStrokeList[int(bell)-1]+bell, self.clients[s]['name']))
            self.bellStrokeList[int(bell)-1]  = 'B' if self.bellStrokeList[int(bell)-1] == 'H' else 'H'
        except:
            self.log("[ERROR] Connection to {} ({}:{}) lost".format(self.clients[s]['name'], self.clients[s]['addr'][0], self.clients[s]['addr'][1]))

    def setClientName(self, s, message):
        self.clients[s]['name'] = (message.split(":"))[1]
        self.log("[CONNECT] New connection from {} ({}:{})".format(self.clients[s]['name'], self.clients[s]['addr'][0], self.clients[s]['addr'][1]))
        self.log("[DATA] Number of Connections: {}".format(self.connections))
        self.clientOutgoingMessageQueue.put([s, bytes("setClientName:Success:{}".format(self.clients[s]['name']) ,"utf-8")])

    def clientDisconnect(self, s, message):
        self.log("[CLIENT] Client {} disconnecting with message: {}".format(self.clients[s]['name'], (message.split(":"))[1]))

    def ping(self, s):
        self.clientOutgoingMessageQueue.put([s, bytes("R:B0" ,"utf-8")])
        self.log("[SERVER] Being pinged by {} ({}:{})".format(self.clients[s]['name'], self.clients[s]['addr'][0], self.clients[s]['addr'][1]))

    def startRinging(self, s, message):
        self.log("[COMMAND] StartRinging command received")
        self.clients[s]['ready'] = True
        self.clientOutgoingMessageQueue.put([s, bytes('serverMessage:"{}" command received'.format((message.split(":"))[1]), "utf-8")])

        self.clientOutgoingMessageQueue.put(['all', bytes('ringingCommand:Begin', "utf-8")])

        notReadyCounter = 0

        for client in self.clients.values():
            if client['ready'] == False:
                notReadyCounter += 1
        if notReadyCounter == 0:
            self.log("[RINGING] All connected users ringing")
        else:
            self.log("[RINGING] {}/{} connected users ringing".format(len(self.clients) - notReadyCounter, len(self.clients)))

    def receiveCommand(self, s, message):

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

        elif (message.split(":"))[0] == "bellStates":
            if (message.split(":"))[1] == "get":
                self.clientOutgoingMessageQueue.put([s, bytes("setBellStates:{}".format(self.bellStrokeList) ,"utf-8")])
            elif (message.split(":"))[1] == "set":
                pass

        elif (message.split(":"))[0] == "R":
            self.bellRinging(s, (message.split(":"))[1][0], (message.split(":"))[1][1:])

        elif (message.split(":"))[0] == "":
            self.log("[WARNING] Blank client command, possible deconnection by {} ({}:{})".format(self.clientName, self.addr[0], self.addr[1]))
            self.clientOutgoingMessageQueue.put([s, bytes("serverMessage:[WARNING] Blank client command, are you still there?" ,"utf-8")])

        else:
            self.log('[ERROR] Unrecognised command from client "{}"'.format((message.split(":"))[0]))
            self.clientOutgoingMessageQueue.put([s, bytes('serverMessage:[ERROR] Unrecognised command from client "{}"'.format((message.split(":"))[0]), "utf-8")])

    def incomingMessages(self):
        while True:
            start = time.time()
            try:
                s, message = self.clientIncomingMessageQueue.get_nowait()
            except:
                pass
            else:
                self.receiveCommand(s, message)
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
                        try:
                            client['connection'].send(message+self.messageEnd)
                        except:
                            self.log("[ERROR] Could not send message to client {} ({}:{}). Message: {}".format(self.clients[s]['name'], self.clients[s]['addr'][0], self.clients[s]['addr'][1], message))
                else:
                    s.send(message+self.messageEnd)
            time.sleep(max(1./self.frameRate - (time.time() - start), 0))

    def backgroundTasks(self):
        self.log("[START] Server starting")

        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.setblocking(0)

        try:
            self.server.bind((self.serverLocalIP, self.serverPort))
        except socket.error as e:
            self.log(str(e))

        self.server.listen(self.maxConnections)

        self.inputs = [self.server]
        self.outputs = []

        self.clientIncomingMessageQueue = queue.Queue()
        self.incomingMessagesThread.start()
        self.clientOutgoingMessageQueue = queue.Queue()
        self.outgoingMessagesThread.start()

        self.log("[INFO] Waiting for a connection")
        try:
            self.serverPublicIP = get('https://api.ipify.org').text
        except:
            self.log("[WARNING] Could not determine public IP, will need to find it manually...")
            self.log("[INFO] Server local IP: {}, server port: {}".format(self.serverLocalIP, self.serverPort))
        else:
            self.log("[INFO] Server public IP: {}, server local IP: {}, server port: {}".format(self.serverPublicIP, self.serverLocalIP, self.serverPort))

        while self.inputs:

            start = time.time()

            self.readable, self.writable, self.exceptional = select.select(self.inputs, self.outputs, self.inputs)

            for s in self.readable:
                if s is self.server:
                    connection, addr = s.accept()
                    connection.setblocking(0)
                    self.clients[connection] = {'socket':s, 'connection':connection, 'addr':addr, 'name':None, 'userLevel':'user',
                                                'ready':False}

                    self.clientOutgoingMessageQueue.put([connection, bytes("connectionStatus:Success:Connected to ReBel server:{}".format(self.reBelServerVersion), "utf-8")])
                    self.log("[SERVER] Incoming connection from {}:{}".format(addr[0], addr[1]))
                    self.connections += 1

                    self.inputs.append(connection)
                else:

                    try:
                        data = s.recv(self.dataSize)
                    except:
                        pass
                    else:
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
                                self.log("[CLIENT] Client {} disconnected".format(name_tmp))

            time.sleep(max(1./self.frameRate - (time.time() - start), 0))
 
        for client in self.clients.values():
            client['socket'].close()

    def commandNotFound(self, serverCommandInput):
        self.log('[WARNING] Server command not found: "{}"'.format(serverCommandInput))

    def help(self, args):
        '''
        Returns available server commands, use 'help [command]' for more info on command.
        Parameters
        ----------
        args : The server commands to print more detailed information on.
        #      Each command should be seperated by a blank space, i.e. ' '.
        ----------
        '''
        if len(args) > 0:
            for command in args:
                if command in self.serverCommand:
                    lines = self.serverCommand[command].__doc__.strip().split('\n')
                    self.log("[INFO] help: {}".format(command))
                    self.log("    {}".format(lines[0].strip()))
                    for line in lines[1:]:
                        if len(line.strip().split('#')) == 1:
                            self.log("    {}".format(line.strip().split('#')[0]))
                        else:
                            self.log("     {}".format(line.strip().split('#')[1]))
        else:
            self.log("[INFO] help:")
            for key, value in self.serverCommand.items():
                self.log("    {}: {}".format(key, value.__doc__.strip().split('\n')[0]))

    def quit(self, args):
        '''
        Shuts the server down.
        '''
        self.log("[INFO] Quitting...")
        self.server.close()
        sys.exit(0)

    def exit(self, args):
        '''
        Shuts the server down.
        '''
        self.quit(args)

    def ip(self, args):
        '''
        Displays server IP information.
        '''
        if self.serverPublicIP != None:
            self.log("[INFO] Server public IP: {}, server local IP: {}, server port: {}".format(self.serverPublicIP, self.serverLocalIP, self.serverPort))
        else:
            self.log("[INFO] Server public IP could not be determined, server local IP: {}, server port: {}".format(self.serverLocalIP, self.serverPort))

    def ls(self, args):
        '''
        Lists client connections to the server.
        '''
        self.log("[INFO] {} Connections:".format(self.connections))
        for client in self.clients.values():
            self.log("       {}: {}:{} ({})".format(client['name'], client['addr'][0], client['addr'][1], client['userLevel']))

    def numberofbells(self, args):
        '''
        Gives the number of ringable bells.
        '''
        self.log("[INFO] Number of bells: {}".format(self.numberOfBells))

    def setnumberofbells(self, args):
        '''
        Sets number of ringable bells to the arg being passed in.
        Parameters
        ----------
        numberOfBells : The number of bells to set the amount of ringable bells to.
        ----------
        '''
        self.numberOfBells = int(args[0])
        self.clientOutgoingMessageQueue.put(['all', bytes("setNumberOfBells:{}".format(self.numberOfBells) ,"utf-8")])
        self.bellStrokeList = ['H'] * self.numberOfBells
        self.log("[INFO] Set number of bells to {}".format(self.numberOfBells))

    def bellstrokes(self, args):
        '''
        Prints the current strokes of all the bells.
        '''
        self.log("[INFO] Bell strokes currently are: {}".format(self.bellStrokeList))

    def resetbellstrokes(self, args):
        '''
        Resets the strokes of the bells back to handstroke.
        '''
        self.bellStrokeList = ['H'] * self.numberOfBells
        self.log("[INFO] Resetting bells back to handstroke")

    def getServerCommand(self):

        self.serverCommand = {"help":self.help,
                              "quit":self.quit,
                              "exit":self.exit,
                              "ip":self.ip,
                              "ls":self.ls,
                              "numberofbells":self.numberofbells,
                              "setnumberofbells":self.setnumberofbells,
                              "bellstrokes":self.bellstrokes,
                              "resetbellstrokes":self.resetbellstrokes}
        self.log("[INFO] Type 'help' for help")
        while True:
            start = time.time()

            serverCommandInput = input()
            self.log("[COMMAND] {}".format(serverCommandInput), printMessage=False)
            serverCommandArgs = serverCommandInput.split(" ")[1:]
            serverCommandInput = serverCommandInput.split(" ")[0].lower()

            if serverCommandInput in self.serverCommand:
                self.serverCommand[serverCommandInput](serverCommandArgs)
            elif serverCommandInput == "":
                pass
            else:
                self.commandNotFound(serverCommandInput)

            time.sleep(max(1./self.frameRate - (time.time() - start), 0))

    def start(self):
        self.backgroundTasksThread.start()
        self.getServerCommand()


if __name__ == "__main__":
    serverLocalIP = input("Server local IP (leave blank for default): ")
    if not serverLocalIP:
        serverLocalIP = "0.0.0.0"
    serverPort = input("Server port (leave blank for default of 35555): ")
    if not serverPort:
        serverPort = 35555
    else:
        serverPort = int(serverPort)
    server = Server(serverLocalIP, serverPort)
    server.start()
