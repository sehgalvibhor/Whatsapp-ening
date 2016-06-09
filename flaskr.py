import os
import sqlite3
import re
import csv
from nltk import FreqDist
from flask import Flask, request, session, g, redirect, url_for, abort,render_template, flash
from werkzeug.utils import secure_filename
from flask import send_from_directory


app = Flask(__name__)
app.config.from_object(__name__)

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = set(['txt'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def create_csv(filename,data):
	with open(os.path.join('static/',filename),'wb') as myfile :
		wr = csv.writer(myfile)
		wr.writerow(['word','weight'])
		for i in data :
			a,b = i
			wr.writerow([str(a),int(b)])





def cleaner(filename):
	textfile = open(os.path.join(app.config['UPLOAD_FOLDER'], filename),'r')
	text = []
	all_dates = []
	complete_text = []
	words_list = []
	nodes = []
	for line in textfile:
		datetime,chat = line.split('-')
		date, time = datetime.split(',')
		loc = chat.find(':')

		#if len(chat.split(':'))==3:
		#	print chat
		user,text = chat[:loc],chat[loc+2:]
		text = text.replace("\n",'')
		words = text.split(' ')
		for i in words:
			words_list.append(i)
		complete_text.append(text)
		nodes.append(user)
		all_dates.append(date)

	#print set(nodes)
	#print set(all_dates)
	fdist = FreqDist(words_list)
	f1 = fdist.most_common(100)
	create_csv('wordcloud.csv',f1)
	textfile.close()



def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            cleaner(filename)
            return render_template('dashboard.html')
    return render_template('index.html')