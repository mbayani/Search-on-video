# from werkzeug.contrib.fixers import ProxyFix
from flask import Flask, request, Blueprint, jsonify, render_template
from flask_restful import Api
import os, os.path, shutil
from shutil import copyfile
import ISOMapping
from ISOMapping import isoMapping
import timeit
from videosplitter import VideoSplitter
from indexer import Indexer
from search import Search

# api_blueprint = Blueprint('api', __name__, url_prefix='/api')
# api = Api(api_blueprint)

app = Flask(__name__)
# app.config['SERVER_URL'] = 'https://cs445finalproject.azurewebsites.net'
# app.config['UPLOAD_FOLDER'] = "upload"
# app.wsgi_app = ProxyFix(app.wsgi_app)
# app.register_blueprint(api_blueprint)



@app.route('/', methods=['GET'])  # allow both GET and POST requests
def home():
    return render_template("index.html")


@app.route('/search_ssd', methods=['GET', 'POST'])  # allow both GET and POST requests
def form_example():
    from videosplitter import VideoSplitter
    from indexer import Indexer
    from search import Search

    if request.method == 'POST':  # this block is only entered when the form is submitted
        dataset_path = 'video_frames'
        index_path = 'index.csv'
        query_path = 'static/defaultvalues'
        result_path = 'static/result'

        video = request.files['video']
        query_image = request.files['image']

        copyfile('static/defaultfiles/Video4_amn_cs445.mp4', 'static/defaultvalues/Video4_amn_cs445.mp4')
        copyfile('static/defaultfiles/query4_amn_cs445.png', 'static/defaultvalues/query4_amn_cs445.png')

        if (video.filename == ''):
            videofilename = 'static/defaultvalues/Video4_amn_cs445.mp4'
        else:
            # save video
            if os.path.exists(video.filename):
                os.remove(video.filename)
            video.save(os.path.join("", video.filename))
            videofilename = video.filename

        if (query_image.filename == ''):
            query_path = 'static/defaultvalues/query4_amn_cs445.png'
        else:
            # save query image
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
        return render_template("result.html", images=output)

    return render_template("index_ssd.html")


@app.route('/search_iso', methods=['GET', 'POST'])  # allow both GET and POST requests
def form_ISO():
    from videosplitter import VideoSplitter
    from indexer import Indexer
    from search import Search

    if request.method == 'POST':  # this block is only entered when the form is submitted
        dataset_path = 'video_frames'
        index_path = 'index.csv'
        query_path = 'static/defaultvalues'
        result_path = 'static/result'

        video = request.files['video']
        query_image = request.files['image']

        copyfile('static/defaultfiles/Video4_amn_cs445.mp4', 'static/defaultvalues/Video4_amn_cs445.mp4')
        copyfile('static/defaultfiles/query_iso_amn_cs445.jpg', 'static/defaultvalues/query_iso_amn_cs445.jpg')

        if (video.filename == ''):
            videofilename = 'static/defaultvalues/Video4_amn_cs445.mp4'
        else:
            # save video
            if os.path.exists(video.filename):
                os.remove(video.filename)
            video.save(os.path.join('', video.filename))
            videofilename = video.filename

        if (query_image.filename == ''):
            query_path = 'static/defaultvalues/query_iso_amn_cs445.jpg'
        else:
            # save query image
            if os.path.exists("static/defaultvalues/" + query_image.filename):
                os.remove("static/defaultvalues/" + query_image.filename)
            query_image.save(os.path.join(query_path, query_image.filename))
            query_path = os.path.join(query_path, query_image.filename)

        videoSplitter = VideoSplitter('video_frames')
        videoSplitter.splitVideo(videofilename)
        output = isoMapping(query_path)

        return render_template("result.html", images=output)

    return render_template("index_iso.html")


