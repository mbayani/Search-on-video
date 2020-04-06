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

		for imagePath in glob.glob(self.dataset_path + "/*.*"):			
			image = cv2.imread(imagePath)
			keypoints, descriptors = self.image_features.imageKeypoints(image)
			bf = cv2.BFMatcher(cv2.NORM_L1, crossCheck=True)
			matches = bf.match(descriptors,query_descriptors)
			matches = sorted(matches, key = lambda x:x.distance)
			img3 = cv2.drawMatches(image, keypoints, query, query_keypoints, matches[:50], query, flags=2)
			imageFileName = imagePath[imagePath.rfind("/") + 1:]
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