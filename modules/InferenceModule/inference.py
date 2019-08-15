# Copyright (c) Microsoft. All rights reserved.
# Licensed under the MIT license. See LICENSE file in the project root for
# full license information.

import numpy as np
import time

def run_onnx(frame, location, timestamp, sess):
	"""
	Detect objects in frame of your camera, and returns results.
	Uses TinyYolo from the onnxmodel zoo. Feel free to use your own model or choose another from https://github.com/onnx/models.
	"""
	input_name = sess.get_inputs()[0].name

	def softmax(x):
		return np.exp(x) / np.sum(np.exp(x), axis=0)

	def sigmoid(x):
		return 1/(1+np.exp(-x))

	start_time = time.time()
	pred = sess.run(None, {input_name: frame})
	pred = np.array(pred[0][0])
	print("INFERENCE TIME (PURE ONNXRUNTIME)", (time.time()-start_time)*1000,"ms")
	
	labels_file = open("labels.txt")
	labels = labels_file.read().split(",")

	outputstring = "" #FOR SENDING RESPONSE
	output = [timestamp, location] #FOR SAVING IN CSV

	post_start_time = time.time()
	
	tiny_yolo_cell_width = 13
	tiny_yolo_cell_height = 13
	num_boxes = 5
	tiny_yolo_classes = 20

	CONFIDENCE_THRESHOLD = 0.35

	# Goes through each of the 'cells' in tiny_yolo. Each cell is responsible for detecting 5 objects
	for bx in range (0, tiny_yolo_cell_width):
		for by in range (0, tiny_yolo_cell_height):
			# Iterate through each 'object'
			for bound in range (0, num_boxes):
				# extract x, y, width, height, and confidence
				channel = bound*25
				tx = pred[channel][by][bx]
				ty = pred[channel+1][by][bx]
				tw = pred[channel+2][by][bx]
				th = pred[channel+3][by][bx]
				tc = pred[channel+4][by][bx]

				# apply sigmoid function to get real x/y coordinates, shift by cell position (COMMENTED OUT TO SAVE TIME)
				#x = (float(bx) + sigmoid(tx))*32
				#y = (float(by) + sigmoid(ty))*32
				
				#Apply sigmoid to get confidence on a scale from 0 to 1
				confidence = sigmoid(tc)
				#Iterate through 20 classes and apply softmax to see which one has the highest confidence, which would be the class of the object
				class_out = pred[channel+5:channel+5+tiny_yolo_classes][bx][by]
				class_out = softmax(np.array(class_out))
				class_detected = np.argmax(class_out)
				display_confidence = class_out[class_detected]*confidence
				if display_confidence > CONFIDENCE_THRESHOLD:
					outputstring += " "+ labels[class_detected] + " confidence " + str(display_confidence)
					output.append([labels[class_detected], display_confidence])
	outputstring = location + " Results @"+ timestamp + " " + outputstring
	print("POST PROCESSING TIME", (time.time() - post_start_time)*1000,"ms")
	print("TOTAL INFERENCE TIME", (time.time() - start_time)*1000,"ms")
	return output, outputstring
