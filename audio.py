import wave

from pydub import AudioSegment

import pygame

import numpy as np

class Audio:
    def __init__(self, numberOfBells, mixer, inputFileName="audio/handbell.wav"):
        self.inputFileName = inputFileName

        self.numberOfBells = numberOfBells
        self.mixer = mixer

        self.bellSemitones = []
        self.bells = {}
        # Major scale formula: W W H W W W H
        self.majorScale = [0, 2, 4, 5, 7, 9, 11, 12]
        self.generateBells()

        self.loadBells()

    def generateBells(self):

        self.bellSemitones = [0]
        j = 0
        for j in range(int(self.numberOfBells/8)):
            self.bellSemitones.append(self.majorScale[1]+j*12)
            for i in range(2, 8):
                if j*8 + i < self.numberOfBells:
                    self.bellSemitones.append(self.majorScale[i]+j*12)
        for i in range(8):
            if len(self.bellSemitones) < self.numberOfBells:
                self.bellSemitones.append(self.majorScale[i+1]+(j)*12)

        sound = AudioSegment.from_file(self.inputFileName, format="wav")
        sound = sound.fade_out(int(len(sound)*0.5))

        for i, semitones in enumerate(self.bellSemitones):
            octave = 12
            new_sample_rate = int(sound.frame_rate * (2.0 ** (semitones/octave)))
            pitchShifted_sound = sound._spawn(sound.raw_data, overrides={'frame_rate': new_sample_rate})

            fadeTime = int(len(pitchShifted_sound)*0.5)
            pitchShifted_sound = pitchShifted_sound.fade_out(fadeTime)

            pitchShifted_sound = pitchShifted_sound.set_frame_rate(11000)

            pitchShifted_sound.export('audio/{}.wav'.format(self.numberOfBells - i), format='wav')

    def loadBells(self):
        import os
        cwd = os.getcwd()
        print(cwd)
        for i in range(self.numberOfBells):
            tmp = pygame.mixer.Sound('audio/{}.wav'.format(i+1))
            self.bells[i+1] = tmp
