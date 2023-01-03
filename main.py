from flask import Flask , render_template, request,redirect,session,send_file
from os import path,listdir
from termcolor import cprint
import json
import random
from time import time,sleep

app = Flask(__name__)
app.secret_key ="secret"

@app.route('/getImg/<path:p>',methods=['GET'])
def getImg(p):
    startTime = time()
    cprint(f"Users Data Sent:{time()-startTime}",'cyan')
    if path.exists(p):
        return send_file(p)
    return render_template("error.html",error=f"{p} does not exist")

@app.route('/play/<path:ver>',methods=['GET'])
def play(ver):
    startTime = time()
    p = f'qna/{ver}'
    if not path.exists(p):
        return render_template("error.html",error=f"{p} does not exist")
    categories = listdir(p)
    categories.remove('img')
        
    cprint(f"Users Data Sent:{time()-startTime}",'cyan')
    return render_template("play.html",categories=categories)


@app.route('/qna',methods=['POST'])
def qna():
    startTime = time()
    result = {"question":"Error","answer":"Error"}
    # Set all data recived to session
    rData = json.loads(request.data) 
    
    #Print data Recived
    cprint(f"qna {rData}",'blue')
    
    if not('version' in rData and 'category' in rData and 'value' in rData):
        return result
    
    p = f"qna/{rData['version']}/{rData['category']}/{rData['value']}.json"
    if not path.exists(p):
        return  result
    
    with open(p,'r') as file:
        qnas = json.load(file)
    
    if 'qnas' in qnas and qnas['qnas']:
        i = random.randrange(0,len(qnas['qnas']))
        result = qnas['qnas'][i]
        
    cprint(f"Users Data Sent:{time()-startTime}",'cyan')
    return result


@app.route('/')
@app.route('/<path:p>')
def default(p=""):
    cprint(f"Data Recived:{p}",'blue')
    for key, value in request.form.items():
        cprint((key,value),'blue')
        
    if p == "":
        return render_template("index.html",session=session)
    p = p.lower()+".html"
    if path.exists(f"templates/{p}") and not p.startswith('0'):
        return render_template(p)
    return render_template("error.html",error=f"{p} does not exist")

if __name__ == "__main__":
    app.run(debug=False)