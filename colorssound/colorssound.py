import math
import time as tm
import numpy as np
import json as js
from PIL import Image as im
from scipy.io import wavfile as wf

class ColorsSound():
	"Creating sound from the colors in an image"

	def __init__(self, configpath):
		self.config = js.load(open(configpath))
		self.start_time = None
		self.out_path = None
		self.out_file = None
		self.mode = None
		self.direction = None
		self.imagedata = None
		self.imagesize = []
		self.audiosr = None
		self.audiolength = None
		self.audiodata = None
		self.frequency_factor = None
		self.partials = None
		self.set_config(self.config)
		print(self)
		if self.mode == "amplitude":
			self.run_amp()
		elif self.mode == "frequency":
			self.run_freq()
		elif self.mode == "spectral":
			self.run_spectral()
		self.audiomax = self.max_amplitude(self.audiodata)
		self.save(self.out_path, self.out_file, self.audiosr, self.audiodata, self.audiomax)
		print("-- time needed for extracting the mistery sound: " + \
				self.working_time(self.start_time, tm.time()))

	#Running in amplitude mode...
	def run_amp(self):
		self.start_time = tm.time()
		if self.direction == "horizontal":
			self.map_amplitude(self.imagedata, self.audiodata, 0)
		elif self.direction == "vertical":
			self.map_amplitude(self.imagedata, self.audiodata, 1)
		elif self.direction == "both":
			self.map_amplitude(self.imagedata, self.audiodata, 2)
		else:
			print("-- I don't know what to do with this mode...", end="\n")

	#Running in frequency mode...
	def run_freq(self):
		self.start_time = tm.time()
		if self.direction == "horizontal":
			self.map_frequency(self.imagedata, self.audiodata, 0)
		elif self.direction == "vertical":
			self.map_frequency(self.imagedata, self.audiodata, 1)
		elif self.direction == "both":
			self.map_frequency(self.imagedata, self.audiodata, 2)
		else:
			print("-- I don't know what to do with this mode...", end="\n")
	
	#Running spectral mode...
	def run_spectral(self):
		pass
		self.start_time = tm.time()
		if self.direction == "horizontal":
			self.map_spectrum(self.imagedata, self.audiodata, self.partials, 0)
		elif self.direction == "vertical":
			self.map_spectrum(self.imagedata, self.audiodata, self.partials, 1)
		elif self.direction == "both":
			self.map_spectrum(self.imagedata, self.audiodata, self.partials, 2)
		else:
			print("-- I don't know what to do with this mode...", end="\n")

	#Deciding amplitude for each sample based in pixel color...
	def map_amplitude(self, idata, adata, mode):
		print("-- mapping colors to amplitude...", end="\r")
		w = idata.shape[0]
		h = idata.shape[1]
		for x in range(w):
			for y in range(h):
				if mode == 0:
					s = x * h + y
					adata[s] +=  self.get_amplitude(idata[x][y])
				elif mode == 1:
					s = x + y * w
					adata[s] += self.get_amplitude(idata[x][y])
				elif mode == 2:
					s = x * h + y
					adata[s] += self.get_amplitude(idata[x][y])
					s = x + y * w
					adata[s] -= self.get_amplitude(idata[x][y])
		print("-- audio data is ready!             ", end= "\n")

	def get_amplitude(self, pixeldata):
		if isinstance(pixeldata,np.ndarray):
			a = -255 + 2 * (pixeldata[0] * 0.45 + pixeldata[1] * 0.32 + pixeldata[2] * 0.23)
			return a
		elif isinstance(pixeldata,np.uint8):
			a = -255 + 2 * pixeldata
			return a
		else:
			print("-- something strange happens with pixel's data...")
			return 0

	#Getting amplidute for sample using color value as frequency input...
	def map_frequency(self, idata, adata, mode):
		print("-- mapping colors to amplitude...", end="\r")
		w = idata.shape[0]
		h = idata.shape[1]
		step_w = 2 * math.pi / (w * self.frequency_factor)
		step_h = 2 * math.pi / (h * self.frequency_factor)
		for x in range(w):
			for y in range(h):
				if mode == 0:
					s = x * h + y
					adata[s] +=  self.get_freq_amplitude(s, step_w, idata[x][y])
				elif mode == 1:
					s = x + y * w
					adata[s] += self.get_freq_amplitude(s, step_h, idata[x][y])
				elif mode == 2:
					s = x * h + y
					adata[s] += self.get_freq_amplitude(s, step_w, idata[x][y])
					s = x + y * w
					adata[s] -= self.get_freq_amplitude(s, step_h, idata[x][y])
		print("-- audio data is ready!             ", end= "\n")

	def get_freq_amplitude(self, sample, step, pixeldata):
		angle = sample * step
		if isinstance(pixeldata,np.ndarray):
			a = math.sin(pixeldata[0] * angle) * 0.45 + math.sin(pixeldata[1] * angle) * 0.32 + math.sin(pixeldata[2] * angle) * 0.23
			return a
		elif isinstance(pixeldata,np.uint8):
			a = math.sin(pixeldata * angle)
			return a
		else:
			print("-- something strange happens with pixel's data...")
			return 0
	
	#Getting amplitude for each sample based giving each partial its amplitude from pixel data...
	def map_spectrum(self, idata, adata, partials, mode):
		print("-- mapping colors to amplitude...", end="\r")
		w = idata.shape[0]
		h = idata.shape[1]
		step_w = 2 * math.pi / (w * self.frequency_factor)
		step_h = 2 * math.pi / (h * self.frequency_factor)
		for x in range(w):
			for y in range(h):
				if mode == 0:
					s = x * h + y
					adata[s] +=  self.get_spec_amplitude(s, step_w, partials, idata[x][y])
				elif mode == 1:
					s = x + y * w
					adata[s] += self.get_spec_amplitude(s, step_h, partials, idata[x][y])
				elif mode == 2:
					s = x * h + y
					adata[s] += self.get_spec_amplitude(s, step_w, partials, idata[x][y])
					s = x + y * w
					adata[s] -= self.get_spec_amplitude(s, step_h, partials, idata[x][y])
		print("-- audio data is ready!             ", end= "\n")
	
	def get_spec_amplitude(self, sample, step, partials, pixeldata):
		angle = sample * step
		if isinstance(pixeldata,np.ndarray):
			a = math.sin(partials[0] * angle) * pixeldata[0] * 0.45
			a += math.sin(partials[1] * angle) * pixeldata[1] * 0.32
			a += math.sin(partials[2] * angle) * pixeldata[2] * 0.23
			return a
		elif isinstance(pixeldata,np.uint8):
			a = math.sin(partials[0] * angle) * pixeldata
			return a
		else:
			print("-- something strange happens with pixel's data...")
			return 0

	#Getting the maximum amplitude in adata...
	def max_amplitude(self, adata):
		return np.amax(np.absolute(adata))

	#Saving our work to an audio file...
	def save(self, filepath, filename, sr, adata, maxamp):
		adata = adata / maxamp
		wf.write(filepath + filename + ".wav", sr, adata)
		print("-- output audio file saved!", end="\n")

	#Loading configuration data from configuration file...
	def set_config(self, data):
		self.mode = data["mode"]
		self.direction = data["direction"]
		self.out_path = data["outPath"]
		self.out_file = data["outFile"]
		self.imagedata = np.array(im.open(data["inPath"] + data["inFile"]))
		self.imagesize.append(self.imagedata.shape[0])
		self.imagesize.append(self.imagedata.shape[1])
		self.audiosr = data["sampleRate"]
		self.audiolength = self.get_audio_length(self.imagesize)
		self.audiodata = np.zeros((self.audiolength), dtype="float32")
		self.frequency_factor = data["fModeFactor"]
		self.partials = self.get_partials(data["partials"])
		self.start_time = tm.time()
	
	#Loading partials frequency from configuration file...
	def get_partials(self, data):
		return [int(a) for a in data.split(",")]

	#Getting the total number of audio samples...
	def get_audio_length(self, isize):
		n = 1
		for f in range(len(isize)):
			n = n * isize[f]
		return n

	#Calculating time needed for processing an image...
	def working_time(self, start, end):
		time = end - start
		formated_time = self.formatTime(time)
		return formated_time
	
	def formatTime(self, time):
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
