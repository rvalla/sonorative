import os
import time as tm
import numpy as np
import json as js
from PIL import Image as im
from scipy.io import wavfile as wf

class ColorsSound():
	"Blending images one on top of the other"

	def __init__(self, configpath):
		self.config = js.load(open(configpath))
		self.starttime = None
		self.outPath = None
		self.outFile = None
		self.mode = None
		self.imagedata = None
		self.imagesize = []
		self.audiosr = None
		self.audiolength = None
		self.audiodata = None
		ColorsSound.setConfig(self, self.config)
		print(self)
		ColorsSound.run(self)
		self.audiomax = ColorsSound.getMaxAmplitude(self.audiodata)
		ColorsSound.save(self.outPath, self.outFile, self.audiosr, self.audiodata, self.audiomax)
		print("-- time needed for extracting the mistery sound: " + \
				ColorsSound.getWorkingTime(self.starttime, tm.time()))

	def run(self):
		self.starttime = tm.time()
		if self.mode == "horizontal":
			ColorsSound.map(self.imagedata, self.audiodata, 0)
		elif self.mode == "vertical":
			ColorsSound.map(self.imagedata, self.audiodata, 1)
		elif self.mode == "both":
			ColorsSound.map(self.imagedata, self.audiodata, 2)
		else:
			print("-- I don't know what to do with this mode...", end="\n")

	def map(idata, adata, mode):
		print("-- mapping colors to amplitude...", end="\r")
		w = idata.shape[0]
		h = idata.shape[1]
		for x in range(w):
			for y in range(h):
				if mode == 0:
					s = x * h + y
					adata[s] +=  ColorsSound.getAmplitude(idata[x][y])
				elif mode == 1:
					s = x + y * w
					adata[s] -= ColorsSound.getAmplitude(idata[x][y])
				elif mode == 2:
					s = x * h + y
					adata[s] += ColorsSound.getAmplitude(idata[x][y])
					s = x + y * w
					adata[s] -= ColorsSound.getAmplitude(idata[x][y])
		print("-- audio data is ready!             ", end= "\n")

	def getAmplitude(pixeldata):
		if isinstance(pixeldata,np.ndarray):
			a = pixeldata[0] * 0.45 + pixeldata[1] * 0.32 + pixeldata[2] * 0.23
			a = a / 255
			return a
		elif isinstance(pixeldata,np.uint8):
			a = pixeldata / 255
			return a
		else:
			print("-- something strange happens with pixel's data...")
			return 0

	def getMaxAmplitude(adata):
		return np.amax(np.absolute(adata))

	def save(filepath, filename, sr, adata, maxamp):
		adata = adata / maxamp
		wf.write(filepath + filename + ".wav", sr, adata)
		print("-- output audio file saved!", end="\n")

	def setConfig(self, data):
		self.mode = data["mode"]
		self.outPath = data["outPath"]
		self.outFile = data["outFile"]
		self.imagedata = np.array(im.open(data["inPath"] + data["inFile"]))
		self.imagesize.append(self.imagedata.shape[0])
		self.imagesize.append(self.imagedata.shape[1])
		self.audiosr = data["sampleRate"]
		self.audiolength = ColorsSound.getAudioLength(self.imagesize)
		self.audiodata = np.zeros((self.audiolength), dtype="float32")
		self.startTime = tm.time()

	def getAudioLength(isize):
		n = 1
		for f in range(len(isize)):
			n = n * isize[f]
		return n

	#Calculating time needed for processing an image...
	def getWorkingTime(start, end):
		time = end - start
		formatedTime = ColorsSound.formatTime(time)
		return formatedTime

	def formatTime(time):
		ms = ""
		minutes = time // 60
		seconds = time - minutes * 60
		seconds = round(seconds, 2)
		ms = "{:02d}".format(int(minutes))
		ms += ":"
		ms += "{:05.2f}".format(seconds)
		return ms

	def __str__(self):
		return "-- sonorative --\n" + \
				"-- ColorsSound\n" + \
				"-- https://gitlab.com/azarte/sonorative\n" + \
				"-- version: 0.50\n" + \
				"-- Listening to image's sounds..."
