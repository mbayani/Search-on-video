from features import ImageFeatures
from searcher import Searcher
import cv2
import glob
import numpy as np
import os

class Search:
	def __init__(self, dataset_path, index_path, query_path, result_path):
		self.dataset_path = dataset_path
		self.index_path = index_path
		self.query_path = query_path
		self.result_path = result_path
		self.image_features = ImageFeatures((8, 12, 3))

	def performSearch(self):
		output = []
		query = cv2.imread(self.query_path)
		features = self.image_features.getFeatures(query)
		searcher = Searcher(self.index_path)
		results = searcher.search(features)
		for (score, resultID) in results:
			file_name = os.path.basename(resultID)
			result = cv2.imread(self.dataset_path + "/" + resultID)
			cv2.imwrite(self.result_path + "/" + resultID, result)
			output.append(self.result_path + "/" + resultID)
		return output
	
	def performKeypointsSearch(self):
		output = []
		matchOutput = []
		resultMatches = []
		query = cv2.imread(self.query_path)
		query_keypoints, query_descriptors = self.image_features.imageKeypoints(query)
		ImgFileNames = []
		matchesMatchedFileNames = []		

		#numberOfImages = len([name for name in os.listdir(self.dataset_path) if os.path.isfile(os.path.join(self.dataset_path, name))])
		matchImages = []

		for obj in os.scandir(self.dataset_path):
			imageFileName = obj.name
			print("imageFileName:%s"%imageFileName)
			imagePath = os.path.join(self.dataset_path, imageFileName)
			image = cv2.imread(imagePath)
			keypoints, descriptors = self.image_features.imageKeypoints(image)
			bf = cv2.BFMatcher(cv2.NORM_L1, crossCheck=True)
			matches = bf.match(descriptors,query_descriptors)
			matches = sorted(matches, key = lambda x:x.distance)
			img3 = cv2.drawMatches(image, keypoints, query, query_keypoints, matches[:50], query, flags=2)
			#imageFileName = imagePath[imagePath.rfind("/") + 1:]
			imageExt = imageFileName.split('.')[1]
			imageName = imageFileName.split('.')[0]
			imageId = imageName.split('frame')[1]
			resultMatch = (int(imageId), len(matches))
			resultMatches.append(resultMatch)
			matchImages.insert(int(imageId),img3)

		searcher = Searcher(self.index_path)
		results = searcher.searchKeypoints(resultMatches)
		for (score, resultID) in results:
			imgFileName = 'frame' + str(resultID) + '.jpg'
			imgMatchedFileName = 'frame' + str(resultID) + '_match.jpg'
			result = cv2.imread(self.dataset_path + "/" + imgFileName)
			cv2.imwrite(self.result_path + "/" + imgFileName, result)
			matchedImage = matchImages[resultID]
			cv2.imwrite(self.result_path + "/" + imgMatchedFileName, matchedImage)
			output.append(self.result_path + "/" + imgFileName)
			matchOutput.append(self.result_path + "/" + imgMatchedFileName)
		return output, matchOutput

	def performORBKeypointsSearch(self):
		output = []
		matchOutput = []
		resultMatches = []
		print("performORBKeypointsSearch:query_path:%s"%self.query_path)
		query_image = cv2.imread(self.query_path)
		query_keypoints, query_descriptors = self.image_features.orbKeypoints(query_image)
		ImgFileNames = []
		matchesMatchedFileNames = []		
		matchImages = []
		
		for obj in os.scandir(self.dataset_path):
			imageFileName = obj.name
			print(imageFileName)
			imagePath = os.path.join(self.dataset_path, imageFileName)
			image = cv2.imread(imagePath)
			keypoints, descriptors = self.image_features.orbKeypoints(image)
			bf = cv2.BFMatcher(cv2.NORM_L1, crossCheck=True)
			matches = bf.match(descriptors,query_descriptors)
			matches = sorted(matches, key = lambda x:x.distance)
			img3 = cv2.drawMatches(image, keypoints, query_image, query_keypoints, matches[:20], query_image, flags=2)
			imageExt = imageFileName.split('.')[1]
			imageName = imageFileName.split('.')[0]
			imageId = imageName.split('frame')[1]
			resultMatch = (int(imageId), len(matches))
			resultMatches.append(resultMatch)
			matchImages.insert(int(imageId),img3)

		searcher = Searcher(self.index_path)
		results = searcher.searchKeypoints(resultMatches, limit=10)
		for (score, resultID) in results:
			imgFileName = 'frame%s.jpg'%resultID
			imgMatchedFileName = 'orb_frame%s_match.jpg'%resultID
			result = cv2.imread(os.path.join(self.dataset_path, imgFileName))
			cv2.imwrite(os.path.join(self.result_path, 'orb_' + imgFileName), result)
			matchedImage = matchImages[resultID]
			cv2.imwrite(os.path.join(self.result_path, imgMatchedFileName), matchedImage)
			output.append(os.path.join(self.result_path, 'orb_' + imgFileName))
			matchOutput.append(os.path.join(self.result_path,imgMatchedFileName))
		return output, matchOutput
	
