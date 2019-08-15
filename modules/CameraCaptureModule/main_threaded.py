# Copyright (c) Microsoft. All rights reserved.
# Licensed under the MIT license. See LICENSE file in the project root for
# full license information.

# pylint: disable=E0611
import cv2
import sys
import numpy as np
import time
import argparse
import requests
from datetime import datetime
from pytz import timezone   
import json
import csv
import threading

# Endpoint to send frames for inferencing
url = 'http://inferencemodule:5000'

# If you would like to change the port, you will need to modify:
#	the url variable above (currently the code is using port 5000)
# 	main.py in InferenceModule
#	Dockerfile.arm64 in InferenceModule

# Set timezone for timestamping (Change if you are not in Pacific timezone)
TIME_ZONE = timezone('US/Pacific')


# Camera class wraps around VideoCApture and allows us to thread cameras for parallel processing
# and streamlining the buffer
class Camera:
	
	def __init__(self, idx):
		self.index = idx
		try:
			self.cap = cv2.VideoCapture(int(self.index))
			self.cap.set(38, 2)
		except Exception:
			self.cap = cv2.VideoCapture(self.index)
			self.cap.set(38, 2)
		
		self._camera_thread = threading.Thread(target=self.run_camera)
		self._camera_thread.start()
	
	def run_camera(self):
		while (True):
			self.ret, self.frame = self.cap.read()
			cv2.waitKey(5)
			_, enc = cv2.imencode('.jpg', self.frame)
			self.enc = enc.flatten().tolist()

	def get_frame(self):
		return self.frame
	
	def get_running(self):
		return self.ret

	def get_encode_list(self):
		return self.enc


def camera_capture():
	"""
	Captures camera feed and sends it to http server in InferenceModule.
    """
	
	cameras = []
	locations = []

	with open('camerainfo.csv', 'r') as camerafile:
		reader = csv.reader(camerafile)
		for row in reader:
			cameras.append(str(row[0]))
			locations.append(str(row[1]))
	
	# Initializes capture objects for each camera
	caps = [Camera(i) for i in cameras]

	#GIVE TIME FOR THREADS TO START (CRITICAL)
	time.sleep(5)

	try:
		start_time = time.time()
		while (True):
			cv2.waitKey(5)
			output = {'cameras' : ','.join(cameras), 'locations' : ','.join(locations)}
			if (time.time() - start_time) > 0.0:
				start_time = time.time()
				total_perf_time = time.time()
				
				#ITERATE AND GET FRAMES FROM EACH CAMERA
				process_time = time.time()
				for i, cap in enumerate(caps):
					location = locations[i]
					camera = cameras[i]
					ts = datetime.now(TIME_ZONE)
					timestring = ts.strftime("%Y-%m-%d %H:%M:%S")
					print(timestring)
					output[camera+":frame"] = cap.get_encode_list()
					output[camera+":location"] = location
					output[camera+':timestamp'] = timestring
				print("TIME TO PROCESS ALL FRAMES FOR", len(cameras), "CAMERAS:", time.time()-process_time, "ms")

				#SEND FRAMES/TIMESTAMPS/LOCATIONS FOR EACH CAMERA
				try: 
					headers = {'Content-Type': 'application/json'}
					response = requests.post(url, headers=headers, data=json.dumps(output))
					print(response.text)
					print("PERF TIME FOR", len(cameras),"IS", (time.time()-total_perf_time), "s")

				except Exception as e:
					print('EXCEPTION:', str(e))

	except KeyboardInterrupt:
		sys.exit(0)

if __name__ == '__main__':
	camera_capture()
