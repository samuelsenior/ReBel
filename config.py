import csv

class Config:
    def __init__(self, fileName='config.txt'):
        self.fileName = fileName
        self.config = {'numberOfBells':None, 'ringableBells':None,
                       'scale':None, 'octaveShift':None, 'pitchShift':None,
                       'testConnectionLatency':[False, 0,100]}
        self.read()
        self.format()

    def read(self):
        with open(self.fileName) as configFile:
            config_tmp = csv.reader(configFile, delimiter=":")
            for config_entry in config_tmp:
                if len(config_entry) > 1:

                    #df[['position','company']] = df['position'].str.rsplit('-', n=1, expand=True)

                    if len(config_entry[1].split(",")) == 1:
                        self.config[config_entry[0]] = config_entry[1]
                    else:
                        self.config[config_entry[0]] = config_entry[1].split(",")
                else:
                    pass

    def format(self):
        if self.config['numberOfBells'] == None:
            self.config['numberOfBells'] = 4
        else:
            self.config['numberOfBells'] = int(self.config['numberOfBells'])

        if self.config['ringableBells'] == None:
            self.config['ringableBells'] = [1,2,3,4]
        else:
            if len(self.config['ringableBells']) == 1:
                self.config['ringableBells'] = int(self.config['ringableBells'])
            else:
                for i, _ in enumerate(self.config['ringableBells']):
                    self.config['ringableBells'][i] = int(self.config['ringableBells'][i])

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
