from flask import *
from xlrd import open_workbook
from xlutils.copy import copy
from werkzeug.utils import secure_filename
import os
import time

app = Flask(__name__)
app.secret_key='djskgaheoihgarg'
app.config['UPLOAD_FOLDER'] = os.getcwd()+'\static\picture'
app.config['MAX_CONTENT_LENGTH'] = 4 * 1024 * 1024

ALLOWED_EXTENSIONS=set(['jpg','png','jpeg','gif'])

def allowed_file(filename):
	return '.' in filename and \
		filename.rsplit('.',1)[1] in ALLOWED_EXTENSIONS

@app.route('/',methods=["GET"])
def welcome():
	return redirect(url_for('signin'))
	
@app.route('/signin/',methods=['GET'])
def signin():
	return render_template('signin.html',message='请登录')
	
@app.route('/signin/',methods=['POST'])
def signin_button():
	username=request.values.get('username')
	password=request.values.get('password')
	if username=='' or password=='':
		return render_template('signin.html',username=username,message='请输入用户名或密码')
	oldbook=open_workbook('users.xls')
	oldsheet=oldbook.sheet_by_index(0)
	i=0
	while True:
		user=oldsheet.cell(i,0).value
		if user=='END':
			break
		if user==username:
			if str(password)==str(int(oldsheet.cell(i,1).value)):
				return redirect(url_for('home',name=username))
			else:
				return render_template('signin.html',username=username,message='密码错误，请重新输入')
		i=i+1
	return render_template('signin.html',username=username,message='无此用户，请联系管理员')

@app.route('/home/<name>',methods=['GET'])
def home(name):
	user=name
	oldbook=open_workbook('users.xls')
	oldsheet=oldbook.sheet_by_index(0)
	i=0
	while True:
		user=oldsheet.cell(i,0).value
		if user=='END':
			break
		if user==name:
			return render_template('home.html',username=name)
		i=i+1
	return redirect(url_for('signin'))
	
@app.route('/home/<name>',methods=['POST'])
def home_button(name):
	date=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
	classes=request.values.get('classes')
	cause=request.values.get('cause')
	if 'picture' not in request.files:
		return render_template('home.html',username=name,classes=classes,cause=cause,message='没有上传图片')
	picture=request.files['picture']
	if picture.filename=='':
		return render_template('home.html',username=name,classes=classes,cause=cause,message='没有上传图片')
	if picture and allowed_file(picture.filename):
		oldbook=open_workbook('data.xls')
		oldsheet=oldbook.sheet_by_index(0)
		i = int(oldsheet.cell(0,4).value)
		filename=secure_filename(picture.filename)
		picture.save(os.path.join(app.config['UPLOAD_FOLDER'],str(i)+'.jpg'))
		newbook=copy(oldbook)
		sheet1=newbook.get_sheet(0)
		sheet1.write(i,0,name)
		sheet1.col(0).width=3333
		sheet1.write(i,1,classes)
		sheet1.col(1).width=3333
		sheet1.write(i,2,cause)
		sheet1.col(2).width=3333
		sheet1.write(i,3,date)
		sheet1.col(3).width=6666
		i=i+1
		sheet1.write(0,4,i)
		newbook.save('data.xls')
		return redirect(url_for('home',name=name))
	else:
		return render_template('home.html',username=name,classes=classes,cause=cause,message='图片格式不正确，格式应该为jpg,png.jpeg,gif中的一个')
		
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],filename)

@app.route('/show/',methods=['GET'])
def show():
	oldbook=open_workbook('data.xls')
	oldsheet=oldbook.sheet_by_index(0)
	i = int(oldsheet.cell(0,4).value)
	names=[]
	classes=[]
	causes=[]
	dates=[]
	pictures=[]
	for x in range(1,i):
		names.append(oldsheet.cell(x,0).value)
		classes.append(oldsheet.cell(x,1).value)
		causes.append(oldsheet.cell(x,2).value)
		dates.append(oldsheet.cell(x,3).value)
		path='/static/picture/'+str(x)+'.jpg'
		pictures.append(path)
	return render_template('show.html',i=i,names=names,classes=classes,causes=causes,dates=dates,pictures=pictures)

if __name__=='__main__':
    app.run(host='0.0.0.0',port=14250,threaded=True)