#from werkzeug.contrib.fixers import ProxyFix
from flask import Flask, request, Blueprint, jsonify, render_template
from flask_restful import Api
import os, os.path, shutil
import ISOMapping
from ISOMapping import isoMapping
import timeit


api_blueprint = Blueprint('api', __name__, url_prefix='/api')
api = Api(api_blueprint)

app = Flask(__name__)
#app.config['SERVER_URL'] = 'https://cs445finalproject.azurewebsites.net'
#app.config['UPLOAD_FOLDER'] = "upload"
#app.wsgi_app = ProxyFix(app.wsgi_app)
app.register_blueprint(api_blueprint)


default_video_filepath = os.path.join('.','static','defaultvalues')#,'Video4_amn_cs445.mp4')
default_query_image_filepath = os.path.join('.','static','defaultvalues')#,'query_iso_amn_cs445.jpg')


@app.route('/', methods=['GET']) #allow both GET and POST requests
def home():
    return render_template("index.html")
    

@app.route('/search_ssd', methods=['GET', 'POST']) #allow both GET and POST requests
def form_example():
    from videosplitter import VideoSplitter
    from indexer import Indexer
    from search import Search

    if request.method == 'POST': #this block is only entered when the form is submitted
        dataset_path = 'video_frames'
        index_path = 'index.csv'
        query_path = 'static/defaultvalues'
        result_path = 'static/result'
        
        video = request.files['video']
        query_image = request.files['image']

        if(video.filename == ''):
            videofilename = 'static/defaultvalues/Video4_amn_cs445.mp4'
        else:
            # save video
            if os.path.exists(video.filename):
                os.remove(video.filename)
            video.save(os.path.join("", video.filename))
            videofilename = video.filename

        if(query_image.filename == ''):
            query_path = 'static/defaultvalues/query4_amn_cs445.png'
        else:
            #save query image
            if os.path.exists("static/defaultvalues/" + query_image.filename):
                os.remove("static/defaultvalues/" + query_image.filename)
            query_image.save(os.path.join(query_path, query_image.filename))
            query_path = os.path.join(query_path, query_image.filename)


        videoSplitter = VideoSplitter('video_frames')
        videoSplitter.splitVideo(videofilename)
        indexer = Indexer('index.csv', 'video_frames')
        indexer.indexImages()
        search = Search(dataset_path, index_path, query_path, result_path)
        results = search.performSearch()

        output = []
        for i in range(len(results)):
             image = results[i]
             output.append(image)
        return render_template("result.html", images = output)

    return render_template("index_ssd.html")


@app.route('/search_iso', methods=['GET', 'POST']) #allow both GET and POST requests
def form_ISO():
    from videosplitter import VideoSplitter
    from indexer import Indexer
    from search import Search

    if request.method == 'POST': #this block is only entered when the form is submitted
        dataset_path = 'video_frames'
        index_path = 'index.csv'
        query_path = 'static/defaultvalues'
        result_path = 'static/result'
        
        video = request.files['video']
        query_image = request.files['image']

        if(video.filename == ''):
            videofilename = 'static/defaultvalues/Video4_amn_cs445.mp4'
        else:
            # save video
            if os.path.exists(video.filename):
                os.remove(video.filename)
            video.save(os.path.join('static/defaultvalues/', video.filename))
            videofilename = video.filename

        if(query_image.filename == ''):
            query_path = 'static/defaultvalues/query_iso_amn_cs445.jpg'
        else:
            #save query image
            if os.path.exists("static/defaultvalues/" + query_image.filename):
                os.remove("static/defaultvalues/" + query_image.filename)
            query_image.save(os.path.join(query_path, query_image.filename))
            query_path = os.path.join(query_path, query_image.filename)

        output = isoMapping('static/defaultvalues/query_iso_amn_cs445.jpg')

        return render_template("result.html", images = output)
        

    return render_template("index_iso.html")


@app.route('/search_sift', methods=['GET', 'POST']) #allow both GET and POST requests
def form_example_2():
    from videosplitter import VideoSplitter
    from indexer import Indexer
    from search import Search

    if request.method == 'POST': #this block is only entered when the form is submitted
        dataset_path = 'video_frames'
        index_path = 'index.csv'
        query_path = 'queries'
        result_path = 'static/result'
        
        video = request.files['video']
        query_image = request.files['image']

        if(video.filename == ''):
            videofilename = 'static/defaultvalues/Video4_amn_cs445.mp4'
        else:
            # save video
            if os.path.exists(video.filename):
                os.remove(video.filename)
            video.save(os.path.join("", video.filename))
            videofilename = video.filename

        if(query_image.filename == ''):
            query_path = 'static/defaultvalues/query4_amn_cs445.png'
        else:
            #save query image
            if os.path.exists("static/defaultvalues/" + query_image.filename):
                os.remove("static/defaultvalues/" + query_image.filename)
            query_image.save(os.path.join(query_path, query_image.filename))
            query_path = os.path.join(query_path, query_image.filename)


        videoSplitter = VideoSplitter('video_frames')
        videoSplitter.splitVideo(videofilename)
        search = Search(dataset_path, index_path, query_path, result_path)
        results, matchResult = search.performKeypointsSearch()

        output = []
        matchOutput = []
        for i in range(len(results)):
            image = results[i]
            matchImage = matchResult[i]
            output.append(image)
            matchOutput.append(matchImage)
        return render_template("result-keypoints.html", images = output, matches = matchOutput)

    return render_template("index_sift.html")


