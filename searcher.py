import numpy as np
import csv

class Searcher(object):
	def __init__(self, indexPath):
		self.indexPath = indexPath        

	def search(self, queryFeatures, limit = 10):
		results = {}
		with open(self.indexPath) as f:
			reader = csv.reader(f)
			for row in reader:
				features = [float(x) for x in row[1:]]
				d = self.square_distance(features, queryFeatures)
				results[row[0]] = d
			f.close()
		results = sorted([(v, k) for (k, v) in results.items()])
		return results[:limit]

	def square_distance(self, histA, histB, eps = 1e-10):
		d = np.sum([((a - b) ** 2)
			for (a, b) in zip(histA, histB)])
		return d
	
	def searchKeypoints(self, matches, limit = 10):
		results = sorted([(v, k) for (k, v) in matches],reverse = True)
		return results[:limit]