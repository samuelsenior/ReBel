import csv

class Config:
	def __init__(self, fileName='config.txt'):
		self.fileName = fileName
		self.config = {}
		self.read()
		self.format()

	def read(self):
		with open(self.fileName) as configFile:
			config_tmp = csv.reader(configFile, delimiter=":")
			for config_entry in config_tmp:
				if len(config_entry[1].split(",")) == 1:
					self.config[config_entry[0]] = config_entry[1]
				else:
					self.config[config_entry[0]] = config_entry[1].split(",")

	def format(self):
		self.config['numberOfBells'] = int(self.config['numberOfBells'])
		self.config['numberOfRingableBells'] = int(self.config['numberOfRingableBells'])
		if len(self.config['ringableBells']) == 1:
			self.config['ringableBells'] = int(self.config['ringableBells'])
		else:
			for i, _ in enumerate(self.config['ringableBells']):
				self.config['ringableBells'][i] = int(self.config['ringableBells'][i])
