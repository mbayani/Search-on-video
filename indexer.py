from features import ImageFeatures
import os
import cv2

class Indexer:
	def __init__(self, index_file_name, image_dataset_path):
		self.index_file_name = index_file_name
		self.image_dataset_path = image_dataset_path
		self.image_feature = ImageFeatures((8, 12, 3))

	def indexImages(self):
		with open(self.index_file_name, "w") as results:
			for obj in os.scandir(self.image_dataset_path):
				imageName = obj.name
				print("imageFileName:%s"%imageName)
				imagePath = os.path.join(self.image_dataset_path, imageName)
				image = cv2.imread(imagePath)
				features = self.image_feature.getFeatures(image)
				features = [str(f) for f in features]
				results.write("%s,%s\n" % (imageName, ",".join(features)))