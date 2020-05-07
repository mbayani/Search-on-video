
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
The project has web interface. set ```FLASK_APP``` to ```application.py``` and run flask. Open url http://localhost:5000 (if port is not overridden).
It shows 4 different implementations.
1. SSD
2. SIFT
3. ISO Mapping
4. ORB

[Welcome Page](./project-welcome page.png)

