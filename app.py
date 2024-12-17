from flask import Flask,render_template,request,redirect,url_for,session
from flask_mysql_connector import MySQL #old version
# from flask_mysqldb import MySQL
import os

app=Flask(__name__)

app.config['MYSQL_HOST']='localhost'
app.config['MYSQL_USER']='root'
app.config['MYSQL_PASSWORD']=''
app.config['MYSQL_DB']='ictinfo'

UPLOAD_FOLDER='static/uploads'
app.config['UPLOAD_FOLDER']=UPLOAD_FOLDER

app.secret_key="hello"

mysql=MySQL(app)

@app.route('/connect')
def connect():
    try:
        #create a cursor
        cur=mysql.connection.cursor()
        #code for conector to connect the database(not needed if use from flask_mysqldb import MySQL)
        cur.execute("USE ictinfo")
        # create a query
        query="SELECT DATABASE()"
        #execute the query
        cur.execute(query)
        #fetch data
        db_name=cur.fetchone()
        return f"My database connected is : {db_name}"
    except Exception as e:
        return f"Error is : {e}"
    finally:
        cur.close()


@app.route('/index')
def index():
     return redirect(url_for("home"))

@app.route('/addblog')
def addblog():
    return render_template("addblog.html")

@app.route('/viewblog')
def viewblog():
    return render_template("viewblog.html")


@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/contact')
def contact():
    return render_template("contact.html")




@app.route("/")
def home():
    if "user" in session:
        try:
            cur = mysql.connection.cursor()
            cur.execute("USE ictinfo")
            cur.execute("SELECT id, post_text, hashtags, media_path, created_at FROM posts ORDER BY created_at DESC")
            posts = cur.fetchall()
            print(posts)
            return render_template("index.html", posts=posts)
        except Exception as e:
            return f"Error: {e}"
    else:
        return render_template("login.html")

@app.route("/register",methods=["POST","GET"])
def register():
    if request.method=="POST":
        name=request.form['txt']
        mobile=request.form['mobile']
        pswd=request.form['pswd']
        try:
            #create a cursor
            cur=mysql.connection.cursor()
            #code for conector to connect the database(not needed if use from flask_mysqldb import MySQL)
            cur.execute("USE ictinfo")
            #execute the query
            cur.execute("INSERT INTO user(name,mobile,password)VALUES(%s,%s,%s)",(name,mobile,pswd))
            mysql.connection.commit()
            return redirect(url_for("home"))
        except Exception as e:
            return f"Exception thrown is : {e}"
        finally:
            cur.close()
@app.route("/login",methods=["POST","GET"])
def login():
    mobile=request.form['mobile']
    pswd=request.form['pswd']
    if request.method=="POST":
        try:
                #create a cursor
                cur=mysql.connection.cursor()
                #code for conector to connect the database(not needed if use from flask_mysqldb import MySQL)
                cur.execute("USE ictinfo")
                #execute the query
                cur.execute("SELECT * FROM  user WHERE mobile=%s AND password=%s",(mobile,pswd))
                user=cur.fetchone()
                if len(user)>1:
                     session['user']=mobile
                     session['name']=user[1]
                     session['type']="user"
                     return render_template("index.html")
                else:
                     return redirect(url_for("home"))
        except Exception as e:
                return f"Exception thrown is : {e}"
        finally:
                cur.close()
@app.route('/addpost', methods=["POST","GET"])
def add_post():
    if request.method == "POST":
        try:
            # Collect form data
            post_text = request.form.get("post_text")
            hashtags = request.form.get("hashtags")
            file = request.files['mediaUpload']  # Get uploaded file

            # Save file to the UPLOAD_FOLDER
            if file:
                filename = file.filename
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(file_path)  # Save file to the static/uploads directory
            else:
                file_path = None

            # Insert data into the database
            cur = mysql.connection.cursor()
            cur.execute("USE ictinfo")
            cur.execute("INSERT INTO posts(post_text, hashtags, media_path)VALUES (%s, %s, %s)", (post_text, hashtags, file_path))
            mysql.connection.commit()
            return redirect(url_for("home"))
        except Exception as e:
            return f"Error: {e}"
        finally:
            cur.close()
def upload():
     if 'file' in request.FILES:
          file=request.FILES['file']
          fname=file.filename
          fpath=os.path.join(app.config['UPLOAD_FOLDER'],fname)
          file.save(fpath)

if __name__=="__main__":
    app.run(debug=True)
