# pyimgresize

Image File Size Optimization. 

This process is performed with multiple libraries based on python. This is a batch process, which will take a bunch of files from google cloud storage and process it and send those files back to their destinations in google cloud storage.

Types of libraries 

Open CV
Pillow
Sk image
Wand

Open CV

OpenCV is a library of programming functions mainly aimed at real-time computer vision. Originally developed by Intel. The library is cross-platform and free for use under the open-source Apache 2 License. It stands for Open Source Computer Vision Library. It is capable of processing images and videos to identify objects, faces, or even handwriting. OpenCV-Python is an appropriate tool for fast prototyping of Computer Vision problems.
This library uses NumPy and all its array structures convert to and from NumPy arrays.


Performance
A test was performed on 20 images to resize and optimize . The time taken for 20 images is 16 seconds and the reduction of the image is from half and less the half the size, there are few file which are going 5X reduction. Its due to the color profile of every image is different from each other.


Pillow


Pillow or PIL is a python library which adds image processing capabilities to python interpreter. This library provides extensive file format support, an efficient internal representation, and fairly powerful image processing capabilities.

Performance 
For testing 20 images it took 23 secs with different resolutions and a 19 Mb file is getting converted to 300 kb size image width is getting differed 


SKimage

Scikit-image, or skimage, is an open source Python package designed for image preprocessing. scikit-image builds on scipy.ndimage to provide a versatile set of image processing routines in Python.

Performance 
For testing 20 images it took 54 secs with different resolutions, and the file reduction is better 31.1 Mb file is converted into 1.1MB


Wand
Wand is a ctypes-based simple ImageMagick binding for Python. Imagemagick is a tool developed to convert images from one format to another.  The Wand is an Imagick library for python. It supports the functionalities of Imagick API in Python 2.6, 2.7, 3.3+, and PyPy.This library not only helps in processing the images but also provides valuable functionalities for Machine Learning codes using NumPy.
Performance 
For testing 20 image it took 1 min 13 secs with different resolution, and the file reduction is 5X



Current Approach:



The Current Approach, all the files will download from cloud storage and Optimize the image and push the image back to cloud storage with the same folder structure.

Image Processing is a Command Line Application. We need to pass args like file_path, height, width.
This Application uses libraries in python like OpenCV2, Wand, PIL.
The reason we are using different libraries is because of the different formats available in cloud storage like JPEG, JPG, PNG, WEPG.
We need to optimize all the image formats, but the image processing rates are varying between these formats and these libraries.
This application will take in the image with more storage size, and it will reduce the image file size without affecting the image quality

User Arch:
	


Category team will upload all the files to the image processing instance VIA FTP.
The reason we are pushed via FTP is to reduce the cost for uploading and downloading.
And we can schedule Cloud Functions triggers for this process and the category team can trigger this after uploading the files to instance.
The image processing Application will remove the files from the instance after image processing and uploading into cloud storage
