from features import ImageFeatures
from searcher import Searcher
import cv2

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