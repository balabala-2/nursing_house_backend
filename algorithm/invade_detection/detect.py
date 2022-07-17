'''
禁止区域检测
'''

import numpy as np
import datetime
import dlib
import cv2
from fastapi.responses import StreamingResponse

from algorithm.utils.global_variable import invade_weights, video_height, video_width, invade_detection_url
from algorithm.invade_detection.track import CentroidTracker
from algorithm.invade_detection.track import TrackableObject

from dao.scene_operation import add_invade
from schemas.other import Invade_info

class Invade_detect():
	# 物体识别模型能识别的物体（21种）
	CLASSES = ["background", "aeroplane", "bicycle", "bird", "boat",
			"bottle", "bus", "car", "cat", "chair", 
			"cow", "diningtable","dog", "horse", "motorbike", 
			"person", "pottedplant", "sheep","sofa", "train", 
			"tvmonitor"]
	# 超参数 minimum probability to filter weak detections
	minimum_confidence = 0.80 
	# of skip frames between detections
	skip_frames = 30 
	# 加载物体识别模型
	net = cv2.dnn.readNetFromCaffe(invade_weights['prototxt'], invade_weights['model'])
	centroidTracker = CentroidTracker(maxDisappeared=40, maxDistance=50)

	def __init__(self) -> None:
		stream = cv2.VideoCapture(invade_detection_url)
		stream.set(3, video_width)
		stream.set(4, video_height)

		# # initialize the frame dimensions
		self.W = video_width
		self.H = video_height
		self.stream = stream
		self.trackers = []
		self.trackableObjects = {}

		self.totalFrames = 0
		self.totalDown = 0
		self.totalUp = 0

	def run(self):
		ret = True
		while ret:
			ret, frame = self.stream.read()
			frame = cv2.flip(frame, 1)
			frame = cv2.resize(frame, (self.W, self.H))
			rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

			rects = []

			if self.totalFrames % self.skip_frames == 0:
				# set the status and initialize our new set of object trackers
				trackers = []

				blob = cv2.dnn.blobFromImage(frame, 0.007843, (self.W, self.H), 127.5)
				self.net.setInput(blob)
				detections = self.net.forward()
				for i in np.arange(0, detections.shape[2]):
					confidence = detections[0, 0, i, 2]
					if confidence > self.minimum_confidence:
						idx = int(detections[0, 0, i, 1])

						if self.CLASSES[idx] != "person":
							continue

						# compute the (x, y)-coordinates of the bounding box
						# for the object
						box = detections[0, 0, i, 3:7]*np.array([self.W, self.H, self.W, self.H])
						(startX, startY, endX, endY) = box.astype("int")
						
						# construct a dlib rectangle object from the bounding
						# box coordinates and then start the dlib correlation
						# tracker
						tracker = dlib.correlation_tracker()
						rect = dlib.rectangle(startX, startY, endX, endY)
						tracker.start_track(rgb, rect)

						# add the tracker to our list of trackers so we can
						# utilize it during skip frames
						trackers.append(tracker)
			else:
				# loop over the trackers
				for tracker in trackers:
					# than 'waiting' or 'detecting'

					# update the tracker and grab the updated position
					tracker.update(rgb)
					pos = tracker.get_position()

					# unpack the position object
					startX, startY, endX, endY = int(pos.left()), int(pos.top()), int(pos.right()), int(pos.bottom())

					# draw a rectangle around the people
					cv2.rectangle(frame, (startX, startY), (endX, endY),
						(0, 255, 0), 2)

					# add the bounding box coordinates to the rectangles list
					rects.append((startX, startY, endX, endY))

			cv2.line(frame, (0, self.H // 2), (self.W, self.H // 2), (0, 255, 255), 2)

			objects = self.centroidTracker.update(rects)

			# loop over the tracked objects
			for (objectID, centroid) in objects.items():
				# check to see if a trackable object exists for the current
				# object ID
				to = self.trackableObjects.get(objectID, None)

				# if there is no existing trackable object, create one
				if to is None:
					to = TrackableObject(objectID, centroid)

				# otherwise, there is a trackable object so we can utilize it
				# to determine direction
				else:
					y = [c[1] for c in to.centroids]
					direction = centroid[1] - np.mean(y)
					to.centroids.append(centroid)

					# check to see if the object has been counted or not
					if not to.counted:
						# if the direction is negative (indicating the object
						# is moving up) AND the centroid is above the center
						# line, count the object
						if direction < 0 and centroid[1] < self.H // 2:
							self.totalUp += 1
							to.counted = True

						# if the direction is positive (indicating the object
						# is moving down) AND the centroid is below the
						# center line, count the object
						# 有人闯入
						elif direction > 0 and centroid[1] > self.H // 2:
							self.totalDown += 1
							to.counted = True
							add_invade(Invade_info(img=cv2.imencode('.jpg', frame)[1].tobytes()))
				
				# store the trackable object in our dictionary
				self.trackableObjects[objectID] = to

			yield cv2.imencode('.jpg', frame)[1].tobytes()
			cv2.waitKey(1)
			self.totalFrames += 1

		self.stream.release()
		cv2.destroyAllWindows()

	def generate_frame(self):
		"""Video streaming generator function."""
		frames = self.run()
		try:
			while True:
				frame = frames.__next__()
				if frame is not None:
					yield (b'--frame\r\n'
					b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
				else:
					break
		except Exception:
			pass

	def video_generate(self):
		if self.stream.isOpened():
			return StreamingResponse(self.generate_frame(),
									media_type='multipart/x-mixed-replace; boundary=frame')
		else:
			def file():
				with open('resources/video_not_open.jpg', mode='rb') as f:
					yield from f
			return StreamingResponse(file(), media_type='image/jpg')
