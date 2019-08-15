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

# Endpoint to send frames for inferencing
url = 'http://inferencemodule:5000'

# If you would like to change the port, you will need to modify:
#	the url variable above (currently the code is using port 5000)
# 	main.py in InferenceModule
#	Dockerfile.arm64 in InferenceModule

# Set timezone for timestamping (Change if you are not in Pacific timezone)
TIME_ZONE = timezone('US/Pacific')

# Set delay so you don't have too many messages (in seconds)
DELAY = 0.0

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
	caps = []
	for i in cameras:
		try:
			cap = cv2.VideoCapture(int(i))	
		except Exception:
			cap = cv2.VideoCapture(i)
		cap.set(38, 2)
		caps.append(cap)

	try:
		start_time = time.time()
		while (True):
			cv2.waitKey(5)
			output = {'cameras' : ','.join(cameras), 'locations' : ','.join(locations)}
			if (time.time() - start_time) > DELAY:
				start_time = time.time()
				total_perf_time = time.time()
				#ITERATE AND GET FRAMES FROM EACH CAMERA
				for i, cap in enumerate(caps):
					location = locations[i]
					camera = cameras[i]
					ret, frame = cap.read()
					ts = datetime.now(TIME_ZONE)
					timestring = ts.strftime("%Y-%m-%d %H:%M:%S")
					print(timestring)
					ret, enc = cv2.imencode('.jpg', frame)
					enc = enc.flatten()
					output[camera+":frame"] = enc.tolist()
					output[camera+":location"] = location
					output[camera+':timestamp'] = timestring

				#SEND FRAMES/TIMESTAMPS/LOCATIONS FOR EACH CAMERA
				try: 
					headers = {'Content-Type': 'application/json'}
					response = requests.post(url, headers=headers, data=json.dumps(output))
					print(response.text)
					print("PERF TIME FOR", len(cameras),"IS", (time.time()-total_perf_time), "s")

				except Exception as e:
					print('EXCEPTION:', str(e))
					print("there was an exception")

	except KeyboardInterrupt:
		sys.exit(0)

if __name__ == '__main__':
	camera_capture()
