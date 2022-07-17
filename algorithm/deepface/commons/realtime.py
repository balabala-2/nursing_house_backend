import os
import pandas as pd
import cv2
import time

import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

from algorithm.deepface import DeepFace
from algorithm.deepface.commons import functions, distance as dst
from algorithm.deepface.detectors import FaceDetector


def analysis(db_path, model_name = 'VGG-Face', detector_backend = 'opencv', enable_face_analysis = True, source = 0):

	#------------------------
	face_detector = FaceDetector.build_model(detector_backend)
	print("Detector backend is ", detector_backend)
	#------------------------

	input_shape = (224, 224)

	employees = []
	#check passed db folder exists
	if os.path.isdir(db_path) == True:
		for r, d, f in os.walk(db_path): # r=root, d=directories, f = files
			for file in f:
				if ('.jpg' in file):
					#exact_path = os.path.join(r, file)
					exact_path = r + "/" + file
					#print(exact_path)
					employees.append(exact_path)

	if len(employees) == 0:
		print("WARNING: There is no image in this path ( ", db_path,") . Face recognition will not be performed.")

	#------------------------

	if len(employees) > 0:

		model = DeepFace.build_model(model_name)
		print(model_name," is built")

		#------------------------

		input_shape = functions.find_input_shape(model)
		input_shape_x = input_shape[0]; input_shape_y = input_shape[1]

	#------------------------
	#facial attribute analysis models

	if enable_face_analysis == True:

		tic = time.time()
		emotion_model = DeepFace.build_model('Emotion')
		print("Emotion model loaded")
		toc = time.time()

		print("Facial attibute analysis models loaded in ",toc-tic," seconds")

	#find embeddings for employee list
	tic = time.time()

	pivot_img_size = 112 #face recognition result image

	freeze = False
	face_included_frames = 0 #freeze screen if face detected sequantially 5 frames

	cap = cv2.VideoCapture(source) #webcam

	while(True):
		ret, img = cap.read()
		
		if not ret:
			continue

		if img is None:
			break

		resolution_x = img.shape[1]

		if freeze == False:
			try:
				#faces store list of detected_face and region pair
				faces = FaceDetector.detect_faces(face_detector, detector_backend, img, align = False)
			except: #to avoid exception if no face detected
				faces = []

			if len(faces) == 0:
				face_included_frames = 0
		else:
			faces = []

		detected_faces = []
		face_index = 0
		for _, (x, y, w, h) in faces:
			if face_index == 0:
				face_included_frames = face_included_frames + 1 #increase frame for a single face

			cv2.rectangle(img, (x,y), (x+w,y+h), (67,67,67), 1) #draw rectangle to main image

			detected_face = img[int(y):int(y+h), int(x):int(x+w)] #crop detected face

			detected_faces.append((x,y,w,h))
			face_index = face_index + 1

		for detected_face in detected_faces:
			x = detected_face[0]; y = detected_face[1]
			w = detected_face[2]; h = detected_face[3]

			cv2.rectangle(img, (x,y), (x+w,y+h), (67,67,67), 1) #draw rectangle to main image

			#-------------------------------
			#apply deep learning for custom_face
			custom_face = img[y:y+h, x:x+w]
			#-------------------------------
			#facial attribute analysis

			if enable_face_analysis == True:

				gray_img = functions.preprocess_face(img = custom_face, target_size = (48, 48), grayscale = True, enforce_detection = False, detector_backend ='opencv')
				emotion_labels = ['Angry', 'Disgust', 'Fear', 'Happy', 'Sad', 'Surprise', 'Neutral']
				emotion_predictions = emotion_model.predict(gray_img, verbose=0)[0,:]
				sum_of_predictions = emotion_predictions.sum()

				mood_items = []
				for i in range(0, len(emotion_labels)):
					mood_item = []
					emotion_label = emotion_labels[i]
					emotion_prediction = 100 * emotion_predictions[i] / sum_of_predictions
					mood_item.append(emotion_label)
					mood_item.append(emotion_prediction)
					mood_items.append(mood_item)

				emotion_df = pd.DataFrame(mood_items, columns = ["emotion", "score"])
				emotion_df = emotion_df.sort_values(by = ["score"], ascending=False).reset_index(drop=True)


				#transparency
				overlay = img.copy()
				opacity = 0.4
				
				if x+w+pivot_img_size < resolution_x:
					#right
					cv2.rectangle(img, (x+w,y), (x+w+pivot_img_size, y+h), (64,64,64),cv2.FILLED)
					cv2.addWeighted(overlay, opacity, img, 1 - opacity, 0, img)

				elif x-pivot_img_size > 0:
					#left
					cv2.rectangle(img, (x-pivot_img_size,y), (x, y+h), (64,64,64),cv2.FILLED)
					cv2.addWeighted(overlay, opacity, img, 1 - opacity, 0, img)

				for index, instance in emotion_df.iterrows():
					emotion_label = "%s " % (instance['emotion'])
					emotion_score = instance['score']/100

					bar_x = 35 #this is the size if an emotion is 100%
					bar_x = int(bar_x * emotion_score)
					text_location_y = y + 20 + (index+1) * 20
					if x+w+pivot_img_size < resolution_x:
						text_location_x = x+w
						if text_location_y < y + h:
							cv2.putText(img, emotion_label, (text_location_x, text_location_y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
							cv2.rectangle(img, (x+w+70, y + 13 + (index+1) * 20), (x+w+70+bar_x, y + 13 + (index+1) * 20 + 5), (255,255,255), cv2.FILLED)

					elif x-pivot_img_size > 0:
						text_location_x = x-pivot_img_size
						if text_location_y <= y+h:
							cv2.putText(img, emotion_label, (text_location_x, text_location_y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

							cv2.rectangle(img, (x-pivot_img_size+70, y + 13 + (index+1) * 20), (x-pivot_img_size+70+bar_x, y + 13 + (index+1) * 20 + 5), (255,255,255), cv2.FILLED)
		cv2.imshow('img', img)

		if cv2.waitKey(1) & 0xFF == ord('q'): #press q to quit
			break

	#kill open cv things
	cap.release()
	cv2.destroyAllWindows()
