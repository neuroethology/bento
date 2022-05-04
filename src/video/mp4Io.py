import cv2
import numpy as np
import os
from qtpy.QtGui import QImage, QPixmap

class mp4Io_reader():
	def __init__(self, filename, info=[]):
		self.filename = filename
		self.file = cv2.VideoCapture(filename)

		if self.file.isOpened()==False:
			print("Error in opening video file.")

		self.header={}
		if info==[]:
			self.readHeader()

	def readHeader(self):

		self.header = {
			'width': int(self.file.get(cv2.CAP_PROP_FRAME_WIDTH)),
			'height': int(self.file.get(cv2.CAP_PROP_FRAME_HEIGHT)),
			'fps': self.file.get(cv2.CAP_PROP_FPS),
			'numFrames': int(self.file.get(cv2.CAP_PROP_FRAME_COUNT))
		}

	def seek(self, index):

		self.file.set(cv2.CAP_PROP_POS_FRAMES, index)

	def getTs(self,n=None):
		if n==None:
			n = self.header['numFrames']

		ts = np.zeros(n+1)
		for i in np.arange(1,n+1):
			self.seek(i)
			self.file.read()
			ts[i] = self.file.get(cv2.CAP_PROP_POS_MSEC)/1000.

		self.ts = ts[1:]
		return self.ts

	def getFrame(self, index, decode=True):

		self.seek(index)
		ret, frame = self.file.read()

		ts = self.file.get(cv2.CAP_PROP_POS_MSEC)/1000.
		return frame, ts

	def getFrameAsQPixmap(self, index, decode=True):
		image, _ = self.getFrame(index, decode)
		h, w, ch = image.shape
		bytes_per_line = ch * w
		convert_to_Qt_format = QImage(image.data, w, h, bytes_per_line, QImage.Format_BGR888)
		return QPixmap.fromImage(convert_to_Qt_format)

	def close(self):
		self.file.release()

