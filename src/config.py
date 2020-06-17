import csv
import os
import sys

class Config:
    def __init__(self, fileName):
        self.fileName = fileName
        self.config = {'numberOfBells':None, 'ringableBells':None, 'keys':None,
                       'bellStates':None,
                       'tuningSource':None, 'scale':None, 'octaveShift':None, 'pitchShift':None,
                       'testConnectionLatency':[False, 0,100],
                       'regenerateBells':False,
                       'handbellSource':None, 'rebelBellFileLocation':None, 'abelBellFileLocation':None,
                       'frameRate':None}
        if getattr(sys, 'frozen', False):
            # In a bundle
            self.exeDir = os.path.dirname(sys.executable)
        else:
            # In normal python
            self.exeDir = ""
        self.read()
        self.format()

    def read(self):
        with open(self.fileName) as configFile:
            config_tmp = csv.reader(configFile, delimiter=":")
            for config_entry in config_tmp:
                if len(config_entry) > 2:
                    for i in range(len(config_entry) - 2):
                        config_entry[1] += ":" + config_entry[2]
                        config_entry.pop(2)
                if len(config_entry) > 1:
                    if len(config_entry[1].split(",")) == 1:
                        self.config[config_entry[0]] = config_entry[1]
                    else:
                        self.config[config_entry[0]] = config_entry[1].split(",")
                else:
                    pass

    def format(self):
        if self.config['numberOfBells'] == None:
            self.config['numberOfBells'] = 8
        else:
            self.config['numberOfBells'] = int(self.config['numberOfBells'])

        if self.config['ringableBells'] == None:
            self.config['ringableBells'] = [1,2]
        else:
            ringableBells_tmp = []
            if len(self.config['ringableBells']) == 1:
                if self.config['ringableBells'].isdigit():
                    ringableBells_tmp = [int(self.config['ringableBells'])]
                else:
                    ringableBells_tmp = [1]
            else:
                for i, bell in enumerate(self.config['ringableBells']):
                    if self.config['ringableBells'][i].isdigit():
                        ringableBells_tmp.append(int(self.config['ringableBells'][i]))
                    else:
                        pass
            self.config['ringableBells'] = ringableBells_tmp

        if self.config['keys'] == None:
            self.config['keys'] = ['j', 'f']
        else:
            key_tmp = []
            if len(self.config['keys']) == 1:
                if self.config['keys'].isdigit() or self.config['keys'].isalpha():
                    key_tmp = [self.config['keys']]
                else:
                    key_tmp = ['j']
            else:
                for i, key in enumerate(self.config['keys']):
                    if self.config['keys'][i].isdigit() or self.config['keys'][i].isalpha():
                        key_tmp.append(self.config['keys'][i])
                    else:
                        pass
            self.config['keys'] = key_tmp
        if len(self.config['ringableBells']) > len(self.config['keys']):
            self.config['ringableBells'] = self.config['ringableBells'][:len(self.config['keys'])]
        elif len(self.config['keys']) > len(self.config['ringableBells']):
            self.config['keys'] = self.config['keys'][:len(self.config['ringableBells'])]

        if self.config['bellStates'] == None:
            self.config['bellStates'] = ['B'] * self.config['numberOfBells']
        else:
            bellStates_tmp = []
            if len(self.config['bellStates']) == 1:
                if self.config['bellStates'].lower() == 'b' or self.config['bellStates'].lower() == 'h':
                    bellStates_tmp = [self.config['bellStates'].upper()]
                else:
                    bellStates_tmp = ['B']
            else:
                for i, state in enumerate(self.config['bellStates']):
                    if self.config['bellStates'][i].lower() == 'b' or self.config['bellStates'][i].lower() == 'h':
                        bellStates_tmp.append(self.config['bellStates'][i].upper())
                    else:
                        pass
            self.config['bellStates'] = bellStates_tmp
        if len(self.config['bellStates']) > self.config['numberOfBells']:
            self.config['bellStates'] = self.config['bellStates'][:len(self.config['numberOfBells'])]

        if self.config['tuningSource'] == None:
            self.config['tuningSource'] = 'server'
        elif (self.config['tuningSource'] != 'server') and (self.config['tuningSource'] != 'client'):
            self.config['tuningSource'] = 'server'
        if self.config['scale'] == None:
            self.config['scale'] = "major"
        else:
            pass
        if self.config['octaveShift'] == None:
            self.config['octaveShift'] = 0
        else:
            self.config['octaveShift'] = int(self.config['octaveShift'])

        if self.config['pitchShift'] == None:
            self.config['pitchShift'] = 0
        else:
            self.config['pitchShift'] = int(self.config['pitchShift'])

        if self.config['testConnectionLatency'][0] == 'True':
            self.config['testConnectionLatency'][0] = True
            self.config['testConnectionLatency'][1] = int(self.config['testConnectionLatency'][1])
            self.config['testConnectionLatency'][2] = int(self.config['testConnectionLatency'][2])

        if self.config['regenerateBells'] == 'True':
            self.config['regenerateBells'] = True
        else:
            self.config['regenerateBells'] = False

        if self.config['handbellSource'] == None:
            self.config['handbellSource'] = 'rebel'

        if self.config['rebelBellFileLocation'] == None:
            self.config['rebelBellFileLocation'] = os.path.join(self.exeDir, "..", 'audio', 'handbell.wav')
        else:
            tmp = self.config['rebelBellFileLocation'].split('/|\\')
            self.config['rebelBellFileLocation'] = ""
            for t in tmp:
                self.config['rebelBellFileLocation'] = os.path.join(self.config['rebelBellFileLocation'], t)
            self.config['rebelBellFileLocation'] = os.path.join(self.exeDir, self.config['rebelBellFileLocation'])

        if self.config['abelBellFileLocation'] == None:
            pass
        else:
            tmp = self.config['abelBellFileLocation'].split('/|\\')
            self.config['abelBellFileLocation'] = ""
            for t in tmp:
                self.config['abelBellFileLocation'] = os.path.join(self.config['abelBellFileLocation'], t)
            self.config['abelBellFileLocation'] = os.path.join(self.exeDir, self.config['abelBellFileLocation'])

        if self.config['frameRate'] == None:
            self.config['frameRate'] = 500
        else:
            self.config['frameRate'] = int(self.config['frameRate'])

    def get(self, dictKey):
        return self.config[dictKey]

    def set(self, dictKey, value):
        self.config[dictKey] = value