@app.route('/search_sift', methods=['GET', 'POST'])  # allow both GET and POST requests
def form_example_2():
    from videosplitter import VideoSplitter
    from indexer import Indexer
    from search import Search

    if request.method == 'POST':  # this block is only entered when the form is submitted
        dataset_path = 'video_frames'
        index_path = 'index.csv'
        query_path = 'static/defaultvalues'
        result_path = 'static/result'

        video = request.files['video']
        query_image = request.files['image']

        copyfile('static/defaultfiles/Video4_amn_cs445.mp4', 'static/defaultvalues/Video4_amn_cs445.mp4')
        copyfile('static/defaultfiles/query4_amn_cs445.png', 'static/defaultvalues/query4_amn_cs445.png')

        if (video.filename == ''):
            videofilename = 'static/defaultvalues/Video4_amn_cs445.mp4'
        else:
            # save video
            if os.path.exists(video.filename):
                os.remove(video.filename)
            video.save(os.path.join("", video.filename))
            videofilename = video.filename

        if (query_image.filename == ''):
            query_path = 'static/defaultvalues/query4_amn_cs445.png'
        else:
            # save query image
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
        return render_template("result-keypoints.html", images=output, matches=matchOutput, header="SIFT")

    return render_template("index_sift.html")


@app.route('/search_orb', methods=['GET', 'POST'])  # allow both GET and POST requests
def form_orb():
    default_img_name = "query4_amn_cs445.png"
    if request.method == 'POST':  # this block is only entered when the form is submitted
        copyfile('static/defaultfiles/Video4_amn_cs445.mp4', 'static/defaultvalues/Video4_amn_cs445.mp4')
        copyfile('static/defaultfiles/query4_amn_cs445.png', 'static/defaultvalues/query4_amn_cs445.png')

        dataset_path = 'orb_video_frames'
        index_path = 'index_orb.csv'
        query_path = os.path.join('.', 'static', 'defaultvalues')
        result_path = os.path.join('.', 'static', 'result')
        generate_frames = True
        video = request.files['video']
        query_image = request.files['image']

        print("video.filename:%s" % video.filename)
        if video.filename:
            # save video
            if os.path.exists(video.filename):
                os.remove(video.filename)
            video.save(os.path.join("", video.filename))
            videofilename = video.filename
        else:
            videofilename = os.path.join(query_path, 'Video4_amn_cs445.mp4')
            dataset_path = os.path.join('.','orb_default_video_frames')
            index_path = os.path.join('.','index_orb_default.csv')
            print("os.path.exists(%s):%s"%(dataset_path,os.path.exists(dataset_path)))
            print("os.path.exists(%s):%s"%(index_path, os.path.exists(index_path)))

        print("query_image.filename:%s" % query_image.filename)
        if query_image.filename:
            # save query image
            query_img_path = os.path.join(query_path, query_image.filename)
            if os.path.exists(query_img_path):
                os.remove(query_img_path)
            query_image.save(query_img_path)
        else:
            query_img_path = os.path.join(query_path, default_img_name)

        print("query_img_path:%s"%query_img_path)
        print("generate_frames:%s" % generate_frames)

        print("dataset_path:%s" % dataset_path)
        os.makedirs(dataset_path, exist_ok=True)
        t1 = timeit.default_timer()
        print("videofilename:%s" % videofilename)
        videoSplitter = VideoSplitter(dataset_path)
        videoSplitter.splitVideo(videofilename)
        print("Time taken in Splitting Video:%s" % (timeit.default_timer() - t1))
        t2 = timeit.default_timer()
        indexer = Indexer(index_path, dataset_path)
        indexer.indexImages()
        print("Time taken in Indexing images:%s" % (timeit.default_timer() - t2))
        t3 = timeit.default_timer()
        search = Search(dataset_path, index_path, query_img_path, result_path)
        results, matchResult = search.performORBKeypointsSearch()
        print("Time taken in ORB Search:%s" % (timeit.default_timer() - t3))
        print("results")
        print(results)
        print("matchResult")
        print(matchResult)

        return render_template("result-keypoints.html", images=results, matches=matchResult, header="ORB Results",
                               query_img=query_img_path)

    return render_template("index_orb.html", default_img_name=default_img_name)


""" The Commented Out Section is For Local Machines Use Only """
if __name__ == '__main__':
    # app.run(host='0.0.0.0', port="8400", debug=True)
    app.run(host='0.0.0.0', debug=True)
