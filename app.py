from flask import Flask, render_template,request
#scientific computing library for saving, reading, and resizing images
from scipy.misc import imsave, imread, imresize
#for matrix math
import numpy as np
#for importing our keras model
import keras.models
#for regular expressions, saves time dealing with string data
import re
import base64

from mimetypes import guess_extension
from urllib.request import urlretrieve

#system level operations (like loading files)
import sys 
#for reading operating system data
import os
#tell our app where our saved model is
sys.path.append(os.path.abspath("./model"))
from load import * 
#initalize our flask app
app = Flask(__name__)
#global vars for easy reusability
global model, graph
#initialize these variables
model, graph = init()

#decoding an image from base64 into raw representation

def convert_and_save(b64_string):
    with open("output.png", "wb") as fh:
        fh.write(base64.decodebytes(b64_string.encode()))

def convertImage(imgData1):
	imgstr = re.search(r'base64,(.*)', imgData1.decode('utf-8')).group(1)
	#print(imgstr)
	imgdata = base64.b64decode(imgstr)
	with open('output.png','wb') as output:

		output.write(imgdata)
	#fh = open("output.png", "wb")
	#fh.write(imgData1.decode('base64'))
	#fh.close()

@app.route('/')
def index():
	#initModel()
	#render out pre-built HTML file right on the index page
	return render_template("index.html")

@app.route('/predict/',methods=['GET','POST'])
def predict():
	#whenever the predict method is called, we're going
	#to input the user drawn character as an image into the model
	#perform inference, and return the classification
	#get the raw data format of the image
	imgData = request.get_data()
	#encode it into a suitable format
	convertImage(imgData)
	print ("debug")
	#read the image into memory
	x = imread('output.png',mode='L')
	#compute a bit-wise inversion so black becomes white and vice versa
	x = np.invert(x)
	#make it the right size
	x = imresize(x,(28,28))
	#imshow(x)
	#convert to a 4D tensor to feed into our model
	x = x.reshape(1,28,28,1)
	print ("debug2")
	#in our computation graph
	with graph.as_default():
		#perform the prediction
		out = model.predict(x)
		print(out)
		print(np.argmax(out,axis=1))
		print ("debug3")
		#convert the response to a string
		response = np.array_str(np.argmax(out,axis=1))
		return response	
	

if __name__ == "__main__":
	#decide what port to run the app in
	port = int(os.environ.get('PORT', 5000))
	#run the app locally on the givn port
	app.run(host='0.0.0.0', port=port,debug=True,threaded=True)
	#optional if we want to run in debugging mode
	#app.run(debug=True)
