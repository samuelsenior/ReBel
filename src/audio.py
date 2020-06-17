from pydub import AudioSegment
import os
import sys
import csv

import threading, queue
import time

from error import Error

import pygame

class Audio(Error):
    '''
    The Audio object takes the number of handbells and their tuning from the
    current ReBel configuration and compares them to the bell spec file of the
    previously generated bells, if it exists. If the two sets of parameters
    match then the previously generated handbells sounds are read in and if
    they do not match or the bell spec file doesn't exist then the bell sounds
    are generated from the ReBel configuration using the provided handbell
    tenor sound and pitch shifting.

    Four different scales are provided that the handbells can be tuned to:
    major, natural minor, harmonic minor, and melodic minor. The bells can also
    be shifted in pitch by user specified number of octaves and semitones.

    Parameters
    ----------
    numberOfBells : int
        The total number of bells being rung.

    config : Config
        The ReBel config instance.

    logFile : string
        The name and location of the log file to write to.
    '''
    def __init__(self, numberOfBells, config, logger):
        # Set the working directory based on if ReBel is being run from an
        # executable or the Python source code.
        if getattr(sys, 'frozen', False):
            # In a bundle
            self.exeDir = os.path.dirname(sys.executable)
        else:
            # In normal python
            self.exeDir = ""
        # Set the logger
        self.logger = logger
        # Initialise the inherited Error instance.
        Error.__init__(self)

        self.numberOfBells = numberOfBells
        self.config = config
        #self.mixer = mixer

        self.bellSemitones = []
        self.bells = {}

        # Define the semistone steps between the notes of the different
        # available scales. In the comments below t = tone and s = semitone.
        # Major scale formula: t t s t t t s
        self.majorScale = [0, 2, 4, 5, 7, 9, 11, 12]
        # Natural minor scale: t s t t s t t
        self.naturalMinorScale = [0, 2, 3, 5, 7, 8, 10, 12]
        # Harmonic minor scale: t s t t 1.5t s
        self.harmonicMinorScale = [0, 2, 3, 5, 7, 8, 11, 12]
        # Melodic minor scale: t s t t t t s
        self.melodicMinorScale = [0, 2, 3, 5, 7, 9, 11, 12]
        # Set the scale being used to that given in the config.
        if self.config.get('scale') == "major":
            self.scale = self.majorScale
        elif self.config.get('scale') == "naturalMinor":
            self.scale = self.naturalMinorScale
        elif self.config.get('scale') == "harmonicMinor":
            self.scale = self.harmonicMinorScale
        elif self.config.get('scale') == "melodicMinor":
            self.scale = self.melodicMinorScale

        # Check if the bell sounds already exist and match the given number of
        # bells and tuning, if they don't exist or match then generate them.
        self.regenerateBells = True
        self.checkGeneratedBells()
        if self.regenerateBells == True:
            self.generateBells()
        if self.config.get('regenerateBells') == True:
            self.log("[INFO] Config regenerate bells option is True")
            self.generateBells()

        # Load in the bell sounds.
        #self.loadBells()

        self.frameRate = 500
        self.running = True
        self.playBellQueue = queue.Queue()
        self.playBellThread = threading.Thread(target=self.playBell, args=(), daemon=True)
        self.playBellThread.start()

    def log(self, *args):
        '''
        Wrapper function to the logger.log function.

        Parameters
        ----------
        args
            The arguments to pass into the logger.log function.
        '''
        self.logger.log(*args)

    def checkGeneratedBells(self):
        '''
        Check whether the bell spec file exists and if it does then check that
        the parameters of the number of bells and their tunings as given in the
        ReBel config match those in the bell spec file.
        '''
        # Parameter for check as to whether the bells match or not and so need
        # to be read in or not.
        self.regenerateBells = True
        # Define the file location of the bell spec file.
        self.bellSpecFileLocation = os.path.join(self.exeDir, "..", "audio", "bsf")
        # Check bell spec file exists.
        if os.path.isfile(self.bellSpecFileLocation):
            bellSpec = {}
            # Read in bell spec file and temporarily save parameters.
            with open(self.bellSpecFileLocation, 'r') as bellSpecFile:
                bellSpecFile_reader = csv.reader(bellSpecFile, delimiter=":")
                for bellSpecLine in bellSpecFile_reader:
                    bellSpec[bellSpecLine[0]] = bellSpecLine[1]
            bellSpec['scale'] = bellSpec['scale'].split(",")
            bellSpec['scale'] = [int(b) for b in bellSpec['scale']]
            bellSpec['numberOfBells'] = int(bellSpec['numberOfBells'])
            bellSpec['octaveShift'] = int(bellSpec['octaveShift'])
            bellSpec['semitoneShift'] = int(bellSpec['semitoneShift'])

            # Compare the bell spec file parameters to the ReBel config
            # parameters.
            if bellSpec['scaleName'] == self.config.get('scale') \
               and bellSpec['scale'] == self.scale \
               and bellSpec['numberOfBells'] == self.config.get('numberOfBells') \
               and bellSpec['octaveShift'] == self.config.get('octaveShift') \
               and bellSpec['semitoneShift'] == self.config.get('semitoneShift') \
               and bellSpec['handbellSource'] == self.config.get('handbellSource'):
                # If all the parameters match then the bells do not need to be
                # generated/regenerated.
                self.regenerateBells = False
                self.log("[INFO] Config file bell options match bell spec file")
            else:
                self.log("[INFO] Config file bell options do not match bell spec file, regenerating bells")

    def writeBellSpecFile(self):
        '''
        Write the current number of bells and bell tunings as given in the
        ReBel config to the bell spec file.
        '''
        self.log("[INFO] Writing bell spec file")
        # Define the location of the bell spec file.
        self.bellSpecFileLocation = os.path.join(self.exeDir, "..", "audio", "bsf")
        # Open the file and write the bell parameters of the ReBel config to it.
        with open(self.bellSpecFileLocation, 'w') as bellSpecFile:
            bellSpecFile.write("{}:{}\n".format("scaleName", self.config.get('scale')))
            bellSpecFile.write("{}:".format("scale"))
            for i, _ in enumerate(self.scale):
                if i > 0:
                    bellSpecFile.write(",")
                bellSpecFile.write("{}".format(self.scale[i]))
            bellSpecFile.write("\n")
            bellSpecFile.write("{}:{}\n".format("numberOfBells", self.config.get('numberOfBells')))
            bellSpecFile.write("{}:{}\n".format("octaveShift", self.config.get('octaveShift')))
            bellSpecFile.write("{}:{}\n".format("semitoneShift", self.config.get('semitoneShift')))
            bellSpecFile.write("{}:{}\n".format("handbellSource", self.config.get('handbellSource')))

    def generateBells(self):
        '''
        Generate the bell sounds using the source handbell tenor sound, pitch
        shifting, and the bell parameters of the ReBel config.
        '''
        self.log("[INFO] Generating bells")

        # Starting note is always the root note of the scale and so is zero
        # semitone steps away from the root note.
        self.bellSemitones = [0]

        # Append the bell semitone list with the number of semitones between
        # the current note of the scale and the root note, doing this until
        # the bell semitone list has a length equal to the total number of
        # bells being rung.
        # The for loop sets the note semitones for bells in whole octaves.
        j = 0
        for j in range(int(self.numberOfBells/8)):
            self.bellSemitones.append(self.scale[1]+j*12)
            for i in range(2, 8):
                if j*8 + i < self.numberOfBells:
                    self.bellSemitones.append(self.scale[i]+j*12)
        # If the total number of bells is less than one octave then fill the
        # semitone list up to that partial octave. Else if the total number of
        # bells lies between two whole octaves then append the semitone list
        # with that remaining partial octave.
        if self.numberOfBells < 8:
            for i in range(self.numberOfBells):
                if len(self.bellSemitones) < self.numberOfBells:
                    self.bellSemitones.append(self.scale[i+1])
        else:
            for i in range(8):
                if len(self.bellSemitones) < self.numberOfBells:
                    self.bellSemitones.append(self.scale[i+1]+(j+1)*12)

        # Try to read in the tenor handbell sound from the handbell source
        # location. If the handbell source does not exist then try the default
        # ReBel handbell source location. If that does not exist too then throw
        # an error and quit ReBel.
        if self.config.get('handbellSource') == 'abel':
            try:
                sound = AudioSegment.from_file(self.config.get('abelBellFileLocation'), format="wav")
            except:
                self.log("[WARNING] Abel handbell source file not found, defaulting to ReBel handbell source file")
                try:
                    sound = AudioSegment.from_file(self.config.get('rebelBellFileLocation'), format="wav")
                except:
                    self.log("ReBel handbell source file not found, terminating program...", False)
                    self.error("ReBel handbell source file not found, terminating program...", 1)
        elif self.config.get('handbellSource') == 'rebel':
            try:
                sound = AudioSegment.from_file(self.config.get('rebelBellFileLocation'), format="wav")
            except:
                self.log("ReBel handbell source file not found, terminating program...", False)
                self.error("ReBel handbell source file not found, terminating program...", 1)
        else:
            self.log("[WARNING] Handbell source not set, defaulting to ReBel handbell source file")
            try:
                sound = AudioSegment.from_file(self.config.get('rebelBellFileLocation'), format="wav")
            except:
                self.log("ReBel handbell source file not found, terminating program...", False)
                self.error("ReBel handbell source file not found, terminating program...", 1)

        # Apply high and low spectral filters to the tenor handbell sound to
        # improve the sound quality of the bell sounds generated through the
        # pitch shifting. Cutoff frequencies have been determined by through
        # inspecting the tenor handbell sounds via spectrograms.
        if self.config.get('handbellSource') == 'abel':
            sound = sound.high_pass_filter(cutoff=500)
            sound = sound.high_pass_filter(cutoff=500)
            sound = sound.high_pass_filter(cutoff=500)
        elif self.config.get('handbellSource') == 'rebel':
            sound = sound.high_pass_filter(cutoff=400)
            sound = sound.high_pass_filter(cutoff=400)
            sound = sound.high_pass_filter(cutoff=400)

            sound = sound.low_pass_filter(cutoff=7750)
            sound = sound.low_pass_filter(cutoff=7750)
            sound = sound.low_pass_filter(cutoff=7750)

        # Generate the handbell sounds via pitch shifting done by changing
        # sampling rates, with the equation to determine the new sampling being
        # newSamplingRate = oldSamplingRate * 2 ^ (O + (S + s) / 12).
        # Here O is the number of octaves to shift by, S is the number of
        # semitones to shift by and s is the semitone difference between the
        # desired note and the root note of the scale, 12 being the number of
        # semitones in an octave and converts the semitones to partial octaves.
        # Simply copy the tenor handbell sound whilst overriding the original
        # sampling rate with the new one to change the pitch to the desired
        # note.
        for i, semitone in enumerate(self.bellSemitones):
            octave = 12
            new_sample_rate = int(sound.frame_rate * (2.0 ** (self.config.get('octaveShift') + (self.config.get('semitoneShift')+semitone)/octave)))
            pitchShifted_sound = sound._spawn(sound.raw_data, overrides={'frame_rate': new_sample_rate})

            # The pitch shifting via changing sampling rate inherently changes
            # the frame rate of the sound, therefore set all the bell sounds to
            # the same frame rate, here chosen to be 44100 Hz.
            pitchShifted_sound = pitchShifted_sound.set_frame_rate(44100)

            # Apply fade outs to the bell sounds so that they don't ring on for
            # too long.
            if self.config.get('handbellSource') == 'abel':
                fadeTime = int(len(pitchShifted_sound)*0.95)
                pitchShifted_sound = pitchShifted_sound.fade_out(fadeTime)
                pitchShifted_sound = pitchShifted_sound.fade_out(fadeTime)
                pitchShifted_sound = pitchShifted_sound.fade_out(fadeTime)
                pitchShifted_sound = pitchShifted_sound.fade_out(fadeTime)
            elif self.config.get('handbellSource') == 'rebel':
                fadeTime = int(len(pitchShifted_sound)*0.95)
                #pitchShifted_sound = pitchShifted_sound.fade_out(fadeTime)
                #pitchShifted_sound = pitchShifted_sound.fade_out(fadeTime)
                #pitchShifted_sound = pitchShifted_sound.fade_out(fadeTime)

            # Save the generated bell sound, with the file name being equal to
            # the bell number.
            pitchShifted_sound.export(os.path.join(self.exeDir, "..", "audio", "{}.wav".format(self.numberOfBells - i)), format='wav')

        # Write the new bell spec file.
        self.writeBellSpecFile()

    def loadBells(self):
        '''
        Read in the bell sounds and save them to an internal Audio variable.
        '''
        self.log("[INFO] Loading in bells")
        # Read in the bell sounds using the convention that the file names
        # equal the bell numbers.
        for i in range(self.numberOfBells):
            self.bells[i+1] = self.mixer.Sound(os.path.join(self.exeDir, "..", "audio", "{}.wav".format(i+1)))

    def playBell(self):

        self.mixer = pygame.mixer
        self.mixer.set_num_channels(self.config.get('numberOfBells'))

        self.loadBells()

        while self.running:
            start = time.time()
            try:
                bellNumber = self.playBellQueue.get_nowait()
            except:
                pass
            else:
                self.mixer.Channel(bellNumber-1).play(self.bells[bellNumber])
            time.sleep(max(1./self.frameRate - (time.time() - start), 0))

    def play(self, bellNumber):
        self.playBellQueue.put(bellNumber)
