import cv2
import shutil
import os

class VideoSplitter:
  def __init__(self, video_frames_path):
    self.video_folder = video_frames_path
  
  def splitVideo(self, videoFile):
    shutil.rmtree(self.video_folder, ignore_errors=True)
    if not os.path.exists(self.video_folder):
      os.mkdir(self.video_folder)

    vidcap = cv2.VideoCapture(videoFile)
    success,image = vidcap.read()
    count = 0
    while success:
      cv2.imwrite(self.video_folder + "/frame%d.jpg" % count, image)
      success,image = vidcap.read()
      count += 1