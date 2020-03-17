from features import ImageFeatures
import glob
import cv2

class Indexer:
	def __init__(self, index_file_name, image_dataset_path):
		self.index_file_name = index_file_name
		self.image_dataset_path = image_dataset_path
		self.image_feature = ImageFeatures((8, 12, 3))

	def indexImages(self):
		results = open(self.index_file_name, "w")
		for imagePath in glob.glob(self.image_dataset_path + "/*.*"):
			imageName = imagePath[imagePath.rfind("/") + 1:]
			image = cv2.imread(imagePath)
			features = self.image_feature.getFeatures(image)
			features = [str(f) for f in features]
			results.write("%s,%s\n" % (imageName, ",".join(features)))
		results.close()