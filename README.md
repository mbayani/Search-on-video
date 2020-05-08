
## CS445 Final Project (Spring2020)
Search on Video - It provides ability to search images within a video.

## Team Members
1. Negin Kashkooli(Email: negink2@illinois.edu)
2. Mani Bayani(Email: mbayani2@illinois.edu)
3. Amit Agrawal(Email: amita3@illinois.edu)

## Motivation
Many businesses rely on visual data such as images and videos. In today’s information age, businesses
can be overwhelmed by the volume of information available online. Manually searching images
would be a time-consuming, and therefore costly, task. In order to effectively use visual data, an
image search mechanism is required. The goal of our project is to create an automated API-based
solution to reliably and accurately retrieve images from scattered image datasets. This type of search
mechanism could have many applications in business and technology. One potential use would be
to identify flaws in products based on product images so those defective products could be returned
to the appropriate department.

## Installation
It is written in python. All the python dependencies are in 'requirements.txt. Use pip command to install them.
```
pip install -r requirements.txt
```

## How to use?
This project has web interface. 
On Windows Platform, run below commands:
```
set FLASK_APP=application.py
flask run
```
On Linux/Mac Platform, run below commands:
```
export FLASK_APP=application.py
flask run
```
Open url http://localhost:5000 (if port is not overridden). It shows 4 different implementations.
1. SSD
2. SIFT
3. ISO Mapping
4. ORB

![Welcome Page](project-welcome%20page.png)

## Code Organization
Under root folder, we have following scripts:
- application.py - It provides web interface to the search engine. User can upload or use default video and a query image. 
- features.py - It extracts the keypoints and features.
- indexer.py - It save the features of a video frame into a file so we do not need to compute it again and again.
- ISOMapping.py - It has all the functionality of ISO Mapping.
- search.py - It takes query image and video frame and searches for closest match.
- searcher.py - It takes the match result and tries to find best match based on SSD or variance.
- videosplitter.py - It splits a video into individual frames.

## YouTube Presentation
[YouTube Presentation Link!](https://www.youtube.com/embed/7WtMH7xXYCE)
