import os
from flask import Flask, request, render_template, url_for, redirect
from logging import DEBUG
from flask_caching import Cache
import image
import video
config = {
    "DEBUG": True,          # some Flask specific configs
    "CACHE_TYPE": "null", # Flask-Caching related configs
    "CACHE_DEFAULT_TIMEOUT": 0
}

imagesfolder = os.path.join('static', 'images')
videosfolder = os.path.join('static', 'videos')
app = Flask(__name__)
app.config.from_mapping(config)
cache = Cache(app)
app.logger.setLevel(DEBUG)

im='OutputKeypoints.jpg'
vi='deepak.mp4'

app.config['UPLOAD_image'] = imagesfolder
app.config['UPLOAD_video'] = videosfolder
@app.route("/")
@cache.cached(timeout=0)
def home():
    global im , vi
    print(vi)
    imagename = os.path.join(app.config['UPLOAD_image'], im)
    videoname = os.path.join(app.config['UPLOAD_video'], vi)
    return render_template("index.html" , outputkeypoint = imagename , outputvideo = videoname) 
	
@app.route("/imageupload", methods=['POST'])
def imageupload():
    global im
    if 'photo' in request.files:
        photo = request.files['photo']
        if photo.filename != '':
            print(photo.filename)
            #photo.filename = 'deepak.jpg'		
            photo.save(os.path.join(photo.filename))
            im = photo.filename
            image.func(im)
             
            
    return redirect(url_for('home'))

@app.route("/videoupload", methods=['POST'])
def videoupload():
    global vi
    if 'video' in request.files:
        photo = request.files['video']
        if photo.filename != '':
            #photo.filename = 'deepak.mp4'		
            photo.save(os.path.join(photo.filename))
            vi = photo.filename
            video.func(vi)
            
    return redirect(url_for('home'))

if __name__ == '__main__':
 app.run(debug=True)
