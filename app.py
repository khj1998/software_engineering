from flask import Flask,render_template,redirect,url_for,request,session,redirect
import sqlite3
import os
from tkinter import *
from tkinter import messagebox
app=Flask(__name__)
app.secret_key="asdasjdoijoj!#!@#"

User_table={}
now_login_id,now_id_follower,key_word=[],[],[]
block_error=-1
global second
second = 0

####상품사진업로드를 위한 경로###
picfolder=os.path.join('static','pics')
app.config['UPLOAD_FOLDER']=picfolder
####상품사진업로드를 위한 경로###

#####keyword 테이블에서 키워드들을 불러온다.#####
def get_keyword():
    global key_word
    conn=sqlite3.connect('keyword.db')
    cur=conn.cursor()
    cur.execute('SELECT * FROM keyword')
    data=cur.fetchall()
    conn.close()

    for i in data:
        key_word.append(i[0])

#######데이터베이스에서 유저 id,pw 정보 딕셔너리 형태로 가져오기#######
def set_user_info():
    global User_table
    conn=sqlite3.connect('user.db')
    cur=conn.cursor()
    cur.execute("SELECT * FROM user_info")
    data=cur.fetchall()
    conn.close()

    for i in data:
        if i[0] not in User_table.keys():
            User_table[i[0]]=i[1]

########회원 가입한 회원의 정보를 딕셔너리, db에 추가한다########
def add_user_info(id,pw):
    global User_table
    User_table[id]=pw
    conn=sqlite3.connect('user.db')
    cur=conn.cursor()
    cur.execute("INSERT INTO user_info VALUES(?,?)",(id,pw))
    cur.execute("CREATE TABLE {}(follow_id varchar(50))".format(id))

    conn.commit()
    conn.close()

###현재 로그인한 아이디 테이블에서 팔로우한 아이디 정보 불러오기
def get_follower():
    global now_id_follower

    conn=sqlite3.connect('user.db')
    cur=conn.cursor()
    cur.execute('SELECT * FROM {}'.format(now_login_id[0]))
    data=cur.fetchall()
    for i in data:
        now_id_follower.append(i[0])
    conn.close()

###팔로워 추가하기 추후 업데이트##
def add_user_follower(following_id):
    conn=sqlite3.connect('user.db')
    cur=conn.cursor()
    cur.execute('SELECT * FROM {}'.format(now_login_id[0]))
    cur.execute('INSERT INTO {} VALUES(?)'.format(now_login_id[0]),(following_id,))

    ##### 현재 로그인된 아이디 리스트 이름에 해당하는 테이블에 팔로우 아이디데이터를 추가할것.
    conn.commit()
    conn.close()
    return

###### 업로드시 상품명만 add_keyword한다. ######
def add_keyword(key_word,filename):
    filename=filename.split('.')
    filename=filename[0]

    if filename not in key_word:
        key_word.append(filename)
        conn=sqlite3.connect('keyword.db')
        con=conn.cursor()
       
        con.execute("INSERT INTO keyword VALUES (?)",(filename,)) #Without the comma, (img) is just a grouped expression, not a tuple, and thus the img string is treated as the input sequence
        conn.commit()
        conn.close()


def add_product(name,price):
    global User_table
    conn=sqlite3.connect('user.db')
    cur=conn.cursor()
    cur.execute("INSERT INTO product VALUES(?,?,?)",(name,price,"slg126"))

    conn.commit()
    conn.close()

###로그인한 유저의 아이디정보로 폴더생성###
def CreateFolder(id):
    if not os.path.exists(id):
        os.makedirs(id)

@app.route('/')
def home():
    global User_table
    
    if second == 1:
        if "userid" in session:
            return render_template("home.html",username=session.get("userid"),login=True, next=True)
        else:
            return render_template('home.html',login=False, next=False)

    else:
        if "userid" in session:
            return render_template("home.html",username=session.get("userid"),login=True)
        else:
            return render_template('home.html',login=False)

@app.route('/search',methods=["get"])
def search():
    search=request.args.get("searched")
    next_page="{}.html".format(search)

    if search in key_word:
        return render_template(next_page)
    else:
        return redirect(url_for('home'))

@app.route('/sign_in',methods=["get"])
def sign_in():
    global User_table
    _ID_=request.args.get("new_id")
    _PW_=request.args.get("new_pw")

    if _ID_==None or _PW_==None:
        return render_template('sign_up.html',create=-1)
    elif _ID_ in User_table.keys():
        return render_template('sign_up.html',create=-1)
    elif _ID_ not in User_table.keys():
        add_user_info(_ID_,_PW_)
        return redirect(url_for('home'))

@app.route('/sign_up')
def sign_up():
    return render_template('sign_up.html')


@app.route('/login_page')
def login_page():
    return render_template("login_page.html")

@app.route('/test')
def test():
    return render_template("test.html")

@app.route('/log_in',methods=["get"])
def log_in():
    global now_login_id

    _id_=request.args.get("login_id")
    _password_=request.args.get("login_pw")
    
    now_login_id=[_id_]

    CreateFolder(_id_) ### 특정 유저의 판매이미지를 따오기위한 경로 폴더생성

    if _id_ in User_table.keys() and User_table[_id_]==_password_:
        session["userid"]=_id_
        second=0
        return redirect(url_for("home"))
    else:
        return render_template('login_page.html',answer=False)
       

@app.route('/mypage')
def mypage():
    get_follower()
    global second
    second = 1    
    return render_template("mypage.html",username=now_login_id[0],id_list=User_table.keys(),follow_list=now_id_follower)


@app.route('/log_out')
def log_out():
    global now_login_id,now_id_follower

    session.pop("userid")
    if now_login_id:
        del now_login_id[0]
    now_id_follower.clear()
 
    return render_template('home2.html')

@app.route('/mypage_list')
def mypage_list():
    return render_template('mypage2.html')

@app.route('/follow',methods=["get"])
def follow():
    _id_=request.args.get("follower_id")
    print('전달받은 아이디: '+_id_)
    add_user_follower(_id_)

    return redirect(url_for("mypage"))

@app.route('/show_follower',methods=['get'])
def show_follower():
    _id_=request.args.get("follower_id")
    print(_id_)

    return redirect(url_for("mypage"))

@app.route('/sale_product', methods=["get"])
def sale_product():
    name = request.args.get("product_name")
    price = request.args.get("product_price")
    add_product(name, price)

    return render_template('upload.html')

@app.route('/upload',methods=["post"])
def upload():
    global block_error,key_word
    
    if block_error!=-1:
        if 'file' in request.files:
            img=request.files['file']
            img.save("static\img\{}".format(img.filename))
            img.save("{0}\{1}".format(session["userid"],img.filename))
            add_keyword(key_word,img.filename)
    block_error=1

    return render_template('upload.html')

if __name__=='__main__':
    get_keyword()
    set_user_info()
    app.run(debug=True)