@app.route('/search_orb', methods=['GET', 'POST']) #allow both GET and POST requests
def form_orb():	   
	global default_video_filename
	global default_query_image_filename
	default_img_name = "query4_amn_cs445.png"
	if request.method == 'POST': #this block is only entered when the form is submitted
		dataset_path = 'orb_video_frames'
		index_path = 'index_orb.csv'
		query_path	= os.path.join('.','static','defaultvalues')
		os.makedirs(query_path, exist_ok=True)
		result_path = os.path.join('.','static','result')
		os.makedirs(result_path, exist_ok=True)
		generate_frames = True
		video = request.files['video']
		query_image = request.files['image']

		print("video.filename:%s"%video.filename)
		if video.filename:
			# save video
			video_path = os.path.join(default_video_filepath, video.filename)
			if os.path.exists(video_path):
				os.remove(video_path)
			print("video_path:%s"%video_path)
			video.save(video_path)
			videofilename = video_path#video.filename
		else:
			videofilename = os.path.join(default_video_filepath, 'Video4_amn_cs445.mp4')
			dataset_path = 'orb_default_video_frames'
			index_path = 'index_orb_default.csv'	
			generate_frames = not(os.path.exists(dataset_path) and os.path.exists(index_path))
		
		print("query_image.filename:%s"%query_image.filename)
		if query_image.filename:
			#save query image
			query_img_path = os.path.join(query_path,query_image.filename)
			if os.path.exists(query_img_path):
				os.remove(query_img_path)
			query_image.save(query_img_path)
		else:
			query_img_path = os.path.join(default_query_image_filepath, default_img_name)
			
		print("generate_frames:%s"%generate_frames)
		if generate_frames:
			print("dataset_path:%s"%dataset_path)
			os.makedirs(dataset_path, exist_ok=True)
			t1 = timeit.default_timer()
			print("videofilename:%s"%videofilename)
			videoSplitter = VideoSplitter(dataset_path)
			videoSplitter.splitVideo(videofilename)
			print("Time taken in Splitting Video:%s"%(timeit.default_timer() - t1))
			t2 = timeit.default_timer()
			indexer = Indexer(index_path, dataset_path)
			indexer.indexImages()
			print("Time taken in Indexing images:%s"%(timeit.default_timer() - t2))
			t3 = timeit.default_timer()
			search = Search(dataset_path, index_path, query_img_path, result_path)
			results, matchResult = search.performORBKeypointsSearch()
			print("Time taken in ORB Search:%s"%(timeit.default_timer() - t3))
			print("results")
			print(results)
			print("matchResult")
			print(matchResult)
			
		else:
			# default video and image result
			results = ['.\\static\\result\\orb_frame90.jpg', '.\\static\\result\\orb_frame91.jpg', '.\\static\\result\\orb_frame68.jpg', '.\\static\\result\\orb_frame66.jpg', '.\\static\\result\\orb_frame70.jpg', '.\\static\\result\\orb_frame94.jpg', '.\\static\\result\\orb_frame92.jpg', '.\\static\\result\\orb_frame67.jpg', '.\\static\\result\\orb_frame73.jpg', '.\\static\\result\\orb_frame69.jpg', '.\\static\\result\\orb_frame65.jpg', '.\\static\\result\\orb_frame64.jpg']
			matchResult = ['.\\static\\result\\orb_frame90_match.jpg', '.\\static\\result\\orb_frame91_match.jpg', '.\\static\\result\\orb_frame68_match.jpg', '.\\static\\result\\orb_frame66_match.jpg', '.\\static\\result\\orb_frame70_match.jpg', '.\\static\\result\\orb_frame94_match.jpg', '.\\static\\result\\orb_frame92_match.jpg', '.\\static\\result\\orb_frame67_match.jpg', '.\\static\\result\\orb_frame73_match.jpg', '.\\static\\result\\orb_frame69_match.jpg', '.\\static\\result\\orb_frame65_match.jpg', '.\\static\\result\\orb_frame64_match.jpg']
			
		return render_template("result-keypoints.html", images = results, matches = matchResult, header="ORB Results", query_img=query_img_path)
	
	return render_template("index_orb.html", default_img_name=default_img_name)
	



""" The Commented Out Section is For Local Machines Use Only """
if __name__ == '__main__':
    #app.run(host='0.0.0.0', port="8400", debug=True)
    app.run(host='0.0.0.0', debug=True)
