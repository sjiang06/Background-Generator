This project contains files pertaining to the background generator. This file documents each directory, their files, and general implementation notes.

BACKGROUND GENERATOR
Contains directories and files related to random generation of backgrounds.
--generator--
The generator directory contains the html and script that creates random svg backgrounds. generator.html is the background generator; pattern.html contains the html for creating the golden angle spiral with svg.
--golden_angle_spiral--
Code downloaded from github that allows generation of spiral patterns using angles, dot size, and dot number. Can be useful to create the blossom pattern in svg.

HUMAN DETECTION
Contains files that process images for human faces and color detection.
--colorkmeans.py--
Uses k-clusters to find the dominant colors in an image. Processes png and jpg files.
--find_human.py--
Locates human faces in images and identifies the centroid of the face.
--svg_script.html--
Webpage that identifies the color clusters of an svg and allows user to change the color of each cluster by inputting a color code.

IMAGE PROCESSOR
Utility files, using python to perform image processing techniques, such as changing hue, resizing, rotating, finding objects in image, and cropping.

IMAGE RANKER
html webpage that allows user to label image. Labels can be fed into ML algorithm to differentiate into image categories (ie good and bad images).

Uses Angular for backend, Mongo for database. Database backend code can be found in webServer.js.