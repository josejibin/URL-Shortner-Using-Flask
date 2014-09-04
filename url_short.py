
import random
import os
import sqlite3
from flask import Flask,request,g,redirect,url_for,render_template,flash,session,jsonify,g,Response

app = Flask(__name__)


app.config.from_object(__name__)

app.config.update(dict(
   DATABASE=os.path.join(app.root_path,'url_collection.db'),
   DEBUG=True,
   SECRET_KEY='jibin jose',
   
  
))
app.config.from_envvar('FLASKR_SETTINGS',silent=True)



def connect_db():
  rv=sqlite3.connect(app.config['DATABASE'])
  rv.row_factory=sqlite3.Row
  return rv

def init_db():
  with app.app_context():
     db=get_db()
     with app.open_resource('schema.sql',mode='r')as f:
	db.cursor().executescript(f.read())
     db.commit()

def get_db():
  if not hasattr(g,'sqlite_db'):
     g.sqlite_db=connect_db()
  return g.sqlite_db



@app.route('/', methods=['GET', 'POST'])
def home():
  if request.method=="POST":  
    print "request"
    print request
    org_url=request.form["org_url"]
    db=get_db()
    cur = db.execute('select * from url where  original_url = (?)',[org_url])
    data = cur.fetchall()
    if data !=[]:
      short_url=data[0][2]
    else:
      short_url=str(random_string(5))
      db.execute('insert into url (original_url,shortened_url) values (?,?)',[request.form["org_url"],short_url])
      db.commit()  

  
    db = get_db()
    cur = db.execute('select original_url,shortened_url from url')
    posts = cur.fetchall()
    print posts
    return render_template('url.html', posts=posts)




@app.route('/<url>', methods=['GET', 'POST'])
def change(url=None):
  db=get_db()
  shortUrl=url
  cur = db.execute('select * from url where  shortened_url = (?)',[shortUrl])
  data = cur.fetchall()
 
  if data !=[]:
    orgUrl=data[0][1]
    return redirect(orgUrl, code=302)
  else:
    print "in else"
    return render_template('pageNotFound.html',url=url)
  


def random_string(length=5):
 possibles = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'
 return ''.join(random.choice(possibles) for i in range(0, length))

 



@app.teardown_appcontext
def close_db(error):
  if hasattr(g,'sqlite_db'):
     g.sqlite_db.close()

if __name__=='__main__':
 app.run(debug=True)
