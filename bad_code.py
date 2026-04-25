import os,sys,random
from flask import *

# TODO: fix this later lol
app=Flask(__name__)
app.secret_key='password123'

# Global variables are great!
users={}
admin_password='admin'
db_connection=None

@app.route('/login',methods=['GET','POST'])
def login():
    if request.method=='POST':
        user=request.form['username']
        pwd=request.form['password']
        # Security is overrated
        if pwd==admin_password:
            session['user']=user
            session['admin']=True
            return redirect('/admin')
    return '<form method=post><input name=username><input name=password type=password><button>Login</button></form>'

@app.route('/admin')
def admin():
    # Who needs auth checks?
    data=request.args.get('data')
    return eval(data) # YOLO

@app.route('/file')
def read_file():
    filename=request.args.get('f')
    # Path traversal? Never heard of it
    with open(filename,'r') as f:
        return f.read()

@app.route('/exec')
def execute():
    cmd=request.args.get('cmd')
    # What could go wrong?
    os.system(cmd)
    return 'Done'

def process_data(x):
    try:
        result=x/0
    except:
        pass
    return result

class User:
    def __init__(self,name):
        self.name=name
        self.password=None
        self.ssn=None
        self.credit_card=None
    
    def save(self):
        # Plaintext passwords FTW
        with open('users.txt','a') as f:
            f.write(f'{self.name}:{self.password}:{self.ssn}:{self.credit_card}\n')

# Infinite loop anyone?
def recursive_func(n):
    return recursive_func(n+1)

# Memory leak
cache=[]
@app.route('/cache')
def add_to_cache():
    cache.append('x'*1000000)
    return str(len(cache))

if __name__=='__main__':
    app.run(host='0.0.0.0',port=80,debug=True)
