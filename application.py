#from werkzeug.contrib.fixers import ProxyFix
from flask import Flask, request, Blueprint, jsonify, render_template
from flask_restful import Api
import os, os.path, shutil

api_blueprint = Blueprint('api', __name__, url_prefix='/api')
api = Api(api_blueprint)

app = Flask(__name__)
#app.config['SERVER_URL'] = 'https://cs445finalproject.azurewebsites.net'
#app.config['UPLOAD_FOLDER'] = "upload"
#app.wsgi_app = ProxyFix(app.wsgi_app)
app.register_blueprint(api_blueprint)

@app.route('/', methods=['GET']) #allow both GET and POST requests
def home():
    return "hi"
    

@app.route('/search', methods=['GET', 'POST']) #allow both GET and POST requests
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
            videofilename = 'static/defaultvalues/Video4.mp4'
        else:
            # save video
            if os.path.exists(video.filename):
                os.remove(video.filename)
            video.save(os.path.join("", video.filename))
            videofilename = video.filename

        if(query_image.filename == ''):
            query_path = 'static/defaultvalues/query4.png'
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

    return render_template("index.html")


@app.route('/search_keypoints', methods=['GET', 'POST']) #allow both GET and POST requests
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
            videofilename = 'static/defaultvalues/Video4.mp4'
        else:
            # save video
            if os.path.exists(video.filename):
                os.remove(video.filename)
            video.save(os.path.join("", video.filename))
            videofilename = video.filename

        if(query_image.filename == ''):
            query_path = 'static/defaultvalues/query4.png'
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

    return render_template("index.html")


""" The Commented Out Section is For Local Machines Use Only """
if __name__ == '__main__':
    #app.run(host='0.0.0.0', port="8400", debug=True)
    app.run(host='0.0.0.0', debug=True)