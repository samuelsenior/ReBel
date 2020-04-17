from pydub import AudioSegment
import pygame
import numpy as np
import os
import csv

class Audio:
    def __init__(self, numberOfBells, mixer, config, inputFileName):
        self.inputFileName = inputFileName

        self.numberOfBells = numberOfBells
        self.config = config
        self.mixer = mixer

        self.bellSemitones = []
        self.bells = {}
        # Major scale formula: t t s t t t s
        self.majorScale = [0, 2, 4, 5, 7, 9, 11, 12]
        # Natural minor scale: t s t t s t t
        self.naturalMinorScale = [0, 2, 3, 5, 7, 8, 10, 12]
        # Harmonic minor scale: t s t t 1.5t s
        self.harmonicMinorScale = [0, 2, 3, 5, 7, 8, 11, 12]
        # Melodic minor scale: t s t t t t s
        self.melodicMinorScale = [0, 2, 3, 5, 7, 9, 11, 12]
        if self.config.config['scale'] == "major":
            self.scale = self.majorScale
        elif self.config.config['scale'] == "naturalMinor":
            self.scale = self.naturalMinorScale
        elif self.config.config['scale'] == "harmonicMinor":
            self.scale = self.harmonicMinorScale
        elif self.config.config['scale'] == "melodicMinor":
            self.scale = self.melodicMinorScale

        self.regenerateBells = True
        self.checkGeneratedBells()
        if self.regenerateBells == True:
            self.generateBells()
        if self.config.config['regenerateBells'] == True:
            print("[INFO] Config regenerate bells option is True")
            self.generateBells()

        self.loadBells()

    def checkGeneratedBells(self):
        self.regenerateBells = True
        self.bellSpecFileLocation = os.path.join('audio', 'bsf')
        # Check BSF exists
        if os.path.isfile(self.bellSpecFileLocation):
            # If it doesn't the regenerate bells
            #   self.regenerateBells = True
            bellSpec = {}

            # If it does then read it in
            with open(self.bellSpecFileLocation, 'r') as bellSpecFile:
                bellSpecFile_reader = csv.reader(bellSpecFile, delimiter=":")
                for bellSpecLine in bellSpecFile_reader:
                    bellSpec[bellSpecLine[0]] = bellSpecLine[1]
        
            bellSpec['scale'] = bellSpec['scale'].split(",")
            bellSpec['scale'] = [int(b) for b in bellSpec['scale']]
            bellSpec['numberOfBells'] = int(bellSpec['numberOfBells'])
            bellSpec['octaveShift'] = int(bellSpec['octaveShift'])
            bellSpec['pitchShift'] = int(bellSpec['pitchShift'])

            if bellSpec['scaleName'] == self.config.config['scale'] \
               and bellSpec['scale'] == self.scale \
               and bellSpec['numberOfBells'] == self.config.config['numberOfBells'] \
               and bellSpec['octaveShift'] == self.config.config['octaveShift'] \
               and bellSpec['pitchShift'] == self.config.config['pitchShift'] \
               and bellSpec['handbellSource'] == self.config.config['handbellSource']:
                self.regenerateBells = False
                print("[INFO] Config file bell options match bell spec file")
            else:
                print("[INFO] Config file bell options do not match bell spec file, regenerating bells")

    def writeBellSpecFile(self):
        print("[INFO] Writing bell spec file")
        self.bellSpecFileLocation = os.path.join('audio', 'bsf')
        with open(self.bellSpecFileLocation, 'w') as bellSpecFile:
            bellSpecFile.write("{}:{}\n".format("scaleName", self.config.config['scale']))
            bellSpecFile.write("{}:".format("scale"))
            for i, _ in enumerate(self.scale):
                if i > 0:
                    bellSpecFile.write(",")
                bellSpecFile.write("{}".format(self.scale[i]))
            bellSpecFile.write("\n")
            bellSpecFile.write("{}:{}\n".format("numberOfBells", self.config.config['numberOfBells']))
            bellSpecFile.write("{}:{}\n".format("octaveShift", self.config.config['octaveShift']))
            bellSpecFile.write("{}:{}\n".format("pitchShift", self.config.config['pitchShift']))
            bellSpecFile.write("{}:{}\n".format("handbellSource", self.config.config['handbellSource']))

    def generateBells(self):

        print("[INFO] Generating bells")

        self.bellSemitones = [0]
        j = 0
        for j in range(int(self.numberOfBells/8)):
            self.bellSemitones.append(self.scale[1]+j*12)
            for i in range(2, 8):
                if j*8 + i < self.numberOfBells:
                    self.bellSemitones.append(self.scale[i]+j*12)
        if self.numberOfBells < 8:
            for i in range(self.numberOfBells):
                if len(self.bellSemitones) < self.numberOfBells:
                    self.bellSemitones.append(self.scale[i+1])
        else:
            for i in range(8):
                if len(self.bellSemitones) < self.numberOfBells:
                    self.bellSemitones.append(self.scale[i+1]+(j+1)*12)

        sound = AudioSegment.from_file(self.inputFileName, format="wav")

        if self.config.config['handbellSource'] == 'abel':
            sound = sound.high_pass_filter(cutoff=500)
            sound = sound.high_pass_filter(cutoff=500)
            sound = sound.high_pass_filter(cutoff=500)
        elif self.config.config['handbellSource'] == 'rebel':
            sound = sound.high_pass_filter(cutoff=400)
            sound = sound.high_pass_filter(cutoff=400)
            sound = sound.high_pass_filter(cutoff=400)

            sound = sound.low_pass_filter(cutoff=7750)
            sound = sound.low_pass_filter(cutoff=7750)
            sound = sound.low_pass_filter(cutoff=7750)

        for i, semitone in enumerate(self.bellSemitones):
            octave = 12
            new_sample_rate = int(sound.frame_rate * (2.0 ** (self.config.config['octaveShift'] + (self.config.config['pitchShift']+semitone)/octave)))
            pitchShifted_sound = sound._spawn(sound.raw_data, overrides={'frame_rate': new_sample_rate})

            pitchShifted_sound = pitchShifted_sound.set_frame_rate(44100)

            if self.config.config['handbellSource'] == 'abel':
                fadeTime = int(len(pitchShifted_sound)*0.95)
                pitchShifted_sound = pitchShifted_sound.fade_out(fadeTime)
                pitchShifted_sound = pitchShifted_sound.fade_out(fadeTime)
                pitchShifted_sound = pitchShifted_sound.fade_out(fadeTime)
                pitchShifted_sound = pitchShifted_sound.fade_out(fadeTime)
            elif self.config.config['handbellSource'] == 'rebel':
                fadeTime = int(len(pitchShifted_sound)*0.95)
                pitchShifted_sound = pitchShifted_sound.fade_out(fadeTime)
                pitchShifted_sound = pitchShifted_sound.fade_out(fadeTime)
                pitchShifted_sound = pitchShifted_sound.fade_out(fadeTime)

            pitchShifted_sound.export(os.path.join('audio', '{}.wav'.format(self.numberOfBells - i)), format='wav')

        self.writeBellSpecFile()

    def loadBells(self):
        import os
        print("[INFO] Loading in bells")
        for i in range(self.numberOfBells):
            tmp = pygame.mixer.Sound(os.path.join('audio', '{}.wav'.format(i+1)))
            self.bells[i+1] = tmp
